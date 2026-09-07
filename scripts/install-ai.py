#!/usr/bin/env python3
"""Local AI configuration installer. Requires Python 3.11+, no pip packages.

Managed keys override existing values; other JSON/TOML settings survive.
TOML formatting/comments are normalized, but values (including env references)
are preserved. No login, dependency bootstrap, shell setup, or binary install.
"""
import argparse
import copy
import datetime
import errno
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import TextIO

if sys.version_info < (3, 11):
    sys.exit('install-ai: Python 3.11+ required; use make PYTHON=python3.11')
import tomllib

ROOT = Path(__file__).resolve().parents[1]


class Progress:
    """Track conservative destination outcomes, not a rollback transaction."""

    phase: str = 'preparing sources'
    started: bool = False
    destination_preflight: bool = False
    files: int = 0
    plugins: int = 0
    bundles: int = 0


PROGRESS = Progress()


def say(message: str, output: TextIO | None = None) -> None:
    """Emit flushed, plain ASCII progress without terminal control characters."""
    text = ''.join(char if ' ' <= char <= '~' else ascii(char)[1:-1]
                   for char in message)
    print(text, file=output, flush=True)


def display_path(path: str | Path) -> str:
    """Hide implementation-only staging names from diagnostics."""
    parts = Path(path).parts
    if any(part.startswith(('.ai-', '.render-agent-')) for part in parts):
        return 'agent/file staging'
    return str(path)


def io_error(error: OSError, path: str | Path | None = None) -> str:
    """Describe filesystem failures without platform exception text."""
    category = {errno.ENOENT: 'not found', errno.EACCES: 'permission denied',
                errno.EPERM: 'operation not permitted', errno.ENOTDIR: 'not a directory',
                errno.EISDIR: 'is a directory', errno.ENOSPC: 'no space left',
                errno.EROFS: 'read-only filesystem', errno.EEXIST: 'already exists',
                errno.ELOOP: 'symlink loop'}.get(error.errno or 0, 'I/O failure')
    location = path or error.filename
    return f'{category}: {display_path(location)}' if location else category


def parse_json(text: str, context: str) -> dict:
    """Decode JSON with only numeric error locations exposed."""
    try:
        value = json.loads(text)
    except json.JSONDecodeError as error:
        raise ValueError(f'{context}: invalid JSON at line {error.lineno}, column {error.colno}') from None
    if not isinstance(value, dict):
        raise ValueError(f'{context}: expected a JSON object')
    return value


def operation(argv: list[str]) -> str:
    """Map installer-owned commands to safe operations, never entire argv."""
    if argv[0] == 'codex':
        if argv[1:] == ['--version']:
            return 'checking Codex version'
        if argv[1:4] == ['plugin', 'marketplace', 'list']:
            return 'listing marketplaces'
        if argv[1:4] == ['plugin', 'marketplace', 'add']:
            return 'registering local marketplace'
        if argv[1:3] == ['plugin', 'add'] and re.fullmatch(r'[a-z0-9-]+@[a-z0-9-]+', argv[-1]):
            return f'installing {argv[-1]}'
        return 'listing plugins'
    if argv[0] == 'skills':
        return PROGRESS.phase if PROGRESS.phase.startswith('installing skills bundle ') else 'installing skills'
    return 'checking/rendering agents from ai/codex/agents'


def contains_deny(value):
    return (any(contains_deny(v) for v in value.values())
            if isinstance(value, dict) else value == 'deny')


def merge(old, new, path=()):
    result = copy.deepcopy(old)
    for key, value in new.items():
        if key == 'permission' and result.get(key) == 'deny':
            continue
        if 'permission' in path and contains_deny(result.get(key)) and not isinstance(value, dict):
            continue
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            previous = result[key]
            if path in (('mcp',), ('mcp_servers',)):
                previous = clean_mcp_fields(previous, value)
            result[key] = merge(previous, value, (*path, key))
        else:
            result[key] = copy.deepcopy(value)
    if 'permission' in path:
        # Restore managed rule order: default namespace rules precede exact
        # exceptions. Only retained custom denies belong after those exceptions.
        for key in new:
            result[key] = result.pop(key)
        for key, value in old.items():
            if contains_deny(value) and (key not in new or value != new[key]):
                result[key] = result.pop(key)
    return result


