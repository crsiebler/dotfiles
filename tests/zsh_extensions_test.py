"""Offline Zsh extension installs using project-local Git repositories."""

import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


class ZshExtensionsTest(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location(
            'zsh_extensions', ROOT / 'scripts/install-zsh-extensions.py')
        assert spec is not None and spec.loader is not None
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        scratch = tempfile.TemporaryDirectory(dir=ROOT / 'tests')
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        self.home = self.root / 'home'
        self.zsh = self.home / '.oh-my-zsh'
        self.zsh.mkdir(parents=True)
        (self.zsh / 'oh-my-zsh.sh').write_text('# fixture\n')
        env = {
            'HOME': str(self.home), 'PATH': os.environ['PATH'],
            'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
            'GIT_AUTHOR_NAME': 'Fixture', 'GIT_AUTHOR_EMAIL': 'fixture@example.invalid',
            'GIT_COMMITTER_NAME': 'Fixture', 'GIT_COMMITTER_EMAIL': 'fixture@example.invalid',
        }
        self.environment = patch.dict(os.environ, env, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.source = self.root / 'source'
        self.source.mkdir()
        subprocess.run(['git', 'init', '-q', str(self.source)], check=True)
        (self.source / 'sample.plugin.zsh').write_text('# original\n')
        subprocess.run(['git', '-C', str(self.source), 'add', '.'], check=True)
        subprocess.run(['git', '-C', str(self.source), 'commit', '-qm', 'fixture'], check=True)
        self.extensions = [('plugins/sample', str(self.source), 'sample.plugin.zsh')]

    def install(self):
        with patch.object(self.module, 'EXTENSIONS', self.extensions):
            self.module.main()

    def test_fresh_install_and_repeat_preserve_local_changes(self):
        self.install()
        installed = self.zsh / 'custom/plugins/sample/sample.plugin.zsh'
        self.assertEqual(installed.read_text(), '# original\n')
        installed.write_text('# local changes\n')
        with patch.object(self.module.subprocess, 'run', side_effect=AssertionError('must not fetch')):
            self.install()
        self.assertEqual(installed.read_text(), '# local changes\n')

    def test_custom_root_and_non_git_plugin_are_preserved(self):
        custom = self.root / 'custom with spaces'
        existing = custom / 'plugins/sample'
        existing.mkdir(parents=True)
        (existing / 'sample.plugin.zsh').write_text('# custom\n')
        with patch.dict(os.environ, {'ZSH_CUSTOM': str(custom)}):
            self.install()
        self.assertEqual((existing / 'sample.plugin.zsh').read_text(), '# custom\n')

    def test_conflicts_are_checked_before_any_clone(self):
        conflict = self.zsh / 'custom/themes/broken'
        conflict.mkdir(parents=True)
        (conflict / 'keep').write_text('preserve')
        self.extensions.append(('themes/broken', str(self.source), 'broken.zsh-theme'))
        with self.assertRaisesRegex(ValueError, 'existing.*themes/broken'):
            self.install()
        self.assertFalse((self.zsh / 'custom/plugins/sample').exists())
        self.assertEqual((conflict / 'keep').read_text(), 'preserve')

    def test_failed_clone_leaves_no_destination(self):
        self.extensions[0] = ('plugins/sample', str(self.root / 'missing'), 'sample.plugin.zsh')
        with self.assertRaisesRegex(ValueError, 'clone.*plugins/sample'):
            self.install()
        self.assertFalse((self.zsh / 'custom/plugins/sample').exists())
        self.assertEqual(list((self.zsh / 'custom/plugins').iterdir()), [])

    def test_missing_entrypoint_is_not_installed(self):
        self.extensions[0] = ('plugins/sample', str(self.source), 'absent.plugin.zsh')
        with self.assertRaisesRegex(ValueError, 'entry.*plugins/sample'):
            self.install()
        self.assertFalse((self.zsh / 'custom/plugins/sample').exists())

    def test_missing_framework_and_relative_custom_root(self):
        with patch.dict(os.environ, {'ZSH': str(self.root / 'absent')}):
            with self.assertRaisesRegex(ValueError, 'Oh My Zsh'):
                self.install()
        with patch.dict(os.environ, {'ZSH_CUSTOM': 'relative'}):
            with self.assertRaisesRegex(ValueError, 'absolute'):
                self.install()

    def test_missing_git_and_symlink_conflict_do_not_install(self):
        with patch.object(self.module.shutil, 'which', return_value=None):
            with self.assertRaisesRegex(ValueError, 'git is required'):
                self.install()
        target = self.zsh / 'custom/plugins/sample'
        target.parent.mkdir(parents=True)
        target.symlink_to(self.source, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.install()
        self.assertTrue(target.is_symlink())
        self.assertEqual((self.source / 'sample.plugin.zsh').read_text(), '# original\n')

    def test_configured_extension_origins(self):
        self.assertEqual({path for path, _, _ in self.module.EXTENSIONS}, {
            'plugins/opencode', 'plugins/gh', 'plugins/bun',
            'plugins/you-should-use', 'plugins/zsh-autosuggestions',
            'plugins/zsh-syntax-highlighting', 'themes/powerlevel10k',
        })
        origins = {path: url for path, url, _ in self.module.EXTENSIONS}
        self.assertEqual(origins['plugins/opencode'],
                         'https://github.com/crsiebler/omz-plugin-opencode.git')
        self.assertEqual(origins['plugins/gh'],
                         'https://github.com/crsiebler/omz-plugin-gh.git')


if __name__ == '__main__':
    unittest.main()
