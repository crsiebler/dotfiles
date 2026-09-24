"""Offline native Codex plugin contract test; never starts a model or MCP."""
import json
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('codex'), 'Codex CLI not installed')
class NativePluginTest(unittest.TestCase):
    def test_local_marketplace_add_and_repeat(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            root = Path(directory)
            home = root / 'home'
            home.mkdir()
            (home / 'codex').mkdir()
            env = {'HOME': str(home), 'CODEX_HOME': str(home / 'codex'),
                   'XDG_CONFIG_HOME': str(home / 'xdg'), 'TMPDIR': str(root),
                   'PATH': os.environ['PATH']}
            def run(*argv):
                result = subprocess.run(['codex', *argv], cwd=root, env=env,
                                        capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stderr)
                return result.stdout
            if run('--version').strip() != 'codex-cli 0.153.4':
                self.skipTest('native contract targets Codex 0.153.4')
            manifest = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text())
            target = root / '.agents/plugins'
            target.mkdir(parents=True)
            (target / 'marketplace.json').write_text(json.dumps(manifest))
            for plugin in manifest['plugins']:
                source = ROOT / plugin['source']['path'] / '.codex-plugin/plugin.json'
                target = root / plugin['source']['path'] / '.codex-plugin'
                target.mkdir(parents=True)
                (target / 'plugin.json').write_bytes(source.read_bytes())
                shutil.copytree(ROOT / plugin['source']['path'] / 'skills',
                                target.parent / 'skills')
            for _ in range(2):
                run('plugin', 'marketplace', 'add', str(root))
                for plugin in manifest['plugins']:
                    run('plugin', 'add', plugin['name'] + '@' + manifest['name'])
            listing = json.loads(run('plugin', 'list', '--marketplace', manifest['name'], '--json'))
            self.assertEqual({p['pluginId'] for p in listing['installed']},
                             {p['name'] + '@' + manifest['name'] for p in manifest['plugins']})
            self.assertTrue(all(p['source']['source'] == 'local' for p in listing['installed']))
            spec = importlib.util.spec_from_file_location('retirement', ROOT / 'scripts/ai_retirement.py')
            assert spec and spec.loader
            retirement = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(retirement)
            desired = [(p['name'], root / p['source']['path']) for p in manifest['plugins']]
            manager = retirement.Plugins(root, home / 'codex', manifest['name'], desired)
            manager.prepare(listing['installed'])
            manager.record()
            removed, retained = desired[-1], desired[:-1]
            manifest['plugins'] = manifest['plugins'][:-1]
            (root / '.agents/plugins/marketplace.json').write_text(json.dumps(manifest))
            run('plugin', 'marketplace', 'add', str(root))
            manager = retirement.Plugins(root, home / 'codex', manifest['name'], retained)
            manager.prepare(json.loads(run('plugin', 'list', '--marketplace', manifest['name'], '--json'))['installed'])
            manager.apply(lambda argv: run(*argv[1:]))
            manager.record()
            after = json.loads(run('plugin', 'list', '--marketplace', manifest['name'], '--json'))
            self.assertNotIn(removed[0] + '@' + manifest['name'], {p['pluginId'] for p in after['installed']})
            self.assertEqual(len(after['installed']), len(retained))


if __name__ == '__main__':
    unittest.main()
