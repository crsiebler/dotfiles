"""Independent MCP contracts; no installer imports, downloads, or live servers.

Run: python3.11 -m unittest discover -s tests -p 'mcp_configuration_test.py' -v
Native checks skip explicitly when Codex/Zsh is unavailable. Strict-mode checks
skip when the installed CLI explicitly rejects strict mode for MCP listing.
All subprocesses
start with an allowlisted environment and scratch HOME beneath tests/.

Schema evidence reviewed 2026-09-05:
https://opencode.ai/config.json ($defs.McpLocalConfig, McpRemoteConfig,
Config.properties.lsp): lsp accepts boolean (including true) or an object.
https://raw.githubusercontent.com/openai/codex/rust-v0.153.4/
codex-rs/core/config.schema.json; installed version is checked at runtime and
native parsing is preferred; 0.153.4 explicitly rejects strict mode for MCP.
The versioned field projection below covers unknown MCP keys in that release.
These are focused contracts, not a complete JSON Schema implementation.
"""

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from urllib.parse import parse_qs, urlsplit
import uuid


ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / 'ai/codex/config.toml'
OPENCODE = ROOT / 'ai/opencode/opencode.json'
EXAMPLE = ROOT / 'env/.env.example'
GLOBAL = {'github', 'exa', 'context7'}
OPT_IN = {'jira', 'postgresql'}
POSTGRESQL_PATH = (
    '/Repositories/mcp-suite/servers/postgresql/dist/servers/postgresql/src/index.js'
)
# RawMcpServerConfig.properties in the versioned Codex schema cited above.
# Keep this offline projection versioned, not inferred from the config under test.
CODEX_SCHEMA_VERSION = '0.153.4'
CODEX_MCP_FIELDS = set('''
    args auth bearer_token_env_var command cwd default_tools_approval_mode
    disabled_tools enabled enabled_tools env env_http_headers env_vars
    environment_id http_headers http_headers_helper name oauth oauth_resource
    omit_tools_from required scopes startup_timeout_ms startup_timeout_sec
    supports_parallel_tool_calls tool_timeout_sec tools url
'''.split())