def clean_mcp_fields(old, new):
    """Keep server-independent settings, not obsolete transport/process fields."""
    old = copy.deepcopy(old)
    local_fields = ('command', 'args', 'environment', 'env', 'env_vars', 'cwd')
    remote_fields = ('url', 'headers', 'http_headers', 'env_http_headers',
                     'bearer_token_env_var', 'oauth')
    if new.get('type') == 'remote' or 'url' in new:
        for key in local_fields:
            old.pop(key, None)
        if 'url' in new and new['url'] != old.get('url'):
            for key in remote_fields:
                old.pop(key, None)
    elif new.get('type') == 'local' or 'command' in new:
        for key in remote_fields:
            old.pop(key, None)
        if 'command' in new and new['command'] != old.get('command'):
            for key in local_fields:
                old.pop(key, None)
    # Managed process environment is an atomic map, not an accumulation of
    # obsolete credentials/settings across server implementations.
    for key in ('environment', 'env', 'env_vars'):
        if key in new:
            old.pop(key, None)
    return old


def check_github_token(config, environment):
    for table in ('mcp', 'mcp_servers'):
        github = config.get(table, {}).get('github', {})
        if not isinstance(github, dict) or github.get('enabled') is False:
            continue
        header = github.get('headers', {}).get('Authorization', '')
        required = (github.get('bearer_token_env_var') == 'GITHUB_MCP_TOKEN' or
                    ('Bearer' in header and '{env:GITHUB_MCP_TOKEN}' in header))
        if required and not environment.get('GITHUB_MCP_TOKEN', '').strip():
            raise ValueError('GITHUB_MCP_TOKEN is required for enabled GitHub MCP; export it securely before installing (value is never printed or copied)')


def toml_value(value):
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False).replace('\x7f', '\\u007f')
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value).lower()
    if isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
        return value.isoformat()
    if isinstance(value, list):
        return '[' + ', '.join(toml_value(v) for v in value) + ']'
    if isinstance(value, dict):
        return '{ ' + ', '.join(f'{toml_value(k)} = {toml_value(v)}' for k, v in value.items()) + ' }'
    raise ValueError('unsupported TOML value')


def toml_dump(value):
    lines = []
    def table(data, path):
        if path:
            lines.append('[' + '.'.join(toml_value(k) for k in path) + ']')
        for key, val in data.items():
            if not isinstance(val, dict):
                lines.append(f'{toml_value(key)} = {toml_value(val)}')
        for key, val in data.items():
            if isinstance(val, dict):
                table(val, [*path, key])
    table(value, [])
    text = '\n'.join(lines) + '\n'
    tomllib.loads(text)
    return text


def write_managed(path, content):
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
        raise ValueError(f'managed file is a symlink: {path}; resolve manually')
    if path.exists() and path.read_bytes() == content:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        shutil.copy2(path, path.with_name(path.name + '.backup.' + stamp))
    # Same-directory atomic replacement, private permissions even for new files.
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.ai-', delete=False) as stream:
        stage = Path(stream.name)
        try:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
            stage.replace(path)
        finally:
            stage.unlink(missing_ok=True)


def with_native_backup(path, operation):
    """Retain pre-command config if the native CLI changes it, even on failure."""
    before = path.read_bytes() if path.exists() else None
    try:
        return operation()
    finally:
        after = path.read_bytes() if path.exists() else None
        if before is not None and before != after:
            stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            write_managed(path.with_name(path.name + '.backup.' + stamp), before)


