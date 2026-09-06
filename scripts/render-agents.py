#!/usr/bin/env python3
"""Render native Codex roles using Python 3.11's standard library only.

Supported portable fields: name, description, developer_instructions, model,
model_provider (OpenCode requires openai and an explicit model),
model_reasoning_effort. OpenCode maps
model to openai/<model> and effort to options.reasoningEffort; omitted values
inherit runtime defaults. Provider-qualified native model IDs are rejected.

Native sandbox_mode="read-only" maps to an OpenCode deny-by-default read/glob/grep
allowlist. These are not equivalent guarantees: Codex permits read-only shell
inspection, MCP approvals are separate, and parent runtime permission overrides
apply after role settings. OpenCode rejects other sandbox modes, approval_policy,
and nickname_candidates rather than broadening permissions. All other fields fail
closed for both targets; extend validation deliberately when adding a documented
native option.
References: github.com/openai/codex/blob/main/codex-rs/agent-roles/src/
agent_role_config.rs (role metadata plus flattened ConfigToml),
developers.openai.com/codex/config-reference/, opencode.ai/docs/agents/.

Every TOML source is copied to Codex or rendered for OpenCode. OpenCode-native
Markdown is owned separately and copied by the installer, not this renderer.

Success stdout is one JSON object: harness, sources, rendered, written, output
(absolute directory or null). Diagnostics use stderr.
Validation/I/O failures exit 1; argument errors exit 2. No network or installs.
Output is preflighted in full, staged, then atomically replaced per file. This
is not a whole-directory transaction: callers should stage before activation.
Unrelated files are retained, never deleted.
"""
import argparse
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ai/codex/agents"
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*\Z")
REQUIRED = {"name", "description", "developer_instructions"}
PORTABLE = REQUIRED | {"model", "model_provider", "model_reasoning_effort", "sandbox_mode"}
NATIVE_ONLY = {"approval_policy", "nickname_candidates"}
EFFORTS = {"none", "minimal", "low", "medium", "high", "xhigh"}


def safe_path(path):
    """Reject symlinks in every component before normalizing the path."""
    path = Path(path).absolute()
    if ".." in path.parts:
        raise ValueError(f"unsafe parent traversal: {path}")
    for current in (*reversed(path.parents), path):
        if current.is_symlink():
            raise ValueError(f"refusing symlink: {current}")
    return path


def parse_source(path):
    safe_path(path)
    if not path.is_file():
        raise ValueError(f"not a regular source file: {path}")
    raw = path.read_bytes()
    try:
        data = tomllib.loads(raw.decode("utf-8"))
    except tomllib.TOMLDecodeError as error:
        raise ValueError(f"{path.name}: invalid TOML: {error}") from error
    for field in REQUIRED:
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"{path.name}: {field} must be meaningful and nonempty")
    name = data["name"]
    if not NAME.fullmatch(name):
        raise ValueError(f"{path.name}: unsafe name")
    if name != path.stem:
        raise ValueError(f"{path.name}: name must match filename")
    unknown = data.keys() - PORTABLE - NATIVE_ONLY
    if unknown:
        raise ValueError(f"{name}: unsupported native fields: {', '.join(sorted(unknown))}")
    for field in ("model", "model_provider"):
        if field in data and (not isinstance(data[field], str)
                              or not NAME.fullmatch(data[field])):
            raise ValueError(f"{name}: unsupported {field}; use an unqualified native identifier")
    enums = {
        "model_reasoning_effort": EFFORTS,
        "sandbox_mode": {"read-only", "workspace-write", "danger-full-access"},
        "approval_policy": {"untrusted", "on-failure", "on-request", "never"},
    }
    for field, choices in enums.items():
        if field in data and (not isinstance(data[field], str) or data[field] not in choices):
            raise ValueError(f"{name}: unsupported {field}")
    if "nickname_candidates" in data:
        candidates = data["nickname_candidates"]
        if not isinstance(candidates, list) or not candidates or not all(
            isinstance(item, str) and item.strip() for item in candidates
        ):
            raise ValueError(f"{name}: nickname_candidates must be nonempty strings")
    return data, raw


