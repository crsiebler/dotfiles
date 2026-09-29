import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MakeCleanTest(unittest.TestCase):
    def run_clean(self, home, **overrides):
        return subprocess.run(
            ['make', '-f', str(ROOT / 'Makefile'), 'clean'],
            cwd=ROOT,
            env=dict(os.environ, HOME=str(home), CODEX_HOME=str(Path(home) / '.codex'),
                     XDG_CONFIG_HOME=str(Path(home) / '.config'),
                     MAKEFLAGS='', MAKEOVERRIDES='') | overrides,
            capture_output=True, text=True,
        )

    def test_removes_installer_backups_and_preserves_active_files(self):
        with tempfile.TemporaryDirectory(prefix='clean home ', dir=ROOT / 'tests') as directory:
            home = Path(directory)
            backups = ['.zshrc.backup.20260906_120000',
                       '.config/opencode/opencode.json.backup.20260906_120000_123456',
                       '.config/opencode/agents/retired.md.backup.20260906_120000',
                       '.config/opencode/commands/group/old.md.backup.20260906_120000',
                       '.codex/config.toml.backup.20260906_120000',
                       '.codex/agents/old.toml.backup.20260906_120000',
                       '.config/opencode/.install-ai-backups/20260906_120000_123456/skills/custom/SKILL.md',
                       '.codex/.install-ai-backups/20260906_120000/retired/plugins/old/plugin.json',
                       '.codex/.install-ai-backups/plugin-sources/coding/' + 'a' * 64 + '/SKILL.md']
            retained = ['.zshrc', '.env', '.env.backup.20260906_120000',
                        '.aliases.backup.20260906_120000',
                        '.config/opencode/opencode.json', '.codex/config.toml',
                        '.config/opencode/.install-ai-skills.json',
                        '.codex/plugins/cache/craft/coding/SKILL.md',
                        '.config/opencode/custom.json.backup.20260906_120000',
                        '.codex/config.toml.backup.manual',
                        '.ralph-stop', 'memory.json',
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

    def test_custom_roots_and_symlinks_preserve_external_files(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            home = Path(directory)
            codex = home / 'custom codex'
            xdg = home / 'custom xdg'
            codex.mkdir()
            (xdg / 'opencode').mkdir(parents=True)
            backup = codex / 'config.toml.backup.20260906_120000'
            backup.write_text('old')
            external = home / 'outside'
            external.mkdir()
            sentinel = external / 'role.md.backup.20260906_120000'
            sentinel.write_text('keep')
            (xdg / 'opencode/agents').symlink_to(external, target_is_directory=True)
            linked = codex / 'astra.config.toml.backup.20260906_120000'
            linked.symlink_to(sentinel)
            archive = codex / '.install-ai-backups/20260906_120000'
            archive.mkdir(parents=True)
            (archive / 'external').symlink_to(external, target_is_directory=True)
            result = self.run_clean(home, CODEX_HOME=str(codex), XDG_CONFIG_HOME=str(xdg))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(backup.exists())
            self.assertFalse(archive.exists())
            self.assertTrue(linked.is_symlink())
            self.assertEqual(sentinel.read_text(), 'keep')

    def test_invalid_ai_roots_fail_before_any_deletion(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            home = Path(directory)
            backup = home / '.zshrc.backup.20260906_120000'
            backup.write_text('keep')
            real = home / 'real'
            real.mkdir()
            link = home / 'linked'
            link.symlink_to(real, target_is_directory=True)
            for key in ('CODEX_HOME', 'XDG_CONFIG_HOME'):
                for value in ('', '/', 'relative', str(link)):
                    with self.subTest(key=key, value=value):
                        result = self.run_clean(home, **{key: value})
                        self.assertNotEqual(result.returncode, 0)
                        self.assertEqual(backup.read_text(), 'keep')

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
            self.assertLess(result.stdout.index('scripts/install-zsh-extensions.py'),
                            result.stdout.index('.zshrc.backup.'))


if __name__ == '__main__':
    unittest.main()