def local_plugins(root, manifest):
    name = manifest['name']
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', name):
        raise ValueError('invalid marketplace name')
    result, names, skills = [], set(), set()
    for entry in manifest['plugins']:
        source = entry['source']
        if source.get('source') != 'local':
            raise ValueError('only checkout-local plugin sources are allowed')
        path = (root / source['path']).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError('plugin source escapes checkout')
        plugin = load_config(path / '.codex-plugin/plugin.json')
        plugin_name = plugin['name']
        if plugin_name != entry['name'] or plugin_name in names:
            raise ValueError('plugin identifiers mismatch or duplicate')
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', plugin_name):
            raise ValueError('invalid plugin name')
        if entry.get('policy', {}).get('authentication') != 'ON_USE':
            raise ValueError('plugins must not request install-time authentication')
        if plugin.get('skills') != './skills/':
            raise ValueError('plugin skills must be local ./skills/')
        found = list((path / 'skills').glob('*/SKILL.md'))
        if not found:
            raise ValueError(f'no local skills for {plugin_name}')
        for file in path.rglob('*'):
            if file.is_symlink():
                raise ValueError(f'plugin symlinks are not copy-safe: {file}')
        for file in found:
            frontmatter = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', file.read_text(), re.DOTALL)
            if not frontmatter:
                raise ValueError(f'missing skill frontmatter: {file.parent.name}')
            names_in_header = re.findall(r'^name:\s*[\"\']?([a-z0-9-]+)[\"\']?\s*$', frontmatter[1], re.MULTILINE)
            if names_in_header != [file.parent.name]:
                raise ValueError(f'skill name must match local directory: {file.parent.name}')
            if file.parent.name in skills:
                raise ValueError(f'duplicate skill: {file.parent.name}')
            skills.add(file.parent.name)
        names.add(plugin_name)
        result.append((plugin_name, path))
    if len(result) != 4:
        raise ValueError('expected four plugin manifests')
    return result


def run(argv):
    env = dict(os.environ, DISABLE_TELEMETRY='1', DO_NOT_TRACK='1')
    label = operation(argv)
    try:
        result = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True,
                                text=True, errors='replace')
    except OSError as error:
        raise ValueError(f'{label}: {io_error(error)}') from None
    if result.returncode:
        # Avoid echoing harness errors which may contain credential values.
        raise ValueError(f'{label}: exit status {result.returncode}; inspect configuration locally')
    return result.stdout


def check_registration(root, name, listing):
    matches = [row for row in listing['marketplaces'] if row['name'] == name]
    for row in matches:
        source = row.get('marketplaceSource')
        if Path(row['root']).resolve() != root.resolve() or (source and (
                source.get('sourceType') != 'local' or Path(source.get('source', '')).resolve() != root.resolve())):
            raise ValueError(f'marketplace {name} source clash; inspect codex plugin marketplace list and remove/re-register manually')
    if len(matches) > 1:
        raise ValueError(f'duplicate marketplace {name}; resolve registrations manually')


def render_agents(staging, execute=run, output=None, *, harness='opencode'):
    """Expose the renderer's actual counts, never inferred availability."""
    summary = parse_json(execute([sys.executable, str(ROOT / 'scripts/render-agents.py'),
                                 '--harness', harness, '--output', str(staging)]),
                         f'renderer CLI JSON for {harness}')
    if summary.get('harness') != harness or any(
            type(summary.get(key)) is not int or summary[key] < 0
            for key in ('sources', 'rendered', 'written')):
        raise ValueError(f'invalid renderer CLI JSON counts for {harness}')
    say(f"Prepared {harness} agents: {summary['sources']} sources, "
        f"{summary['rendered']} rendered, {summary['written']} staged.", output)
    return summary


