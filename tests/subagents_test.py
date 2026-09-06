import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / 'ai/plugins/delegating/skills/use-subagents/scripts/subagents'


class SubagentsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'tests')
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.env = dict(os.environ, HOME=str(self.home),
                        CODEX_HOME=str(self.home / 'codex'),
                        XDG_CONFIG_HOME=str(self.home / 'xdg'))

    def run_cli(self, *args):
        return subprocess.run(['sh', str(HELPER), '--project', str(self.home), *args],
                              env=self.env, cwd=self.home,
                              capture_output=True, text=True)

    def agent(self, path, text):
        file = self.home / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text)

    def test_fetch_full_and_xdg(self):
        text = '---\ndescription: Test\n---\n' + 'line\n' * 200
        self.agent('xdg/opencode/agents/test.md', text)
        result = self.run_cli('--harness', 'opencode', 'fetch', 'test')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, text)

    def test_duplicate_requires_scope(self):
        self.agent('xdg/opencode/agents/test.md', 'global')
        self.agent('.opencode/agents/test.md', 'project')
        result = self.run_cli('--harness', 'opencode', 'fetch', 'test')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('--scope', result.stderr)
        result = self.run_cli('--harness', 'opencode', '--scope', 'project', 'fetch', 'test')
        self.assertEqual(result.stdout, 'project')

    def test_codex_toml(self):
        text = 'name = "tester"\ndescription = "Native specialist"\n'
        self.agent('codex/agents/test.toml', text)
        result = self.run_cli('--harness', 'codex', 'fetch', 'tester')
        self.assertEqual(result.stdout, text)
        self.assertIn('static', self.run_cli('--harness', 'codex', 'list').stdout)

    def test_strict_arguments(self):
        for args in [('list', 'extra'), ('fetch',), ('search', ''), ('fetch', '../test')]:
            self.assertNotEqual(self.run_cli(*args).returncode, 0)

    def test_dotted_logical_names_fetch_complete_definitions(self):
        for name in ('dotnet-framework-4.8-expert', 'future-noncoding.role'):
            with self.subTest(name=name):
                markdown = f'---\nname: {name}\n---\nComplete definition\n'
                native = f'name = "{name}"\ndeveloper_instructions = "Complete definition"\n'
                self.agent(f'xdg/opencode/agents/{name}.md', markdown)
                # Resolve metadata names too; never construct a path from input.
                self.agent('codex/agents/fixture.toml', native)
                for harness, expected in [('opencode', markdown), ('codex', native)]:
                    result = self.run_cli('--harness', harness, 'fetch', name)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout, expected)

    def test_logical_name_rejects_paths_and_invalid_first_character(self):
        for name in ('../test', 'test/other', 'test\\other', '.hidden', '_hidden', '-hidden', 'éxpert'):
            result = self.run_cli('--harness', 'codex', 'fetch', '--', name)
            self.assertEqual(result.returncode, 2, name)


if __name__ == '__main__':
    unittest.main()