def yaml_json(value):
    # JSON flow values are YAML-compatible, except JSON's surrogate-pair escapes
    # are rejected by YAML parsers. Keep Unicode scalars literal while escaping
    # YAML line breaks and non-printable C1 controls to prevent folding/loss.
    text = json.dumps(value, ensure_ascii=False)
    return re.sub(r"[\x7f-\x9f\u2028\u2029]",
                  lambda match: f"\\u{ord(match[0]):04x}", text)


def render_opencode(data):
    unsupported = data.keys() & NATIVE_ONLY
    if "sandbox_mode" in data and data["sandbox_mode"] != "read-only":
        unsupported.add("sandbox_mode")
    if unsupported:
        raise ValueError(f"{data['name']}: no OpenCode translation for {', '.join(sorted(unsupported))}")
    if data.get("model_provider", "openai") != "openai":
        raise ValueError(f"{data['name']}: unsupported custom model_provider for OpenCode")
    if "model_provider" in data and "model" not in data:
        raise ValueError(f"{data['name']}: model_provider requires an explicit model for OpenCode")
    meta = {"description": data["description"], "mode": "subagent"}
    if data.get("sandbox_mode") == "read-only":
        meta["permission"] = {"*": "deny", "read": "allow", "glob": "allow", "grep": "allow"}
    if "model" in data:
        meta["model"] = "openai/" + data["model"]
    if "model_reasoning_effort" in data:
        meta["options"] = {"reasoningEffort": data["model_reasoning_effort"]}
    frontmatter = "".join(f"{key}: {yaml_json(value)}\n"
                          for key, value in meta.items())
    return ("---\n" + frontmatter + "---\n" + data["developer_instructions"]).encode("utf-8")


def preflight(destination, source, rendered):
    safe_path(destination)
    if (destination == source or source in destination.parents
            or destination in source.parents):
        raise ValueError("output must not overlap canonical source")
    for parent in (*destination.parents, destination):
        if parent.exists() and not parent.is_dir():
            raise ValueError(f"output ancestor is not a directory: {parent}")
    # Detect cross-platform filename aliases rather than overwriting a different
    # spelling on case-insensitive filesystems.
    existing = {p.name.casefold(): p.name for p in destination.iterdir()} if destination.exists() else {}
    for filename in rendered:
        if filename.casefold() in existing and existing[filename.casefold()] != filename:
            raise ValueError(f"output filename collision: {filename}")
        path = safe_path(destination / filename)
        if path.exists() and not path.is_file():
            raise ValueError(f"not a regular output file: {path}")


def write_outputs(destination, rendered):
    destination.mkdir(parents=True, exist_ok=True)
    staged = []
    try:
        # Finish all serialization and staging before replacing any output file.
        for filename, content in rendered.items():
            with tempfile.NamedTemporaryFile(prefix=".render-agent-", dir=destination,
                                             delete=False) as stream:
                temporary = Path(stream.name)
                staged.append((temporary, destination / filename))
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            temporary.chmod(0o644)
        for temporary, target in staged:
            safe_path(target)
            os.replace(temporary, target)
    finally:
        for temporary, _ in staged:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", type=Path, default=SOURCE, help="Native TOML source directory")
    parser.add_argument("--harness", choices=("opencode", "codex"), default="opencode")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true", help="Validate only (default; no writes)")
    action.add_argument("--output", type=Path, help="Explicit output agents directory")
    args = parser.parse_args(argv)
    try:
        source = safe_path(args.source)
        paths = sorted(source.glob("*.toml"))
        if not paths:
            raise ValueError(f"no agents found in {source}")
        agents = [parse_source(path) for path in paths]
        names = {data["name"] for data, _ in agents}
        if len({name.casefold() for name in names}) != len(agents):
            raise ValueError("duplicate or case-colliding source names")
        rendered = {}
        for data, raw in agents:
            name = data["name"]
            if args.harness == "codex":
                rendered[name + ".toml"] = raw
            else:
                rendered[name + ".md"] = render_opencode(data)
        destination = safe_path(args.output) if args.output is not None else None
        if destination is not None:
            preflight(destination, source, rendered)
            write_outputs(destination, rendered)
        print(json.dumps({"harness": args.harness, "sources": len(agents),
                          "rendered": len(rendered),
                          "written": len(rendered) if destination is not None else 0,
                          "output": str(destination) if destination is not None else None}))
        return 0
    except (ValueError, OSError) as error:
        print(f"render-agents: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