def check_prompt_conflicts(old, source):
    permissions = source.get('permission', {})
    guarded = {key[:-1]: value for key, value in permissions.items()
               if key.endswith('_*') and value in ('ask', 'deny')}
    reads = {key for key, value in permissions.items()
             if value == 'allow' and not re.search(r'[*?\[]', key)}
    def overlaps(pattern, prefix):
        literal = re.split(r'[*?\[]', pattern, maxsplit=1)[0]
        return literal.startswith(prefix) or prefix.startswith(literal)
    def permits(value, default):
        if isinstance(value, dict):
            return any(permits(v, default) for v in value.values())
        return value == 'allow' or value is True or (default == 'deny' and value == 'ask')
    def check_permission(value):
        if isinstance(value, dict):
            # A bare/trailing namespace deny may be a deliberate custom block,
            # not our default-before-exceptions policy. Never guess its origin.
            order = list(value)
            for prefix, default in guarded.items():
                pattern = prefix + '*'
                if default == 'deny' and value.get(pattern) == 'deny':
                    if any(name not in value or order.index(name) < order.index(pattern)
                           for name in reads if name.startswith(prefix)):
                        return True
            return any(key not in reads and overlaps(key, prefix) and permits(action, default)
                       for key, action in value.items() for prefix, default in guarded.items())
        return any(permits(value, default) for default in guarded.values())
    conflict = check_permission(old.get('permission', {}))
    for agent in old.get('agent', {}).values():
        if isinstance(agent, dict):
            conflict |= check_permission(agent.get('permission', {}))
            conflict |= check_permission(agent.get('tools', {}))
    for name, settings in source.get('mcp_servers', {}).items():
        if settings.get('default_tools_approval_mode') != 'prompt':
            continue
        existing = old.get('mcp_servers', {}).get(name, {})
        conflict |= existing.get('default_tools_approval_mode', 'prompt') != 'prompt'
        if 'enabled_tools' in settings and 'enabled_tools' in existing:
            conflict |= not set(existing['enabled_tools']) <= set(settings['enabled_tools'])
        for tool_name, tool in existing.get('tools', {}).items():
            if isinstance(tool, dict) and tool.get('enabled') is not False:
                # Codex disables tools with enabled=false, not approval_mode=deny.
                # Reject unsupported values rather than replacing a custom block.
                allowed = {'prompt'}
                if settings.get('tools', {}).get(tool_name, {}).get('approval_mode') == 'approve':
                    allowed.add('approve')
                conflict |= tool.get('approval_mode', 'prompt') not in allowed
    if conflict:
        raise ValueError('existing managed MCP prompt-rule conflict; reconcile OpenCode permission/agent overrides or Codex mcp_servers default_tools_approval_mode/tool approval_mode settings manually before installing. Values are not printed.')
    for profile in old.get('profiles', {}).values():
        if isinstance(profile, dict):
            check_prompt_conflicts(profile, source)


def check_plugins(root, name, plugins, execute=run):
    listing = parse_json(execute(['codex', 'plugin', 'marketplace', 'list', '--json']),
                         'CLI JSON while listing marketplaces')
    try:
        check_registration(root, name, listing)
    except (KeyError, TypeError, AttributeError):
        raise ValueError('invalid CLI JSON structure while listing marketplaces') from None
    current = parse_json(execute(['codex', 'plugin', 'list', '--marketplace', name, '--json', '--available']),
                         'CLI JSON while listing plugins')
    expected = {f'{p}@{name}': path.resolve() for p, path in plugins}
    try:
        for row in current['installed'] + current['available']:
            if row['pluginId'] in expected:
                source = row['source']
                if source.get('source') != 'local' or Path(source['path']).resolve() != expected[row['pluginId']]:
                    raise ValueError('installed plugin source clash; resolve manually before installing')
    except (KeyError, TypeError, AttributeError):
        raise ValueError('invalid CLI JSON structure while listing plugins') from None