class MCPConfigurationTest(unittest.TestCase):
    def setUp(self):
        self.codex = tomllib.loads(CODEX.read_text())
        self.opencode = json.loads(OPENCODE.read_text())
        self.servers = {
            'codex': self.codex['mcp_servers'],
            'opencode': self.opencode['mcp'],
        }
        scratch = tempfile.TemporaryDirectory(prefix='mcp-contract-',
                                               dir=ROOT / 'tests')
        self.addCleanup(scratch.cleanup)
        self.scratch = Path(scratch.name)
        for name in ('home', 'codex', 'bin', 'xdg', 'cache', 'data', 'tmp'):
            (self.scratch / name).mkdir()
        # No inherited tokens, AWS configuration, proxy settings or shell hooks.
        self.env = {
            'HOME': str(self.scratch / 'home'),
            'CODEX_HOME': str(self.scratch / 'codex'),
            'XDG_CONFIG_HOME': str(self.scratch / 'xdg'),
            'XDG_CACHE_HOME': str(self.scratch / 'cache'),
            'XDG_DATA_HOME': str(self.scratch / 'data'),
            'TMPDIR': str(self.scratch / 'tmp'),
            'PATH': str(self.scratch / 'bin'),
            'LC_ALL': 'C',
        }

    def run_isolated(self, argv, extra=None):
        try:
            return subprocess.run(
                argv, env=self.env | (extra or {}), cwd=self.scratch,
                stdin=subprocess.DEVNULL, capture_output=True, text=True,
                timeout=20,
            )
        except subprocess.TimeoutExpired:
            self.fail('isolated subprocess timed out (output withheld)')

    def test_only_global_connections_are_enabled(self):
        for harness, servers in self.servers.items():
            with self.subTest(harness=harness):
                self.assertTrue((GLOBAL | OPT_IN) <= servers.keys())
                self.assertFalse({'aws', 'elastic'} & servers.keys())
                self.assertEqual({n for n, s in servers.items()
                                  if s.get('enabled') is True}, GLOBAL)
                for name, server in servers.items():
                    self.assertIs(type(server.get('enabled')), bool, name)
                    if name not in GLOBAL:
                        self.assertIs(server['enabled'], False, name)

    def test_codex_mcp_fields_match_versioned_schema(self):
        for name, server in self.servers['codex'].items():
            with self.subTest(server=name):
                self.assertFalse(server.keys() - CODEX_MCP_FIELDS,
                                 f'{name}: unsupported MCP fields in Codex '
                                 f'{CODEX_SCHEMA_VERSION} schema')
                self.assertNotEqual('command' in server, 'url' in server,
                                    'exactly one transport is required')
                for field in ('env', 'env_http_headers', 'http_headers'):
                    values = server.get(field, {})
                    self.assertIsInstance(values, dict)
                    self.assertTrue(all(isinstance(v, str) for v in values.values()))

    def test_remote_endpoints_and_exact_toolsets(self):
        endpoints = {
            'github': 'https://api.githubcopilot.com/mcp/',
            'context7': 'https://mcp.context7.com/mcp',
            'jira': 'https://mcp.atlassian.com/v2/mcp',
        }
        for harness, servers in self.servers.items():
            with self.subTest(harness=harness):
                for name, url in endpoints.items():
                    self.assertTrue(servers[name]['url'] == url,
                                    f'{name}: endpoint changed (value withheld)')
                headers = servers['github'].get(
                    'http_headers', servers['github'].get('headers'))
                self.assertEqual(headers['X-MCP-Toolsets'],
                                 'repos,issues,pull_requests')
                exa = urlsplit(servers['exa']['url'])
                self.assertEqual((exa.scheme, exa.netloc, exa.path),
                                 ('https', 'mcp.exa.ai', '/mcp'))
                self.assertEqual(parse_qs(exa.query), {'tools': [
                    'web_search_exa,web_fetch_exa,agent_run,web_search_advanced_exa'
                ]})

    def test_authorization_prompts_cannot_be_overridden(self):
        self.assertEqual(self.codex['approval_policy'], 'on-request')
        for name in {'github'} | OPT_IN:
            with self.subTest(server=name):
                server = self.servers['codex'][name]
                self.assertEqual(server['default_tools_approval_mode'], 'prompt')
                permissions = self.opencode['permission']
                self.assertEqual(permissions[name + '_*'], 'ask')
                # Exact read exceptions and negative write controls are covered
                # independently in mcp_permissions_test.py.

    def test_credentials_are_environment_references(self):
        expected = {
            'github': {'Authorization': 'Bearer {env:GITHUB_MCP_TOKEN}',
                       'X-MCP-Toolsets': 'repos,issues,pull_requests'},
            'context7': {'CONTEXT7_API_KEY': '{env:CONTEXT7_API_KEY}'},
            'exa': {'x-api-key': '{env:EXA_API_KEY}'},
        }
        c = self.servers['codex']
        self.assertTrue(c['github']['bearer_token_env_var'] == 'GITHUB_MCP_TOKEN')
        for name, headers in expected.items():
            with self.subTest(server=name):
                self.assertTrue(self.servers['opencode'][name]['headers'] == headers,
                                'headers must contain references, not credentials')
                if name != 'github':
                    refs = {key: value[5:-1] for key, value in headers.items()}
                    self.assertTrue(c[name]['env_http_headers'] == refs,
                                    'Codex headers must name environment variables')
                self.assertTrue(c[name].get('http_headers', {}) == (
                    {'X-MCP-Toolsets': 'repos,issues,pull_requests'}
                    if name == 'github' else {}), 'unexpected literal headers')
        self.assertIs(self.servers['opencode']['github']['oauth'], False)
        for harness, servers in self.servers.items():
            for name, server in servers.items():
                with self.subTest(harness=harness, server=name):
                    self.assertNotIn('bearer_token', server)
                    for key, value in server.get('environment',
                                                 server.get('env', {})).items():
                        allowed = {'ELEVENLABS_MCP_OUTPUT_MODE': 'files'}
                        self.assertTrue(value == allowed.get(key) or
                                        re.fullmatch(r'\{env:[A-Z_]+\}', value)
                                        is not None,
                                        f'{name}.{key}: unexpected literal env value')
                    if 'url' in server:
                        url = urlsplit(server['url'])
                        self.assertIsNone(url.username)
                        self.assertIsNone(url.password)

    def test_environment_example_is_blank_and_zsh_syntax_valid(self):
        names = []
        for number, line in enumerate(EXAMPLE.read_text().splitlines(), 1):
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            match = re.fullmatch(r'export ([A-Z][A-Z0-9_]*)=', line)
            if match is None:
                self.fail(f'line {number}: expected blank export')
            names.append(match[1])
        self.assertEqual(len(names), len(set(names)))
        self.assertTrue({
            'GITHUB_MCP_TOKEN', 'EXA_API_KEY', 'CONTEXT7_API_KEY',
            'POSTGRESQL_CONNECTION_STRING',
        } <= set(names))
        self.assertFalse({
            'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_PROFILE',
            'AWS_REGION', 'ELASTIC_MCP_URL', 'ELASTIC_MCP_AUTHORIZATION',
        } & set(names))
        zsh = shutil.which('zsh')
        if not zsh:
            self.skipTest('zsh unavailable; blank export checks completed')
        result = self.run_isolated([zsh, '-f', '-n', str(EXAMPLE)])
        self.assertEqual(result.returncode, 0, 'zsh -n failed; output withheld')

    def postgresql_launcher(self, harness, secret):
        server = self.servers[harness]['postgresql']
        if harness == 'codex':
            self.assertEqual(server['command'], 'sh')
            self.assertEqual(server['args'], [
                '-c', f'exec node "$HOME{POSTGRESQL_PATH}"',
            ])
            self.assertEqual(server['env_vars'],
                             ['HOME', 'POSTGRESQL_CONNECTION_STRING'])
            return ['/bin/sh', *server['args']], {
                key: value for key, value in {
                    'HOME': self.env['HOME'],
                    'POSTGRESQL_CONNECTION_STRING': secret,
                }.items() if key in server['env_vars']
            }
        self.assertEqual(server['command'],
                         ['node', '{env:HOME}' + POSTGRESQL_PATH])
        self.assertEqual(server['environment'], {
            'POSTGRESQL_CONNECTION_STRING': '{env:POSTGRESQL_CONNECTION_STRING}',
        })
        # Model only these known substitutions, not OpenCode's config loader.
        command = [arg.replace('{env:HOME}', self.env['HOME'])
                   for arg in server['command']]
        environment = {
            key: value.replace('{env:POSTGRESQL_CONNECTION_STRING}', secret)
            for key, value in server['environment'].items()
        }
        return command, environment

    def fake_executable(self, name):
        capture = self.scratch / (name + '.json')
        fake = self.scratch / 'bin' / name
        fake.write_text(
            f'#!{sys.executable}\n'
            'import json, os, sys\n'
            f'with open({str(capture)!r}, "w") as stream:\n'
            '    json.dump({"argv": sys.argv[1:], "env": dict(os.environ)}, stream)\n'
            'sys.exit(int(os.environ.get("FAKE_EXIT", "0")))\n'
        )
        fake.chmod(0o700)
        return capture

    def test_postgresql_launcher_secret_transport_and_exit_status(self):
        home = self.scratch / 'home with spaces ;$(not-a-command)&\'"*'
        home.mkdir()
        self.env['HOME'] = str(home)
        capture = self.fake_executable('node')
        # Generated sentinel, not a committed credential; shell metacharacters
        # exercise quoting without pointing at a reachable database.
        secret = 'postgresql://fixture:' + uuid.uuid4().hex + (
            ' ;$()&@database.invalid/fixture?sslmode=require')
        for harness in self.servers:
            for status in (0, 23):
                with self.subTest(harness=harness, status=status):
                    capture.unlink(missing_ok=True)
                    command, environment = self.postgresql_launcher(harness, secret)
                    result = self.run_isolated(command, {
                        **environment, 'FAKE_EXIT': str(status),
                    })
                    self.assertEqual(result.returncode, status)
                    self.assertTrue(capture.exists(), 'fake node was not called')
                    record = json.loads(capture.read_text())
                    self.assertTrue(
                        record['env'].get('POSTGRESQL_CONNECTION_STRING') == secret,
                        'connection string passthrough incorrect (value withheld)')
                    self.assertEqual(record['env']['HOME'], str(home))
                    self.assertTrue('DATABASE_URI' not in record['env'],
                                    'obsolete DATABASE_URI mapping present')
                    self.assertTrue(all(secret not in arg
                                        for arg in command + record['argv']),
                                    'secret leaked to launcher argv')
                    self.assertTrue(secret not in result.stdout + result.stderr,
                                    'secret leaked to launcher output')
                    self.assertTrue(record['argv'] == [str(home) + POSTGRESQL_PATH],
                                    'node argv/path incorrect (values withheld)')

    def test_postgresql_launchers_fail_without_node_without_leaking_secret(self):
        secret = 'fixture-' + uuid.uuid4().hex
        for harness in self.servers:
            with self.subTest(harness=harness):
                command, environment = self.postgresql_launcher(harness, secret)
                if harness == 'opencode':
                    with self.assertRaises(FileNotFoundError) as raised:
                        self.run_isolated(command, environment)
                    self.assertTrue(secret not in str(raised.exception))
                else:
                    result = self.run_isolated(command, environment)
                    self.assertEqual(result.returncode, 127)
                    self.assertEqual(result.stdout, '')
                    self.assertTrue(secret not in result.stderr,
                                    'secret leaked to launcher error')

    def test_opencode_published_schema_mcp_shapes_and_lsp(self):
        # Offline focused projection of published schema; never bootstrap OpenCode.
        lsp = self.opencode.get('lsp', False)
        self.assertIn(type(lsp), (bool, dict),
                      'published OpenCode schema accepts boolean or object lsp')
        for name, server in self.servers['opencode'].items():
            with self.subTest(server=name):
                kind = server['type']
                self.assertIn(kind, ('local', 'remote'))
                allowed = {'type', 'enabled', 'timeout'} | (
                    {'command', 'cwd', 'environment'} if kind == 'local'
                    else {'url', 'headers', 'oauth'})
                self.assertFalse(server.keys() - allowed)
                if kind == 'local':
                    self.assertIsInstance(server['command'], list)
                    self.assertTrue(server['command'])
                    self.assertTrue(all(isinstance(x, str) for x in server['command']))
                else:
                    self.assertIsInstance(server['url'], str)
                    self.assertTrue(server.get('oauth', False) is False or
                                    isinstance(server.get('oauth'), dict))

    def native_config(self):
        codex = shutil.which('codex')
        if not codex:
            self.skipTest('Codex CLI unavailable; static contracts still run')
        version = self.run_isolated([codex, '--version'])
        self.assertEqual(version.returncode, 0)
        self.assertRegex(version.stdout.strip(), r'^codex-cli \d+\.\d+\.\d+')
        metadata = version.stdout.strip()
        # File stores prevent reading the real OS keychain. No credentials are
        # supplied; list is configuration inspection, not MCP connection/startup.
        text = ('cli_auth_credentials_store = "file"\n'
                'mcp_oauth_credentials_store = "file"\n' + CODEX.read_text())
        config = self.scratch / 'codex/config.toml'
        config.write_text(text)
        return codex, metadata, config, text

    def test_native_codex_config_parse_without_starting_servers(self):
        codex, metadata, config, text = self.native_config()
        command = [codex, '--strict-config', 'mcp', 'list', '--json']
        result = self.run_isolated(command)
        unsupported = '`--strict-config` is not supported for `codex mcp`'
        if result.returncode != 0 and unsupported in result.stderr:
            command = [codex, 'mcp', 'list', '--json']
            result = self.run_isolated(command)
        # Never dump native output: parser diagnostics can quote source secrets.
        fields = re.findall(r'unknown field [`\']([a-z_]+)[`\']', result.stderr)
        # Retain error prose, but redact every string value in the input TOML,
        # paths, URLs, and source excerpts before displaying native diagnostics.
        def strings(value):
            if isinstance(value, str):
                yield value
            elif isinstance(value, dict):
                for child in value.values():
                    yield from strings(child)
            elif isinstance(value, list):
                for child in value:
                    yield from strings(child)
        diagnostic = result.stderr
        for value in sorted(set(strings(tomllib.loads(text))), key=len, reverse=True):
            if len(value) > 3:
                diagnostic = diagnostic.replace(value, '[redacted]')
        diagnostic = re.sub(r'https?://\S+|/\S+', '[path/url]', diagnostic)
        diagnostic = re.sub(r'(?m)^.*[=|].*$', '[source excerpt withheld]', diagnostic)
        self.assertEqual(result.returncode, 0,
                         f'{metadata}: native MCP parse failed; unknown fields={fields}; '
                         + diagnostic[:1500])
        try:
            rows = json.loads(result.stdout)
        except json.JSONDecodeError:
            self.fail(f'{metadata}: mcp list did not return JSON (output withheld)')
        self.assertIsInstance(rows, list)
        self.assertEqual({row['name'] for row in rows}, GLOBAL | OPT_IN)
        self.assertEqual({row['name'] for row in rows if row['enabled']}, GLOBAL)
        # Even when strict mode is unavailable, native typed deserialization
        # must reject a malformed MCP field rather than silently ignore it.
        config.write_text(text + '\n[mcp_servers.contract_invalid]\n'
                          'url = "https://fixture.invalid/mcp"\n'
                          'enabled = "not-a-boolean"\n')
        invalid = self.run_isolated(command)
        self.assertNotEqual(invalid.returncode, 0,
                            f'{metadata}: native parser accepted invalid enabled type')

    def test_native_codex_strict_mode_rejects_unknown_fields(self):
        codex, metadata, config, text = self.native_config()
        command = [codex, '--strict-config', 'mcp', 'list', '--json']
        result = self.run_isolated(command)
        if (result.returncode != 0 and
                '`--strict-config` is not supported for `codex mcp`' in result.stderr):
            self.skipTest(f'{metadata}: --strict-config unsupported for codex mcp; '
                          'native non-strict parsing tested separately')
        self.assertEqual(result.returncode, 0, 'strict parse failed; output withheld')
        # Negative control: a permissive parser must not silently pass this test.
        config.write_text('contract_unknown_field = true\n' + text)
        invalid = self.run_isolated(command)
        self.assertNotEqual(invalid.returncode, 0,
                            f'{metadata}: strict parser accepted an unknown field')


if __name__ == '__main__':
    unittest.main()
