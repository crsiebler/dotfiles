import importlib.util
from pathlib import Path
import tempfile
import unittest
import tomllib
import json
import os
import subprocess
import sys
import io
import errno
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class InstallTest(unittest.TestCase):
    def test_exact_read_exceptions_and_denied_namespace_survive_reinstall(self):
        m = self.module()
        source = {'permission': {
            'github_*': 'ask', 'github_get_file_contents': 'allow',
            'exa_*': 'deny', 'exa_web_search_exa': 'allow',
        }}
        m.check_prompt_conflicts(source, source)
        result = m.merge(source, source)
        self.assertEqual(list(result['permission']), list(source['permission']))
        old = {'permission': {'github_get_file_contents': 'deny'}}
        result = m.merge(old, source)['permission']
        self.assertEqual(result['github_get_file_contents'], 'deny')
        self.assertEqual(list(result)[-1], 'github_get_file_contents')
        m.check_prompt_conflicts({'agent': {'custom': {
            'permission': {'github_get_file_contents': 'allow'}}}}, source)
        for permission in ({'github_*': 'allow'}, {'*create_issue': 'allow'},
                           {'github_get_*': 'allow'}, {'exa_future_write': 'allow'},
                           {'exa_*': 'ask'}, {'exa_*': 'deny'},
                           {'exa_web_search_exa': 'allow', 'exa_*': 'deny'}):
            with self.subTest(permission=permission):
                with self.assertRaisesRegex(ValueError, 'reconcile'):
                    m.check_prompt_conflicts({'permission': permission}, source)

    def test_codex_exact_reads_and_research_allowlists(self):
        m = self.module()
        source = {'mcp_servers': {'exa': {
            'default_tools_approval_mode': 'prompt',
            'enabled_tools': ['web_search_exa'],
            'tools': {'web_search_exa': {'approval_mode': 'approve'}},
        }}}
        m.check_prompt_conflicts(source, source)
        m.check_prompt_conflicts({'profiles': {'custom': source}}, source)
        for settings in (
                {'tools': {'future_write': {'approval_mode': 'approve'}}},
                {'tools': {'web_search_*': {'approval_mode': 'approve'}}},
                {'tools': {'web_search_exa': {'approval_mode': 'deny'}}},
                {'default_tools_approval_mode': 'approve'},
                {'enabled_tools': ['web_search_exa', 'future_write']}):
            with self.subTest(settings=settings):
                with self.assertRaisesRegex(ValueError, 'reconcile'):
                    m.check_prompt_conflicts({'mcp_servers': {'exa': settings}}, source)
        old = {'mcp_servers': {'exa': {'tools': {
            'web_search_exa': {'enabled': False}}}}}
        self.assertIs(m.merge(old, source)['mcp_servers']['exa']['tools']
                      ['web_search_exa']['enabled'], False)

    def test_real_permission_sources_can_be_merged_and_reinstalled(self):
        m = self.module()
        for relative in ('ai/opencode/opencode.json', 'ai/codex/config.toml'):
            source = m.load_config(ROOT / relative)
            result = m.merge({}, source)
            m.check_prompt_conflicts(result, source)
            again = m.merge(result, source)
            self.assertEqual(result, again)
            if 'permission' in source:
                self.assertEqual(list(source['permission']), list(again['permission']))
            else:
                self.assertEqual(tomllib.loads(m.toml_dump(again)), source)


    def test_codex_permissive_server_defaults_in_companions_and_nested_profiles(self):
        m = self.module()
        source = {'mcp_servers': {'github': {'default_tools_approval_mode': 'prompt'}}}
        unsafe = {'mcp_servers': {'github': {'default_tools_approval_mode': 'auto'}}}
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            root = Path(directory)
            managed = root / 'managed.toml'
            managed.write_text(m.toml_dump(source))
            companion = root / 'astra.config.toml'
            companion.write_text(m.toml_dump(unsafe))
            with self.assertRaisesRegex(ValueError, 'reconcile'):
                m.config_bytes(companion, managed)
            self.assertEqual(tomllib.loads(companion.read_text()), unsafe)
        with self.assertRaisesRegex(ValueError, 'reconcile'):
            m.check_prompt_conflicts({'profiles': {'outer': {'profiles': {'inner': unsafe}}}}, source)
        m.check_prompt_conflicts({'mcp_servers': {'unrelated': {'default_tools_approval_mode': 'auto'}}}, source)
        m.check_prompt_conflicts(source, source)

    def test_prompt_conflicts_refused_and_deny_preserved(self):
        m = self.module()
        self.assertTrue(hasattr(m, 'check_prompt_conflicts'))
        source = {'permission': {'github_*': 'ask'}, 'mcp': {'github': {}}}
        for old in [
            {'permission': {'github_*': 'ask', 'github_create_issue': 'allow'}},
            {'agent': {'custom': {'permission': {'github_*': 'allow'}}}},
            {'agent': {'custom': {'permission': 'allow'}}},
        ]:
            with self.assertRaisesRegex(ValueError, 'reconcile'):
                m.check_prompt_conflicts(old, source)
        old = {'permission': {'github_create_issue': 'deny', 'unrelated_tool': 'allow'}}
        m.check_prompt_conflicts(old, source)
        self.assertEqual(m.merge(old, source)['permission']['github_create_issue'], 'deny')
        self.assertEqual(list(m.merge(old, source)['permission'])[-1], 'github_create_issue')
        self.assertEqual(m.merge({'permission': {'github_*': 'deny'}}, source)['permission']['github_*'], 'deny')
        self.assertEqual(m.merge({'permission': 'deny'}, source)['permission'], 'deny')
        nested = {'permission': {'github_*': {'*': 'deny'}}}
        self.assertEqual(m.merge(nested, source)['permission']['github_*'], {'*': 'deny'})
        codex = {'mcp_servers': {'github': {'default_tools_approval_mode': 'prompt'}}}
        for mode in ('auto', 'never'):
            with self.assertRaisesRegex(ValueError, 'reconcile'):
                m.check_prompt_conflicts({'mcp_servers': {'github': {'tools': {'write': {'approval_mode': mode}}}}}, codex)
        m.check_prompt_conflicts({'mcp_servers': {'unrelated': {'tools': {'write': {'approval_mode': 'auto'}}}}}, codex)

    def test_remote_endpoint_change_drops_old_credential_bindings(self):
        m = self.module()
        for namespace in ('mcp', 'mcp_servers'):
            old = {namespace: {'jira': {'url': 'https://old.invalid/mcp',
                    'headers': {'Authorization': 'secret-sentinel'}, 'oauth': {'clientId': 'old'},
                    'http_headers': {'X-Token': 'secret-sentinel'}, 'env_http_headers': {'X-Key': 'OLD_KEY'},
                    'bearer_token_env_var': 'OLD_TOKEN', 'enabled': False}}}
            new = {namespace: {'jira': {'url': 'https://new.invalid/mcp',
                                      'headers': {'Authorization': '{env:NEW_TOKEN}'}}}}
            result = m.merge(old, new)[namespace]['jira']
            self.assertEqual(result, {'url': 'https://new.invalid/mcp',
                                     'headers': {'Authorization': '{env:NEW_TOKEN}'}, 'enabled': False})

    def test_renderer_summary_is_emitted_without_hardcoded_counts(self):
        m = self.module()
        self.assertTrue(hasattr(m, 'render_agents'))
        output = io.StringIO()
        calls = []
        summary = '{"harness":"codex","sources":7,"rendered":7,"written":7,"output":"staging"}\n'
        def execute(argv):
            calls.append(argv)
            return summary.replace('"codex"', json.dumps(argv[3]))
        for harness in ('opencode', 'codex'):
            m.render_agents('staging', execute, output, harness=harness)
        self.assertIn('Prepared codex agents: 7 sources, 7 rendered, 7 staged.', output.getvalue())
        self.assertNotIn('{', output.getvalue())
        self.assertNotIn('staging', output.getvalue())
        self.assertEqual(calls, [
            [sys.executable, str(ROOT / 'scripts/render-agents.py'),
             '--harness', harness, '--output', 'staging']
             for harness in ('opencode', 'codex')])

    def test_safe_parse_errors(self):
        m = self.module()
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            for suffix, text in [('json', '{"secret-sentinel": }'),
                                 ('toml', '[secret-sentinel]\n[secret-sentinel]\n')]:
                path = Path(directory) / f'config.{suffix}'
                path.write_text(text)
                with self.assertRaises(ValueError) as caught:
                    m.load_config(path)
                message = str(caught.exception)
                self.assertNotIn('secret-sentinel', message)
                self.assertIn(str(path), message)
                self.assertIn('line', message)

    def test_safe_cli_errors_and_malformed_response(self):
        m = self.module()
        failed = subprocess.CompletedProcess([], 23, 'secret-sentinel', 'secret-sentinel')
        with patch.object(m.subprocess, 'run', return_value=failed):
            with self.assertRaisesRegex(ValueError, 'installing coding@craft.*exit status 23') as caught:
                m.run(['codex', 'plugin', 'add', 'coding@craft'])
            self.assertNotIn('secret-sentinel', str(caught.exception))
        with self.assertRaisesRegex(ValueError, 'CLI JSON.*listing marketplaces') as caught:
            m.check_plugins(ROOT, 'craft', [], lambda argv: '{secret-sentinel')
        self.assertNotIn('secret-sentinel', str(caught.exception))
        for response in ('{secret-sentinel', '{"marketplaces": null}',
                         '{"marketplaces": [{"secret-sentinel": 1}]}'):
            with self.assertRaisesRegex(ValueError, 'CLI JSON.*listing marketplaces') as caught:
                m.check_plugins(ROOT, 'craft', [], lambda argv: response)
            self.assertNotIn('secret-sentinel', str(caught.exception))

    def test_renderer_rejects_invalid_summary_without_echoing_it(self):
        m = self.module()
        for response in ('{secret-sentinel', '{"harness": "secret-sentinel"}',
                         '{"harness":"codex","sources":true,"rendered":1,"written":1}'):
            with redirect_stdout(io.StringIO()) as output:
                with self.assertRaisesRegex(ValueError, 'CLI JSON') as caught:
                    m.render_agents('private-staging', lambda argv: response, harness='codex')
            self.assertEqual(output.getvalue(), '')
            self.assertNotIn('secret-sentinel', str(caught.exception))
            self.assertNotIn('private-staging', str(caught.exception))

    def test_progress_is_ascii_and_flushed(self):
        m = self.module()
        stream = io.StringIO()
        with patch.object(stream, 'flush', wraps=stream.flush) as flush:
            m.say('Target: /café\nnext\x1b', stream)
            flush.assert_called_once()
        self.assertEqual(stream.getvalue(), 'Target: /caf\\xe9\\nnext\\x1b\n')

    def test_prerequisites_precede_renderer(self):
        m = self.module()
        for available, version, expected in [(None, '', 'required on PATH'),
                                              ('codex', 'wrong', '0.153.4 required')]:
            calls = []
            def execute(argv):
                calls.append(argv)
                return version
            with patch.object(sys, 'argv', ['install-ai.py', 'codex']), \
                    patch.object(m.shutil, 'which', return_value=available), \
                    patch.object(m, 'run', side_effect=execute):
                with self.assertRaisesRegex(ValueError, expected):
                    m.main()
            self.assertTrue(all(argv == ['codex', '--version'] for argv in calls))

    def test_partial_outcome_reporting(self):
        m = self.module()
        for started in (False, True):
            def fail():
                m.PROGRESS.started = started
                m.PROGRESS.phase = 'installing skills bundle coding'
                raise ValueError('fixture failure')
            output = io.StringIO()
            with patch.object(m, 'main', side_effect=fail), redirect_stderr(output):
                self.assertEqual(m.cli(), 1)
            self.assertIn('installing skills bundle coding', output.getvalue())
            self.assertIn('may remain' if started else 'No destination writes', output.getvalue())

    def test_io_errors_are_safe_and_distinct(self):
        m = self.module()
        for code, category in [(errno.EACCES, 'permission denied'),
                               (errno.ENOENT, 'not found'),
                               (errno.ENOTDIR, 'not a directory'),
                               (errno.ENOSPC, 'no space left')]:
            error = OSError(code, 'secret-sentinel', '/fixture/config.toml')
            with patch.object(m, 'main', side_effect=error), redirect_stderr(io.StringIO()) as output:
                self.assertEqual(m.cli(), 1)
            self.assertIn(category, output.getvalue())
            self.assertIn('/fixture/config.toml', output.getvalue())
            self.assertNotIn('secret-sentinel', output.getvalue())

    def test_plugin_and_bundle_completion_only_after_success(self):
        m = self.module()
        def execute(argv):
            if argv[1:4] == ['plugin', 'marketplace', 'list']:
                return '{"marketplaces": []}'
            if argv[1:3] == ['plugin', 'list']:
                return '{"installed": [], "available": []}'
            if argv[-1] == 'reporting@craft' or 'reporting/skills' in argv[2]:
                raise ValueError('fixture failure')
            return ''
        plugins = [('coding', ROOT / 'ai/plugins/coding'),
                   ('reporting', ROOT / 'ai/plugins/reporting')]
        for install, expected in [(lambda: m.install_plugins(ROOT, 'craft', plugins, execute),
                                   'Installed plugin coding@craft.'),
                                  (lambda: m.install_skills(plugins, execute),
                                   'Installed skills bundle coding.')]:
            with redirect_stdout(io.StringIO()) as output:
                with self.assertRaisesRegex(ValueError, 'fixture failure'):
                    install()
            self.assertIn(expected, output.getvalue())
            self.assertNotIn('Installed plugin reporting', output.getvalue())
            self.assertNotIn('Installed skills bundle reporting', output.getvalue())

    def module(self):
        path = ROOT / 'scripts/install-ai.py'
        self.assertTrue(path.exists(), 'installer helper must exist')
        spec = importlib.util.spec_from_file_location('installer', path)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_merge_preserves_unrelated_and_env(self):
        m = self.module()
        result = m.merge({'mcp': {'custom': {'token': '{env:SECRET}'}, 'shared': {'extra': 1}}},
                         {'mcp': {'shared': {'enabled': False}}})
        self.assertEqual(result['mcp']['custom']['token'], '{env:SECRET}')
        self.assertEqual(result['mcp']['shared'], {'extra': 1, 'enabled': False})

    def test_mcp_transport_replacement_preserves_unrelated_settings(self):
        m = self.module()
        for key, old, new in [
            ('mcp', {'type': 'local', 'command': ['node', 'old'], 'environment': {'OLD': 'reference'}},
             {'type': 'remote', 'url': 'https://example.com/mcp'}),
            ('mcp_servers', {'command': 'node', 'args': ['old'], 'env': {'OLD': 'reference'}, 'cwd': '/old'},
             {'url': 'https://example.com/mcp'}),
        ]:
            result = m.merge({key: {'jira': dict(old, enabled=True, custom_timeout=30), 'unrelated': old}},
                             {key: {'jira': new}})
            self.assertEqual(result[key]['jira'], dict(new, enabled=True, custom_timeout=30))
            self.assertEqual(result[key]['unrelated'], old)

    def test_mcp_command_change_replaces_environment(self):
        m = self.module()
        for key, env_key, command in [('mcp', 'environment', ['docker', 'run']),
                                       ('mcp_servers', 'env', 'docker')]:
            result = m.merge({key: {'postgresql': {'command': 'node', env_key: {'STALE': 'old'}, 'enabled': True}}},
                             {key: {'postgresql': {'command': command, env_key: {'DATABASE_URI': '{env:DATABASE_URI}'}}}})
            self.assertEqual(result[key]['postgresql'][env_key], {'DATABASE_URI': '{env:DATABASE_URI}'})
            self.assertTrue(result[key]['postgresql']['enabled'])

    def test_github_token_preflight(self):
        m = self.module()
        self.assertTrue(hasattr(m, 'check_github_token'))
        for config in [
            {'mcp': {'github': {'enabled': True, 'headers': {'Authorization': 'Bearer {env:GITHUB_MCP_TOKEN}'}}}},
            {'mcp_servers': {'github': {'bearer_token_env_var': 'GITHUB_MCP_TOKEN'}}},
        ]:
            with self.assertRaisesRegex(ValueError, 'GITHUB_MCP_TOKEN'):
                m.check_github_token(config, {})
            m.check_github_token(config, {'GITHUB_MCP_TOKEN': 'fixture-only-not-a-token'})
            table = config.get('mcp', config.get('mcp_servers'))
            table['github']['enabled'] = False
            m.check_github_token(config, {})

    def test_toml_roundtrip(self):
        m = self.module()
        value = {'model': 'astra', 'plugins': {'coding@craft': {'enabled': True}},
                 'other': {'env': '${SECRET}', 'array': [{'x': 1}], 'unicode': '\U0001f600\x7f'}}
        self.assertEqual(tomllib.loads(m.toml_dump(value)), value)

    def test_backup_idempotent(self):
        m = self.module()
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            file = Path(directory) / 'config.json'
            file.write_bytes(b'old')
            m.write_managed(file, b'new')
            m.write_managed(file, b'new')
            self.assertEqual(file.read_bytes(), b'new')
            backups = list(file.parent.glob('config.json.backup.*'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), b'old')

    def test_native_config_backup_only_on_change(self):
        m = self.module()
        self.assertTrue(hasattr(m, 'with_native_backup'))
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            file = Path(directory) / 'config.toml'
            file.write_bytes(b'old')
            for _ in range(2):
                m.with_native_backup(file, lambda: file.write_bytes(b'new'))
            backups = list(file.parent.glob('config.toml.backup.*'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), b'old')

    def test_marketplace_local_and_unique(self):
        m = self.module()
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                m.local_plugins(root, {'name': 'craft', 'plugins': [
                    {'name': 'bad', 'source': {'source': 'url', 'url': 'https://example.com'}}]})

    def test_registration_clash(self):
        m = self.module()
        with self.assertRaises(ValueError):
            m.check_registration(ROOT, 'craft', {'marketplaces': [
                {'name': 'craft', 'root': '/different/checkout'}]})

    def test_plugin_clash_preflight(self):
        m = self.module()
        calls = []
        def run(argv):
            calls.append(argv)
            if argv[1:4] == ['plugin', 'marketplace', 'list']:
                return '{"marketplaces": []}'
            return json.dumps({'installed': [{'pluginId': 'coding@craft',
                              'source': {'source': 'local', 'path': '/different'}}], 'available': []})
        self.assertTrue(hasattr(m, 'check_plugins'), 'plugin preflight must be reusable before config writes')
        with self.assertRaises(ValueError):
            m.check_plugins(ROOT, 'craft', [('coding', ROOT / 'ai/plugins/coding')], run)
        self.assertTrue(all('add' not in command for command in calls))

    def test_codex_native_commands(self):
        m = self.module()
        calls = []
        def run(argv):
            calls.append(argv)
            if argv[1:4] == ['plugin', 'marketplace', 'list']:
                return '{"marketplaces": []}'
            if argv[1:3] == ['plugin', 'list']:
                return '{"installed": [], "available": []}'
            return '{}'
        m.install_plugins(ROOT, 'craft', [('coding', ROOT / 'ai/plugins/coding')], run)
        self.assertIn(['codex', 'plugin', 'marketplace', 'add', str(ROOT)], calls)
        self.assertIn(['codex', 'plugin', 'add', 'coding@craft'], calls)
        self.assertTrue(all('--marketplace' in c for c in calls if c[1:3] == ['plugin', 'list']))

    def test_skills_local_command(self):
        m = self.module()
        calls = []
        m.install_skills([('coding', ROOT / 'ai/plugins/coding')], calls.append)
        self.assertEqual(calls, [['skills', 'add', str(ROOT / 'ai/plugins/coding/skills'),
                                 '--agent', 'opencode', '--global', '--copy', '--yes']])

    def test_research_skill_discovery_and_bundled_reference(self):
        m = self.module()
        manifest = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text())
        plugins = dict(m.local_plugins(ROOT, manifest))
        skills = plugins['researching'] / 'skills'
        self.assertEqual([p.parent.name for p in skills.glob('*/SKILL.md')],
                         ['search-web'])
        source = skills / 'search-web'
        self.assertEqual({p.relative_to(source).as_posix()
                          for p in source.rglob('*') if p.is_file()},
                         {'SKILL.md', 'references/exa.md'})

    def test_isolated_install_merge_and_repeat(self):
        self.module()
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            root = Path(directory)
            def put(name, text):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text)
                return path
            put('scripts/install-ai.py', (ROOT / 'scripts/install-ai.py').read_text())
            put('scripts/render-agents.py', (ROOT / 'scripts/render-agents.py').read_text())
            role = put('ai/codex/agents/example.toml',
                       'name = "example"\ndescription = "Fixture"\n'
                       'developer_instructions = "Rendered fixture"\n')
            for name in ('config.toml', 'astra.config.toml'):
                put(f'ai/codex/{name}', 'model = "fixture"\n')
            instruction_bytes = '# Personal café — 共通\r\nKeep exact bytes.  \r\n\r\n\r\n'.encode('utf-8')
            instructions = root / 'ai/AGENTS.md'
            reviewer = put('ai/opencode/agents/ralph-reviewer.md',
                           '---\nmode: subagent\nsteps: 3\n---\nExact reviewer\n')
            native = put('ai/opencode/agents/native-only.md',
                         '---\ndescription: Native fixture\nmode: primary\n'
                         'permission: {"*": "deny", "read": "allow"}\n---\n\nExact café body\n')
            put('tests/.fixture', '')
            plugins = []
            for name in ('coding', 'reporting', 'researching', 'delegating'):
                put(f'ai/plugins/{name}/.codex-plugin/plugin.json', json.dumps({'name': name, 'skills': './skills/'}))
                put(f'ai/plugins/{name}/skills/{name}/SKILL.md', f'---\nname: {name}\n---\nLocal')
                plugins.append({'name': name, 'source': {'source': 'local', 'path': f'ai/plugins/{name}'},
                                'policy': {'authentication': 'ON_USE'}})
            put('.agents/plugins/marketplace.json', json.dumps({'name': 'craft', 'plugins': plugins}))
            put('ai/opencode/opencode.json', json.dumps({'model': 'test/model', 'mcp': {
                'shared': {'enabled': False}, 'github': {'enabled': True,
                    'headers': {'Authorization': 'Bearer {env:GITHUB_MCP_TOKEN}'}}}}))
            put('ai/opencode/astra.json', '{"model":"test/astra"}')
            target = put('home/xdg/opencode/opencode.json', '{"custom":"preserved","mcp":{"private":{"token":"{env:SECRET}"}}}')
            old_role = put('home/xdg/opencode/agents/example.md', 'previous role')
            custom_role = put('home/xdg/opencode/agents/custom.md', 'keep custom')
            old_skill = put('home/xdg/opencode/skills/use-exa/SKILL.md', 'old installed skill')
            external_skill = put('home/.agents/skills/prd/SKILL.md', 'unmanaged external skill')
            fake = put('fakebin/skills', '#!/bin/sh\nexit 0\n')
            fake.chmod(0o755)
            early_codex = put('fakebin/codex', '#!/bin/sh\nprintf "codex-cli 0.153.4\\n"\n')
            early_codex.chmod(0o755)
            env = dict(os.environ, HOME=str(root / 'home'), CODEX_HOME=str(root / 'home/codex'),
                       XDG_CONFIG_HOME=str(root / 'home/xdg'), PATH=str(root / 'fakebin'))
            env.pop('GITHUB_MCP_TOKEN', None)
            for harness in ('validate', 'opencode', 'codex', 'all'):
                with self.subTest(missing_instructions=harness):
                    before_home = {p.relative_to(root / 'home'): p.read_bytes()
                                   for p in (root / 'home').rglob('*') if p.is_file()}
                    missing_source = subprocess.run(
                        [sys.executable, str(root / 'scripts/install-ai.py'), harness],
                        env=env, cwd=root, capture_output=True, text=True)
                    self.assertNotEqual(missing_source.returncode, 0)
                    self.assertIn('missing required source: ai/AGENTS.md',
                                  missing_source.stderr)
                    self.assertEqual(before_home, {
                        p.relative_to(root / 'home'): p.read_bytes()
                        for p in (root / 'home').rglob('*') if p.is_file()})
                    self.assertFalse((root / 'home/codex').exists())
            instructions.write_bytes(instruction_bytes)
            before = target.read_bytes()
            missing = subprocess.run([sys.executable, str(root / 'scripts/install-ai.py'), 'opencode'],
                                     env=env, cwd=root, capture_output=True, text=True)
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn('GITHUB_MCP_TOKEN', missing.stderr)
            self.assertEqual(target.read_bytes(), before)
            env['GITHUB_MCP_TOKEN'] = 'fixture-sentinel-not-a-real-token'
            for _ in range(2):
                result = subprocess.run([sys.executable, str(root / 'scripts/install-ai.py'), 'opencode'],
                                        env=env, cwd=root, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotIn(env['GITHUB_MCP_TOKEN'], result.stdout + result.stderr)
                self.assertEqual((target.parent / 'AGENTS.md').read_bytes(), instruction_bytes)
                self.assertEqual(list(target.parent.glob('AGENTS.md.backup.*')), [])
            value = json.loads(target.read_text())
            self.assertEqual(value['custom'], 'preserved')
            self.assertEqual(value['mcp']['private']['token'], '{env:SECRET}')
            self.assertFalse(value['mcp']['shared']['enabled'])
            self.assertEqual(len(list(target.parent.glob('opencode.json.backup.*'))), 1)
            self.assertEqual((target.parent / 'AGENTS.md').read_bytes(), instruction_bytes)
            self.assertEqual(json.loads((target.parent / 'astra.json').read_text())['model'], 'test/astra')
            self.assertEqual(value['model'], 'test/model')
            self.assertIn('Managed scope:', result.stderr)
            self.assertNotIn(env['GITHUB_MCP_TOKEN'], target.read_text())
            self.assertEqual(old_skill.read_text(), 'old installed skill')
            self.assertEqual(external_skill.read_text(), 'unmanaged external skill')
            self.assertNotIn('retired', result.stdout + result.stderr)
            self.assertNotIn('move them', result.stdout + result.stderr)
            self.assertTrue((target.parent / 'agents/example.md').is_file(),
                            'OpenCode roles must come from the renderer')
            self.assertEqual((target.parent / 'agents/example.md').read_text(),
                             '---\ndescription: "Fixture"\nmode: "subagent"\n'
                             '---\nRendered fixture')
            self.assertEqual((target.parent / 'agents/ralph-reviewer.md').read_bytes(),
                             reviewer.read_bytes())
            backups = list(old_role.parent.glob('example.md.backup.*'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), 'previous role')
            self.assertEqual(custom_role.read_text(), 'keep custom')
            with self.subTest('native-only source copied byte exact'):
                installed_native = target.parent / 'agents/native-only.md'
                self.assertTrue(installed_native.is_file())
                self.assertEqual(installed_native.read_bytes(), native.read_bytes())
            validated = subprocess.run(
                [sys.executable, str(root / 'scripts/install-ai.py'), 'validate'],
                env=dict(env, PATH=''), cwd=root, capture_output=True, text=True)
            self.assertEqual(validated.returncode, 0, validated.stderr)
            self.assertIn('Prepared opencode agents: 1 sources, 1 rendered, 1 staged.', result.stdout)
            self.assertIn('3 agents (1 rendered + 2 native), 0 commands', result.stdout)
            self.assertNotIn('{', result.stdout)
            self.assertNotIn('.ai-render-', result.stdout + result.stderr)
            self.assertFalse((root / 'home/codex').exists(),
                             'validation must not write harness configuration')
            fake_codex = put('fakebin/codex', f'#!{sys.executable}\n' + '''import sys
if sys.argv[1:] == ['--version']:
    print('codex-cli 0.153.4')
elif sys.argv[1:4] == ['plugin', 'marketplace', 'list']:
    print('{"marketplaces": []}')
else:
    print('{"installed": [], "available": []}')
''')
            fake_codex.chmod(0o755)
            working_codex = fake_codex.read_text()
            fake_codex.write_text(working_codex.replace('{"marketplaces": []}',
                '{"marketplaces": [{"name": "craft", "root": "/different"}]}'))
            clash = subprocess.run(
                [sys.executable, str(root / 'scripts/install-ai.py'), 'codex'],
                env=env, cwd=root, capture_output=True, text=True)
            self.assertEqual(clash.returncode, 1)
            self.assertIn('No managed-file writes or plugin/skill installation started.', clash.stderr)
            self.assertNotIn('Partial installation:', clash.stderr)
            self.assertFalse((root / 'home/codex/config.toml').exists())
            fake_codex.write_text(working_codex)
            installed_codex = subprocess.run(
                [sys.executable, str(root / 'scripts/install-ai.py'), 'codex'],
                env=env, cwd=root, capture_output=True, text=True)
            self.assertEqual(installed_codex.returncode, 0, installed_codex.stderr)
            codex_home = root / 'home/codex'
            self.assertEqual((codex_home / 'AGENTS.md').read_bytes(), instruction_bytes)
            self.assertEqual(tomllib.loads((codex_home / 'config.toml').read_text())['model'], 'fixture')
            self.assertEqual(tomllib.loads((codex_home / 'astra.config.toml').read_text()),
                             tomllib.loads((root / 'ai/codex/astra.config.toml').read_text()))
            self.assertFalse((codex_home / 'ralph.config.toml').exists())
            codex_agents = root / 'home/codex/agents'
            self.assertEqual((codex_agents / role.name).read_bytes(), role.read_bytes())
            self.assertEqual([p.name for p in codex_agents.iterdir()], ['example.toml'])
            self.assertIn('Prepared codex agents: 1 sources, 1 rendered, 1 staged.', installed_codex.stdout)
            # Real isolated failures: commands can mutate configuration before
            # returning nonzero, and their output must never reach diagnostics.
            working_codex = fake_codex.read_text()
            fake_codex.write_text(working_codex.replace('import sys', 'import sys\nfrom pathlib import Path\nimport os\n'
                'if sys.argv[1:] == ["plugin", "add", "coding@craft"]:\n'
                '    Path(os.environ["CODEX_HOME"], "config.toml").write_text("# CLI changed config\\n")\n'
                '    print("secret-sentinel")\n'
                '    print("secret-sentinel", file=sys.stderr)\n'
                '    sys.exit(23)'))
            failed_plugin = subprocess.run(
                [sys.executable, str(root / 'scripts/install-ai.py'), 'codex'],
                env=env, cwd=root, capture_output=True, text=True)
            self.assertEqual(failed_plugin.returncode, 1)
            self.assertIn('installing coding@craft: exit status 23', failed_plugin.stderr)
            self.assertIn('0 plugins, 0 skill bundles', failed_plugin.stderr)
            self.assertIn('may remain', failed_plugin.stderr)
            self.assertNotIn('Installed plugin coding@craft.', failed_plugin.stdout)
            self.assertNotIn('secret-sentinel', failed_plugin.stdout + failed_plugin.stderr)
            self.assertEqual((codex_home / 'config.toml').read_text(), '# CLI changed config\n')
            self.assertTrue(any('fixture' in backup.read_text()
                                for backup in codex_home.glob('config.toml.backup.*')))
            fake_codex.write_text(working_codex)
            fake.write_text('#!/bin/sh\ncase "$2" in */reporting/skills)\n'
                            'printf "secret-sentinel\\n" >&2\nexit 19;;\nesac\nexit 0\n')
            failed_bundle = subprocess.run(
                [sys.executable, str(root / 'scripts/install-ai.py'), 'all'],
                env=env, cwd=root, capture_output=True, text=True)
            self.assertEqual(failed_bundle.returncode, 1)
            self.assertIn('installing skills bundle reporting: exit status 19', failed_bundle.stderr)
            self.assertIn(f'{len(plugins)} plugins, 1 skill bundles', failed_bundle.stderr)
            self.assertIn('Installed skills bundle coding.', failed_bundle.stdout)
            self.assertNotIn('Installed skills bundle reporting.', failed_bundle.stdout)
            self.assertNotIn('secret-sentinel', failed_bundle.stdout + failed_bundle.stderr)
            fake.write_text('#!/bin/sh\nexit 0\n')
            for expected in (instruction_bytes,
                             '# Updated café — 共通\r\nNew policy.\r\n\r\n'.encode('utf-8')):
                instructions.write_bytes(expected)
                for _ in range(2):
                    repeated = subprocess.run(
                        [sys.executable, str(root / 'scripts/install-ai.py'), 'all'],
                        env=env, cwd=root, capture_output=True, text=True)
                    self.assertEqual(repeated.returncode, 0, repeated.stderr)
                    self.assertNotIn(env['GITHUB_MCP_TOKEN'], repeated.stdout + repeated.stderr)
                    for destination in (codex_home, target.parent):
                        self.assertEqual((destination / 'AGENTS.md').read_bytes(), expected)
                        backups = list(destination.glob('AGENTS.md.backup.*'))
                        self.assertEqual(len(backups), int(expected != instruction_bytes))
                        for backup in backups:
                            self.assertEqual(backup.read_bytes(), instruction_bytes)
            self.assertFalse((root / 'home/.codex').exists())
            self.assertFalse((root / 'home/.config/opencode').exists())
            # A source collision must fail before any destination changes, even
            # in validate mode; use different casing for cross-platform safety.
            put('ai/opencode/agents/Example.md', 'colliding native source')
            for harness in ('validate', 'opencode', 'codex', 'all'):
                before = {p.relative_to(root / 'home'): p.read_bytes()
                          for p in (root / 'home').rglob('*') if p.is_file()}
                collision = subprocess.run(
                    [sys.executable, str(root / 'scripts/install-ai.py'), harness],
                    env=env, cwd=root, capture_output=True, text=True)
                self.assertNotEqual(collision.returncode, 0)
                self.assertIn('collision', collision.stderr)
                self.assertEqual(before, {
                    p.relative_to(root / 'home'): p.read_bytes()
                    for p in (root / 'home').rglob('*') if p.is_file()})
            (root / 'ai/opencode/agents/Example.md').rename(
                root / 'ai/opencode/agents/not-a-collision.md')
            role.write_text('[secret-sentinel]\n[secret-sentinel]\n')
            invalid = subprocess.run(
                [sys.executable, str(root / 'scripts/install-ai.py'), 'opencode'],
                env=env, cwd=root, capture_output=True, text=True)
            self.assertNotEqual(invalid.returncode, 0)
            self.assertNotIn('secret-sentinel', invalid.stdout + invalid.stderr)
            self.assertIn(str(role), invalid.stderr)
            self.assertIn('line 2', invalid.stderr)
            (root / 'scripts/render-agents.py').rename(root / 'scripts/renderer-disabled')
            for harness in ('opencode', 'codex'):
                missing_renderer = subprocess.run(
                    [sys.executable, str(root / 'scripts/install-ai.py'), harness],
                    env=env, cwd=root, capture_output=True, text=True)
                self.assertNotEqual(missing_renderer.returncode, 0)
                self.assertIn('missing required source: scripts/render-agents.py',
                              missing_renderer.stderr)

    def test_symlink_parent_refused(self):
        m = self.module()
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            root = Path(directory)
            (root / 'actual').mkdir()
            (root / 'link').symlink_to(root / 'actual', target_is_directory=True)
            with self.assertRaises(ValueError):
                m.write_managed(root / 'link/config.json', b'new')

    def test_custom_skill_files_block_destructive_cli_copy(self):
        m = self.module()
        self.assertTrue(hasattr(m, 'check_skill_copies'))
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            root = Path(directory)
            source = root / 'plugin/skills/example'
            source.mkdir(parents=True)
            (source / 'SKILL.md').write_text('new')
            target = root / 'opencode/skills/example'
            target.mkdir(parents=True)
            (target / 'SKILL.md').write_text('old')
            (target / 'custom.txt').write_text('retain')
            with self.assertRaises(ValueError):
                m.check_skill_copies([('plugin', root / 'plugin')], root / 'opencode')
            self.assertEqual((target / 'custom.txt').read_text(), 'retain')

    def test_other_skill_directories_are_untouched(self):
        m = self.module()
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            target = Path(directory)
            (target / 'skills/unrelated').mkdir(parents=True)
            self.assertEqual(m.check_skill_copies([], target), [])
            (target / 'skills/subagents').mkdir()
            self.assertEqual(m.check_skill_copies([], target), [])
            self.assertTrue((target / 'skills/subagents').exists())


if __name__ == '__main__':
    unittest.main()
