"""Retirement ownership, archival, and CLI failure regression tests."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RetirementTest(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location(
            'retirement', ROOT / 'scripts/ai_retirement.py')
        assert spec and spec.loader
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT / 'tests')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.home = self.root / 'home'
        self.target = self.home / 'xdg/opencode'
        self.shared = self.home / '.agents/skills'
        self.source = self.root / 'repo'
        self.source.mkdir()

    def put(self, path, text='original'):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def manager(self, desired, legacy=None):
        return self.m.Skills(self.source, self.target, self.shared, desired,
                             legacy or {})

    def test_retired_shared_skill_archived_then_cli_and_repeat(self):
        skill = self.put(self.shared / 'old/SKILL.md')
        hashes = self.m.fingerprint(skill.parent)
        first = self.manager({'old': hashes})
        first.record()
        unrelated = self.put(self.shared / 'personal/SKILL.md')
        second = self.manager({})
        second.prepare()
        self.assertEqual([p.name for p in second.retired], ['old'])
        calls = []

        def remove(argv):
            self.assertFalse(skill.exists())
            self.assertTrue(list(self.target.glob('.install-ai-backups/*/retired/shared/old/SKILL.md')))
            calls.append(argv)

        second.apply(remove)
        second.record()
        self.assertEqual(calls, [['skills', 'remove', 'old', '--global',
                                  '--agent', 'opencode', '--yes']])
        self.assertEqual(unrelated.read_text(), 'original')
        again = self.manager({})
        again.prepare()
        self.assertEqual(again.retired, {})

    def test_legacy_requires_exact_tree_and_current_skill_is_never_retired(self):
        old = self.put(self.shared / 'old/SKILL.md')
        hashes = self.m.fingerprint(old.parent)
        manager = self.manager({'current': hashes}, {'old': [hashes], 'current': [hashes]})
        self.put(self.shared / 'current/SKILL.md')
        self.put(old.parent / 'custom.txt', 'custom')
        manager.prepare()
        self.assertFalse(manager.retired)
        self.assertTrue(manager.conflicts)
        self.assertTrue(old.exists())

    def test_modified_or_symlinked_retirement_is_preserved(self):
        old = self.put(self.shared / 'old/SKILL.md')
        first = self.manager({'old': self.m.fingerprint(old.parent)})
        first.record()
        old.write_text('customized')
        second = self.manager({})
        second.prepare()
        self.assertTrue(second.conflicts)
        self.assertFalse(second.retired)
        old.unlink()
        old.symlink_to(self.put(self.root / 'outside', 'keep'))
        third = self.manager({})
        third.prepare()
        self.assertTrue(third.conflicts)
        self.assertFalse(third.retired)

    def test_changed_after_preflight_and_failed_cli_leave_retryable_state(self):
        old = self.put(self.shared / 'old/SKILL.md')
        first = self.manager({'old': self.m.fingerprint(old.parent)})
        first.record()
        manager = self.manager({})
        manager.prepare()
        old.write_text('changed')
        with self.assertRaisesRegex(ValueError, 'changed'):
            manager.apply(lambda argv: self.fail('must not invoke CLI'))
        old.write_text('original')
        manager.prepare()
        with self.assertRaisesRegex(ValueError, 'CLI failed'):
            manager.apply(lambda argv: (_ for _ in ()).throw(ValueError('CLI failed')))
        retry = self.manager({})
        retry.prepare()
        calls = []
        retry.apply(calls.append)
        self.assertTrue(calls, 'missing directory must not lose pending CLI cleanup')
        retry.record()

    def test_invalid_inventory_blocks_without_overwrite(self):
        manager = self.manager({})
        self.put(manager.state_path, '{broken')
        with self.assertRaisesRegex(ValueError, 'inventory'):
            manager.prepare()
        self.assertEqual(manager.state_path.read_text(), '{broken')

    def test_invalid_cli_lock_blocks_before_archival(self):
        old = self.put(self.shared / 'old/SKILL.md')
        manager = self.manager({}, {'old': [self.m.fingerprint(old.parent)]})
        self.put(manager.lock_path, '{broken')
        with self.assertRaisesRegex(ValueError, 'CLI lock'):
            manager.prepare()
        self.assertTrue(old.exists())

    def test_bundle_move_preserves_current_name(self):
        old = self.put(self.shared / 'moving/SKILL.md')
        hashes = self.m.fingerprint(old.parent)
        self.manager({'moving': hashes}).record()
        moved = self.manager({'moving': hashes})
        moved.prepare()
        self.assertFalse(moved.retired)

    def test_copy_fingerprint_excludes_only_cli_omissions(self):
        source = self.source / 'skill'
        self.put(source / 'SKILL.md')
        self.put(source / 'scripts/helper.py', 'code')
        for name in ('.git', '__pycache__', '__pypackages__', 'metadata.json'):
            self.put(source / 'scripts' / name / 'nested/file', 'omitted')
        self.put(source / 'metadata.json', 'omitted')
        # These names are excluded only when they are directories.
        self.put(source / '__pycache__', 'ordinary file')
        self.put(source / '.hidden', 'retained')
        expected = self.m.skill_copy_fingerprint(source)
        self.assertEqual(set(expected), {'SKILL.md', 'scripts/', 'scripts/helper.py',
                                        '__pycache__', '.hidden'})
        self.assertIn('scripts/__pycache__/nested/file', self.m.fingerprint(source))

    def test_generated_installed_cache_does_not_weaken_retirement_ownership(self):
        installed = self.put(self.shared / 'old/SKILL.md')
        self.manager({'old': self.m.fingerprint(installed.parent)}).record()
        self.put(installed.parent / '__pycache__/custom.pyc', 'keep')
        manager = self.manager({})
        manager.prepare()
        self.assertFalse(manager.retired)
        self.assertTrue(manager.conflicts)
        self.assertTrue(installed.exists())

    def test_record_preserves_current_unowned_shared_symlink(self):
        installed = self.put(self.target / 'skills/current/SKILL.md')
        self.shared.mkdir(parents=True)
        (self.shared / 'current').symlink_to(installed.parent, target_is_directory=True)
        manager = self.manager({'current': self.m.fingerprint(installed.parent)})
        manager.prepare()
        manager.record(verify=True)
        self.assertTrue((self.shared / 'current').is_symlink())

    def test_native_only_removes_recorded_missing_plugin_with_same_source(self):
        desired = [('keep', self.source / 'ai/plugins/keep')]
        self.put(desired[0][1] / '.codex-plugin/plugin.json', '{"name":"keep"}')
        old = self.source / 'ai/plugins/old'
        self.put(old / '.codex-plugin/plugin.json', '{"name":"old"}')
        native = self.m.Plugins(self.source, self.home / 'codex', 'craft', desired + [('old', old)])
        native.record()
        manager = self.m.Plugins(self.source, self.home / 'codex', 'craft', desired)
        self.put(self.home / 'codex/plugins/cache/craft/old/custom.txt', 'custom cache')
        rows = [{'pluginId': 'old@craft', 'source': {'source': 'local', 'path': str(old)}},
                {'pluginId': 'personal@craft', 'source': {'source': 'local', 'path': '/personal'}}]
        manager.prepare(rows)
        self.assertEqual(manager.retired, ['old@craft'])
        calls = []

        def execute(argv):
            calls.append(argv)
            if argv[1:3] == ['plugin', 'remove']:
                rows.pop(0)
            return json.dumps({'installed': rows})

        manager.apply(execute)
        manager.record()
        self.assertIn(['codex', 'plugin', 'remove', 'old@craft'], calls)
        self.assertEqual(rows[0]['pluginId'], 'personal@craft')
        backups = list((self.home / 'codex').glob('.install-ai-backups/*/retired/plugins/old/custom.txt'))
        self.assertEqual(backups[0].read_text(), 'custom cache')

    def test_native_source_conflict_and_false_success_preserve_inventory(self):
        old = self.source / 'ai/plugins/old'
        self.put(old / 'SKILL.md')
        self.m.Plugins(self.source, self.home / 'codex', 'craft', [('old', old)]).record()
        manager = self.m.Plugins(self.source, self.home / 'codex', 'craft', [])
        rows = [{'pluginId': 'old@craft', 'source': {'source': 'local', 'path': '/different'}}]
        with self.assertRaisesRegex(ValueError, 'source conflict'):
            manager.prepare(rows)
        rows[0]['source']['path'] = str(old)
        manager.prepare(rows)
        before = manager.state_path.read_bytes()
        with self.assertRaisesRegex(ValueError, 'did not complete'):
            manager.apply(lambda argv: json.dumps({'installed': rows}))
        self.assertEqual(manager.state_path.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
