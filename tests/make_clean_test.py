import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MakeCleanTest(unittest.TestCase):
    def run_clean(self, home):
        return subprocess.run(
            ['make', '-f', str(ROOT / 'Makefile'), 'clean'],
            cwd=ROOT,
            env=dict(os.environ, HOME=str(home), MAKEFLAGS='', MAKEOVERRIDES=''),
            capture_output=True, text=True,
        )

    def test_removes_only_zshrc_backups(self):
        with tempfile.TemporaryDirectory(prefix='clean home ', dir=ROOT / 'tests') as directory:
            home = Path(directory)
            backups = ['.zshrc.backup.20260906_120000']
            retained = ['.zshrc', '.env', '.env.backup.20260906_120000',
                        '.aliases.backup.20260906_120000',
                        '.config/opencode/opencode.json.backup.20260906_120000',
                        '.codex/config.toml.backup.20260906_120000',
                        '.config/opencode/.install-ai-backups/example/skills/custom/SKILL.md']
            for name in backups + retained:
                path = home / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('fixture')
            for _ in range(2):
                result = self.run_clean(home)
                self.assertEqual(result.returncode, 0, result.stderr)
                for name in backups:
                    self.assertFalse((home / name).exists())
                for name in retained:
                    self.assertEqual((home / name).read_text(), 'fixture')

    def test_rejects_empty_relative_and_root_home(self):
        for home in ('', 'relative-home', '/'):
            with self.subTest(home=home):
                result = self.run_clean(home)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('HOME', result.stderr)

    def test_install_plan_syncs_env_without_backing_it_up(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            result = subprocess.run(
                ['make', '-n', '-f', str(ROOT / 'Makefile'), 'install'],
                cwd=ROOT,
                env=dict(os.environ, HOME=directory, MAKEFLAGS='', MAKEOVERRIDES=''),
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('scripts/sync-env.py', result.stdout)
            self.assertIn('.zshrc.backup.', result.stdout)
            self.assertNotIn('.env.backup.', result.stdout)


if __name__ == '__main__':
    unittest.main()
