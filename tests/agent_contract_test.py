#!/usr/bin/env python3
"""Native source/renderer contract tests; all scratch files are project-local."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/render-agents.py"
CANONICAL = ROOT / "ai/codex/agents"
RESTRICTED = {"auditor"}
READ_ONLY_RULES = [{"action": action, "resource": "*", "effect": effect}
                   for action, effect in (("*", "deny"), ("read", "allow"),
                                          ("glob", "allow"), ("grep", "allow"))]
ROUTING_FIELDS = {"model", "model_provider", "model_reasoning_effort"}


def markdown(path):
    _, frontmatter, body = path.read_text().split("---\n", 2)
    metadata = dict(
        (key, json.loads(value))
        for key, value in (line.split(": ", 1) for line in frontmatter.splitlines())
    )
    return metadata, body


class AgentContractTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agent-contract-", dir=ROOT / "tests")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / "source"
        self.source.mkdir()
        self.output = self.base / "output"

    def agent(self, filename="Future.role", /, **fields):
        data = {
            "name": filename, "description": "Research: café # evidence\n",
            "developer_instructions": '\nUse the Task tool in OpenCode.\n"Quotes", \\ paths.\n',
        }
        data.update(fields)
        path = self.source / f"{filename}.toml"
        path.write_text("".join(f"{key} = {json.dumps(value, ensure_ascii=False)}\n"
                                for key, value in data.items()))
        return path

    def run_cli(self, *args, canonical=False):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--source",
             str(CANONICAL if canonical else self.source), *map(str, args)],
            cwd=self.base, capture_output=True, text=True,
        )

    def success(self, result):
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stderr)
        return json.loads(result.stdout)

    def failure(self, result, message):
        self.assertNotEqual(0, result.returncode)
        self.assertIn(message, result.stderr)
        self.assertEqual("", result.stdout)

    def test_default_checks_without_writes(self):
        self.agent()
        before = sorted(self.base.rglob("*"))
        report = self.success(self.run_cli())
        self.assertEqual({"harness": "opencode", "sources": 1, "rendered": 1,
                          "written": 0, "output": None}, report)
        self.assertEqual(before, sorted(self.base.rglob("*")))

    def test_prose_metadata_model_and_idempotence(self):
        source = self.agent(model="gpt-5.2", model_reasoning_effort="high")
        self.success(self.run_cli("--output", self.output))
        path = self.output / "Future.role.md"
        meta, body = markdown(path)
        original = tomllib.loads(source.read_text())
        self.assertEqual(original["developer_instructions"], body)
        self.assertEqual(original["developer_instructions"].encode("utf-8"),
                         path.read_bytes().split(b"---\n", 2)[2])
        self.assertEqual(original["description"], meta["description"])
        self.assertEqual("subagent", meta["mode"])
        self.assertEqual("openai/gpt-5.2#high", meta["model"])
        self.assertNotIn("options", meta)
        before = path.read_bytes()
        self.success(self.run_cli("--output", self.output))
        self.assertEqual(before, path.read_bytes())

    def test_omitted_model_settings_leave_runtime_selection_to_caller(self):
        source = self.agent(sandbox_mode="read-only")
        self.success(self.run_cli("--output", self.output))
        meta, body = markdown(self.output / "Future.role.md")
        self.assertEqual({"description", "mode", "permissions"}, meta.keys())
        self.assertEqual(tomllib.loads(source.read_text())["developer_instructions"], body)
        self.assertEqual(READ_ONLY_RULES,
                         meta["permissions"])

    def test_body_bytes_preserve_crlf_unicode_and_trailing_whitespace(self):
        body = '\r\nUse café evidence.  \r\n\tKeep this whitespace.\n\n'
        self.agent(developer_instructions=body)
        self.success(self.run_cli("--output", self.output))
        rendered = (self.output / "Future.role.md").read_bytes()
        self.assertEqual(body.encode("utf-8"), rendered.split(b"---\n", 2)[2])

    def test_yaml_scalars_preserve_non_bmp_and_yaml_line_breaks(self):
        description = "Research \U0001f52c\u0085with\u2028evidence\u2029today"
        self.agent(description=description)
        self.success(self.run_cli("--output", self.output))
        path = self.output / "Future.role.md"
        # JSON permits paired surrogate escapes; YAML parsers reject them.
        self.assertNotIn("\\ud83d", path.read_text())
        for separator in ("\u0085", "\u2028", "\u2029"):
            self.assertNotIn(separator, path.read_text().split("---\n", 2)[1])
        meta, _ = markdown(path)
        self.assertEqual(description, meta["description"])

    def test_effort_without_model_fails_before_writes(self):
        self.agent(model_reasoning_effort="high")
        self.failure(self.run_cli("--output", self.output), "explicit model")
        self.assertFalse(self.output.exists())

    def test_provider_without_model_cannot_silently_inherit_another_provider(self):
        self.agent(model_provider="openai")
        self.failure(self.run_cli("--output", self.output), "explicit model")
        self.assertFalse(self.output.exists())

    def test_codex_copies_every_source_byte_exact(self):
        source = self.agent(sandbox_mode="read-only")
        other = self.agent("restricted")
        report = self.success(self.run_cli("--harness", "codex",
                                           "--output", self.output))
        self.assertEqual(source.read_bytes(), (self.output / source.name).read_bytes())
        self.assertEqual(other.read_bytes(), (self.output / other.name).read_bytes())
        self.assertNotIn("skipped", report)
        self.assertEqual(2, report["written"])

    def test_removed_policy_flags_are_argument_errors(self):
        self.agent()
        for option in ("--overrides", "--exclusions"):
            result = self.run_cli(option, self.base / "policy.json")
            self.failure(result, "unrecognized arguments")
            self.assertEqual(2, result.returncode)

    def test_read_only_sandbox_maps_to_conservative_opencode_permissions(self):
        source = self.agent(sandbox_mode="read-only", model="gpt-5.2",
                            model_reasoning_effort="high")
        self.agent("ordinary")
        report = self.success(self.run_cli("--output", self.output))
        self.assertEqual(2, report["written"])
        self.assertNotIn("skipped", report)
        meta, body = markdown(self.output / "Future.role.md")
        self.assertEqual(READ_ONLY_RULES,
                         meta["permissions"])
        self.assertEqual("openai/gpt-5.2#high", meta["model"])
        self.assertNotIn("options", meta)
        self.assertEqual(tomllib.loads(source.read_text())["developer_instructions"], body)
        self.assertNotIn("sandbox_mode", meta)
        self.assertNotIn("permissions", markdown(self.output / "ordinary.md")[0])

    def test_semantic_loss_rejected_before_writes(self):
        self.agent("aaa-valid")
        for fields in ({"sandbox_mode": "workspace-write"},
                       {"sandbox_mode": "danger-full-access"},
                       {"sandbox_mode": "read-only", "approval_policy": "on-request"},
                       {"sandbox_mode": "read-only", "nickname_candidates": ["Ada"]},
                       {"approval_policy": "never"},
                       {"nickname_candidates": ["Ada"]}, {"unknown": "value"},
                       {"model_provider": "custom"}, {"model": "custom/model"},
                       {"model_reasoning_effort": "invented"}, {"permission": "deny"}):
            with self.subTest(fields=fields):
                self.agent(**fields)
                self.failure(self.run_cli("--output", self.output), "render-agents:")
                self.assertFalse(self.output.exists())

    def test_empty_or_invalid_sources_rejected(self):
        self.failure(self.run_cli(), "no agents")
        for fields in ({"description": ""}, {"description": " "},
                       {"description": 1}, {"developer_instructions": "\n"},
                       {"name": "../escape"}, {"name": "other"}):
            self.agent(**fields)
            self.failure(self.run_cli(), "render-agents:")
        (self.source / "Future.role.toml").write_text('name = "Future.role"\nname = "duplicate"')
        self.failure(self.run_cli(), "TOML")

    def test_alias_duplicate_and_case_collision_rejected(self):
        self.agent("first", name="second")
        self.agent("second")
        self.failure(self.run_cli(), "filename")
        # Distinct filenames on case-sensitive hosts; dotted/uppercase valid names
        # are tested independently by all Future.role fixtures.

    def test_output_safety_and_preflight_all_targets(self):
        self.agent("aaa-valid")
        self.agent()
        self.failure(self.run_cli("--output", self.source), "source")
        self.failure(self.run_cli("--output", self.source / "nested"), "source")
        self.failure(self.run_cli("--output", self.base), "source")
        self.output.mkdir()
        victim = self.base / "victim"
        victim.write_text("retain")
        (self.output / "Future.role.md").symlink_to(victim)
        self.failure(self.run_cli("--output", self.output), "symlink")
        self.assertEqual("retain", victim.read_text())
        self.assertFalse((self.output / "aaa-valid.md").exists())

    def test_directory_targets_and_symlink_ancestors_rejected(self):
        self.agent()
        self.output.mkdir()
        (self.output / "Future.role.md").mkdir()
        self.failure(self.run_cli("--output", self.output), "regular")
        alias = self.base / "alias"
        alias.symlink_to(self.output, target_is_directory=True)
        self.failure(self.run_cli("--output", alias / "nested"), "symlink")

    def test_atomic_replacement_preserves_other_hardlinks_and_unrelated_files(self):
        self.agent()
        self.output.mkdir()
        victim = self.base / "original"
        victim.write_text("retain original inode")
        target = self.output / "Future.role.md"
        target.hardlink_to(victim)
        unrelated = self.output / "unrelated.txt"
        unrelated.write_text("retain unrelated file")
        self.success(self.run_cli("--output", self.output))
        self.assertEqual("retain original inode", victim.read_text())
        self.assertEqual("retain unrelated file", unrelated.read_text())
        self.assertEqual({target, unrelated}, set(self.output.iterdir()))
        self.assertEqual("subagent", markdown(target)[0]["mode"])

    def test_source_symlinks_rejected(self):
        path = self.agent()
        (self.source / "alias.toml").symlink_to(path)
        self.failure(self.run_cli(), "symlink")

    def test_conflicting_flags_and_help(self):
        self.agent()
        self.failure(self.run_cli("--check", "--output", self.output), "not allowed")
        result = self.run_cli("--help")
        self.assertEqual(0, result.returncode)
        self.assertIn("--harness", result.stdout)

    def test_collection_counts_and_native_byte_copies(self):
        report = self.success(self.run_cli(canonical=True))
        self.assertEqual(5, report["sources"])
        self.assertEqual(5, report["rendered"])
        report = self.success(self.run_cli("--harness", "codex", "--output", self.output,
                                           canonical=True))
        self.assertEqual(5, report["written"])
        self.assertNotIn("skipped", report)
        self.assertEqual({p.name for p in CANONICAL.glob("*.toml")},
                         {p.name for p in self.output.glob("*.toml")})
        for path in self.output.glob("*.toml"):
            self.assertEqual((CANONICAL / path.name).read_bytes(), path.read_bytes())
        for name in RESTRICTED:
            path = self.output / f"{name}.toml"
            self.assertTrue(path.is_file())
            self.assertEqual("read-only", tomllib.loads(path.read_text())["sandbox_mode"])

    def test_security_assessment_preserves_inspection_contract(self):
        data = tomllib.loads((CANONICAL / "auditor.toml").read_text())
        self.assertEqual("read-only", data["sandbox_mode"])
        self.assertIn("apply-infrastructure-standards", data["developer_instructions"])
        self.assertIn("## Read-only scope", data["developer_instructions"])

    def test_collection_policy_and_body_preservation(self):
        rows = []
        for path in sorted(CANONICAL.glob("*.toml")):
            data = tomllib.loads(path.read_text())
            self.assertTrue({"name", "description", "developer_instructions"} <= data.keys())
            self.assertFalse(ROUTING_FIELDS & data.keys(), path.name)
            rows.append(data)
        reviewer = ROOT / "ai/opencode/agents/sprite-artist.md"
        native = {p.stem for p in reviewer.parent.glob("*.md")}
        self.assertEqual({"sprite-artist"}, native)
        self.assertFalse(native & {p.stem for p in CANONICAL.glob("*.toml")})
        self.success(self.run_cli("--output", self.output, canonical=True))
        for name in RESTRICTED:
            meta, _ = markdown(self.output / f"{name}.md")
            self.assertEqual(READ_ONLY_RULES,
                             meta["permissions"])
        meta, _ = markdown(reviewer.parent / "sprite-artist.md")
        self.assertEqual([{"action": action, "resource": "*", "effect": "ask"}
                          for action in ("gpt_imagegen", "shell", "external_directory")], meta["permissions"])
        for data in rows:
            name = data["name"]
            description = data["description"]
            body = data["developer_instructions"]
            meta, rendered_body = markdown(self.output / f"{name}.md")
            self.assertEqual(body, rendered_body)
            expected = {"description": description, "mode": "subagent"}
            if name in RESTRICTED:
                expected["permissions"] = READ_ONLY_RULES
            self.assertEqual(expected, meta)

    def test_runtime_defaults_do_not_override_model_agnostic_subagents(self):
        config = tomllib.loads((ROOT / "ai/codex/config.toml").read_text())
        self.assertTrue(config["agents"]["enabled"])
        self.assertNotIn("default_subagent_model", config["agents"])
        self.assertNotIn("default_subagent_reasoning_effort", config["agents"])
        # Session model selection stays explicit; inheritance is not a router.
        self.assertEqual("gpt-6.1-sol", config["model"])



if __name__ == "__main__":
    unittest.main()