def install_plugins(root, name, plugins, execute=run):
    check_plugins(root, name, plugins, execute)
    PROGRESS.phase = 'registering local marketplace'
    say(f'Registering local marketplace {name}: {root}')
    execute(['codex', 'plugin', 'marketplace', 'add', str(root)])
    say(f'Registered local marketplace {name}.')
    # Native add refreshes local cached content as well as enabling registration.
    for plugin, _ in plugins:
        PROGRESS.phase = f'installing {plugin}@{name}'
        say(f'Installing {plugin}@{name}...')
        execute(['codex', 'plugin', 'add', f'{plugin}@{name}'])
        PROGRESS.plugins += 1
        say(f'Installed plugin {plugin}@{name}.')


def install_skills(plugins, execute=run):
    for name, path in plugins:
        PROGRESS.phase = f'installing skills bundle {name}'
        say(f'Installing skills bundle {name}...')
        execute(['skills', 'add', str(path / 'skills'), '--agent', 'opencode', '--global', '--copy', '--yes'])
        PROGRESS.bundles += 1
        say(f'Installed skills bundle {name}.')


def check_skill_copies(plugins, target):
    """Refuse CLI copy if its directory replacement would delete custom files."""
    backups = []
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    for _, plugin in plugins:
        for skill in (plugin / 'skills').glob('*/SKILL.md'):
            source = skill.parent
            destination = target / 'skills' / source.name
            if any(p.is_symlink() for p in [destination, *destination.parents]):
                raise ValueError(f'skill destination uses a symlink: {destination}; resolve manually')
            for old in destination.rglob('*'):
                relative = old.relative_to(destination)
                new = source / relative
                if old.is_symlink() or not new.exists() or old.is_dir() != new.is_dir():
                    raise ValueError(f'skill copy would replace or remove an unmanaged asset: {old}; inspect the destination before installing')
                if old.is_file() and old.read_bytes() != new.read_bytes():
                    backups.append((target / '.install-ai-backups' / stamp / 'skills' / source.name / relative,
                                    old.read_bytes()))
    return backups


def load_config(path):
    if not path.exists():
        return {}
    try:
        text = path.read_text()
        return (tomllib.loads(text) if path.suffix == '.toml'
                else parse_json(text, f'configuration {display_path(path)}'))
    except tomllib.TOMLDecodeError as error:
        # Python 3.11 includes config keys in some messages. Only use the
        # anchored parser-generated location suffix, never the message body.
        location = re.search(r'\(at (line [0-9]+, column [0-9]+|end of document)\)\Z', str(error))
        suffix = f' at {location[1]}' if location else ''
        raise ValueError(f'configuration {display_path(path)}: invalid TOML{suffix}') from None
    except UnicodeError:
        raise ValueError(f'configuration {display_path(path)}: invalid text encoding') from None
    except OSError as error:
        raise ValueError(f'reading configuration: {io_error(error, path)}') from None


def config_bytes(path, source):
    old, managed = load_config(path), load_config(source)
    check_prompt_conflicts(old, managed)
    data = merge(old, managed)
    return (toml_dump(data) if source.suffix == '.toml' else json.dumps(data, indent=2) + '\n').encode()


def check_agent_sources(root):
    """Keep generated and native source names disjoint on every platform."""
    names = set()
    native = sorted((root / 'ai/opencode/agents').glob('*.md'))
    for file in [*sorted((root / 'ai/codex/agents').glob('*.toml')), *native]:
        if file.is_symlink() or any(parent.is_symlink() for parent in file.parents):
            raise ValueError(f'agent source uses a symlink: {file}')
        if not file.is_file():
            raise ValueError(f'not a regular agent source: {file}')
        name = file.stem.casefold()
        if name in names:
            raise ValueError(f'agent source filename collision: {file.name}')
        names.add(name)
    return native


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', choices=['all', 'codex', 'opencode', 'validate'])
    args = parser.parse_args()
    PROGRESS.phase = 'checking prerequisites'
    targets = ['codex', 'opencode'] if args.target in ('all', 'validate') else [args.target]
    if args.target != 'validate':
        say('Checking installer prerequisites...')
        dependencies = (['codex'] if 'codex' in targets else []) + (['skills'] if 'opencode' in targets else [])
        for tool in dependencies:
            if not shutil.which(tool):
                raise ValueError(f'{tool} is required on PATH; install it explicitly (no network bootstrap)')
        if 'codex' in targets and run(['codex', '--version']).strip() != 'codex-cli 0.153.4':
            raise ValueError('Codex 0.153.4 required for this installer contract')
    PROGRESS.phase = 'preparing sources'
    native_agents = check_agent_sources(ROOT)
    manifest = load_config(ROOT / '.agents/plugins/marketplace.json')
    plugins = local_plugins(ROOT, manifest)
    plans = []
    inventories = []
    skill_backups = []
    home = Path.home()
    codex_home = Path(os.environ.get('CODEX_HOME', home / '.codex'))
    common_instructions = ROOT / 'ai/AGENTS.md'
    if not common_instructions.is_file():
        raise ValueError('missing required source: ai/AGENTS.md')
    instructions = common_instructions.read_bytes()
    for harness in targets:
        PROGRESS.phase = f'preparing {harness}'
        source = ROOT / 'ai' / harness
        target = (codex_home if harness == 'codex' else
                  Path(os.environ.get('XDG_CONFIG_HOME', home / '.config')) / 'opencode')
        if not target.is_absolute():
            raise ValueError('CODEX_HOME and XDG_CONFIG_HOME must be absolute paths when set')
        filename = 'config.toml' if harness == 'codex' else 'opencode.json'
        required = [source / filename,
                    ROOT / 'scripts/render-agents.py']
        if harness == 'codex':
            required += [source / 'astra.config.toml']
        else:
            required += [source / 'agents/ralph-reviewer.md']
        for file in required:
            if not file.is_file():
                raise ValueError(f'missing required source: {file.relative_to(ROOT)}')
        for file in source.rglob('*'):
            if file.suffix in ('.json', '.toml'):
                load_config(file)
        if harness == 'opencode' and (target / 'opencode.jsonc').exists() and args.target != 'validate':
            raise ValueError('opencode.jsonc already exists; reconcile it with opencode.json manually before installing')
        for file in [source / filename, *sorted(source.glob('*.config.toml')),
                     *sorted(source.glob('tui.json')), *sorted(source.glob('astra.json'))]:
            if args.target != 'validate':
                check_prompt_conflicts(load_config(target / file.name), load_config(source / filename))
            content = file.read_bytes() if args.target == 'validate' else config_bytes(target / file.name, file)
            if args.target != 'validate':
                data = tomllib.loads(content.decode()) if file.suffix == '.toml' else json.loads(content)
                check_github_token(data, os.environ)
            plans.append((target / file.name, content))
        plans.append((target / 'AGENTS.md', instructions))
        if harness == 'opencode':
            if args.target != 'validate':
                skill_backups = check_skill_copies(plugins, target)
            for file in native_agents:
                plans.append((target / 'agents' / file.name, file.read_bytes()))
            for folder in ('commands',):
                for file in sorted((source / folder).rglob('*')):
                    if file.is_file():
                        plans.append((target / folder / file.relative_to(source / folder), file.read_bytes()))
        if args.target != 'validate':
            say(f'Managed scope: {target} - config keys are merged; AGENTS.md and same-name shipped agents/commands are replaced with backups when changed. Unrelated files remain.', sys.stderr)
        # Parse canonical TOML locally for safe file/line errors even when only
        # the OpenCode target is selected; renderer diagnostics stay private.
        for file in sorted((ROOT / 'ai/codex/agents').glob('*.toml')):
            load_config(file)
        run([sys.executable, str(ROOT / 'scripts/render-agents.py'),
             '--harness', harness, '--check'])
        if args.target != 'validate':
            with tempfile.TemporaryDirectory(prefix='.ai-render-', dir=ROOT) as staging:
                summary = render_agents(staging, harness=harness)
                suffix = '*.toml' if harness == 'codex' else '*.md'
                generated = sorted(Path(staging).rglob(suffix))
                if not generated:
                    raise ValueError(f'agent renderer produced no {harness} definitions')
                if len(generated) != summary['written'] or summary['rendered'] != len(generated):
                    raise ValueError(f'agent renderer count mismatch for {harness}')
                for file in generated:
                    if harness == 'codex':
                        load_config(file)
                    plans.append((target / 'agents' / file.relative_to(staging),
                                  file.read_bytes()))
            native_count = len(native_agents) if harness == 'opencode' else 0
            commands = sum(path.is_relative_to(target / 'commands') for path, _ in plans)
            inventories.append((target, len(generated), native_count, commands))
    if args.target == 'validate':
        say('AI sources valid (local structure and JSON/TOML syntax; no harness or MCP started).')
        return
    PROGRESS.phase = 'preflighting destinations'
    # Preflight managed destinations before any config writes.
    for path, _ in plans:
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
            raise ValueError(f'managed destination uses a symlink: {path}; resolve manually')
    if 'codex' in targets:
        PROGRESS.destination_preflight = True
        codex_home.mkdir(parents=True, exist_ok=True)
        PROGRESS.phase = 'checking local plugin registrations'
        check_plugins(ROOT, manifest['name'], plugins)
    for path, _ in plans:
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
            raise ValueError(f'managed destination uses a symlink: {path}; resolve manually')
    for path, content in plans:
        PROGRESS.phase = f'writing {display_path(path)}'
        PROGRESS.started = True
        write_managed(path, content)
        PROGRESS.files += 1
        if path.name == 'AGENTS.md' or path.parent in [item[0] for item in inventories]:
            say(f'Installed config/policy: {path}')
    for target, rendered, native, commands in inventories:
        say(f'Installed files in {target}: {rendered + native} agents '
            f'({rendered} rendered + {native} native), {commands} commands.')
    if 'codex' in targets:
        PROGRESS.phase = f'installing Codex plugins; config {codex_home / "config.toml"}'
        with_native_backup(codex_home / 'config.toml',
                           lambda: install_plugins(ROOT, manifest['name'], plugins))
    if 'opencode' in targets:
        for path, content in skill_backups:
            PROGRESS.phase = f'backing up skill asset {display_path(path)}'
            write_managed(path, content)
        install_skills(plugins)
    say(f'Completed {PROGRESS.plugins} plugins and {PROGRESS.bundles} skill bundles.')
    say('AI configuration installed. Restart the selected harness. No authentication performed.')


def cli() -> int:
    """Report safe errors and conservative partial outcomes at the CLI boundary."""
    global PROGRESS
    PROGRESS = Progress()
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        # Source/config parse errors can contain secrets. Do not print raw values.
        if type(error) is ValueError:
            detail = str(error)
        elif isinstance(error, OSError):
            detail = io_error(error)
        else:
            detail = 'invalid configuration or CLI response structure; inspect locally'
        say(f'install-ai: {PROGRESS.phase}: {detail}', sys.stderr)
        if PROGRESS.started:
            say(f'Partial installation: earlier changes may remain. Completed '
                f'{PROGRESS.files} managed files, {PROGRESS.plugins} plugins, '
                f'{PROGRESS.bundles} skill bundles. The failing operation may also have changed files; no automatic rollback.', sys.stderr)
        elif PROGRESS.destination_preflight:
            say('No managed-file writes or plugin/skill installation started. '
                'Destination preflight may have created directories or CLI state.', sys.stderr)
        else:
            say('No destination writes or plugin/skill installation started.', sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(cli())
