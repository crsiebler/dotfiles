"""Real Git/filesystem archival fixtures; no installed or active run is touched."""

import fcntl
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'ai/plugins/coding/skills/archive-run/scripts/archive_run.py'
sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location('archive_run', SCRIPT)
ARCHIVE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ARCHIVE)


class ArchiveRunTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT / 'tests')
        self.addCleanup(self.temporary.cleanup)
        self.project = Path(self.temporary.name)
        self.git('init', '-q', '--initial-branch=feat/fixture')
        self.manifest = {
            'version': 1, 'run_id': 'fixture-20261003', 'feature': 'fixture',
            'adapter': 'MarkdownPlan', 'task_source': 'PLAN.md',
            'prds': ['tasks/prd-fixture.md'], 'journal': 'progress.md',
            'memory': 'memory.json', 'archive_on_completion': True,
        }
        self.record = {
            'version': 1, 'run_id': self.manifest['run_id'], 'story_id': 'US-001',
            'checks': [{'command': 'fixture-check', 'status': 'passed',
                        'evidence': 'Fixture check succeeded.'}],
            'review': {'verdict': 'pass', 'kind': 'native', 'role': 'code-reviewer',
                       'session_id': 'fixture-session', 'evidence': 'Passing fixture review.'},
        }
        self.write('PLAN.md', '# Fixture\n\n### US-001 - Fixture story\n- [x] Story complete\n')
        self.write_prd()
        self.write_record()
        self.write('memory.json', json.dumps({'version': 1, 'patterns': [], 'suppressions': []}))
        self.write('unrelated.md', 'Preserve this file.\n')
        self.commit('feat(fixture): complete story')

    def git(self, *args, check=True):
        return subprocess.run(['git', '-C', str(self.project), *args],
                              capture_output=True, check=check)

    def git_path(self, name):
        path = self.git('rev-parse', '--git-path', name).stdout.decode().strip()
        return self.project / path

    def write(self, name, value):
        path = self.project / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value)

    def write_prd(self, name='tasks/prd-fixture.md', manifest=None):
        data = self.manifest if manifest is None else manifest
        self.write(name, '# PRD: Fixture\n\n```work-run\n' + json.dumps(data) + '\n```\n')

    def write_record(self):
        self.write('progress.md', '# Progress\n\n```story-result\n' + json.dumps(self.record) + '\n```\n')

    def commit(self, message):
        self.git('add', '--all')
        self.git('-c', 'user.name=Archive Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '-q', '-m', message)

    def run_script(self, *args, prd='tasks/prd-fixture.md', expected=0):
        result = subprocess.run([sys.executable, str(SCRIPT), '--project', str(self.project),
                                 '--prd', prd, *args], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def preserve_plan(self, *args, expected=0):
        result = subprocess.run([sys.executable, str(SCRIPT), '--project', str(self.project),
                                 '--preserve-plan', 'PLAN.md', *args],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_plan_preservation_keeps_uncommitted_bytes_without_delivery_claim(self):
        self.write('PLAN.md', '# Old plan without structured history\n')
        self.write('progress.md', 'Historical evidence, not machine-readable.\n')
        sources = {name: (self.project / name).read_bytes() for name in
                   ('PLAN.md', 'progress.md', 'memory.json', 'tasks/prd-fixture.md')}
        result = self.preserve_plan('--include-prd', 'tasks/prd-fixture.md')
        self.assertEqual(result['status'], 'preserved')
        receipt_path = self.project / result['destination'] / '_preservation.json'
        receipt = json.loads(receipt_path.read_text())
        self.assertIs(receipt['delivery_verified'], False)
        self.assertNotIn('stories', receipt)
        self.assertEqual({item['source'] for item in receipt['files']}, set(sources))
        for name, data in sources.items():
            self.assertEqual((self.project / name).read_bytes(), data)
            self.assertEqual((receipt_path.parent / Path(name).name).read_bytes(), data)
        self.assertTrue((self.project / 'unrelated.md').exists())
        self.assertFalse((receipt_path.parent / '_archive.json').exists())

    def test_plan_preservation_preview_does_not_write(self):
        result = self.preserve_plan('--dry-run')
        self.assertEqual(result['status'], 'preview')
        self.assertFalse((self.project / 'archive').exists())
        self.assertFalse(self.git_path('archive-run.lock').exists())

    def test_plan_preservation_rejects_symlinks_and_flat_collisions(self):
        (self.project / 'PLAN.md').unlink()
        (self.project / 'PLAN.md').symlink_to('unrelated.md')
        self.preserve_plan(expected=2)
        self.assertFalse((self.project / 'archive').exists())
        (self.project / 'PLAN.md').unlink()
        self.write('PLAN.md', 'old plan')
        self.write('tasks/PLAN.md', 'unrelated duplicate')
        result = self.preserve_plan('--include-prd', 'tasks/PLAN.md', expected=2)
        self.assertIn('collision', result['reason'])
        self.assertFalse((self.project / 'archive').exists())

    def test_plan_preservation_works_without_optional_state_and_never_replaces_archive(self):
        (self.project / 'progress.md').unlink()
        (self.project / 'memory.json').unlink()
        result = self.preserve_plan('--dry-run')
        self.assertEqual([item['source'] for item in result['files']], ['PLAN.md'])
        directory = self.project / result['destination']
        directory.mkdir(parents=True)
        (directory / 'sentinel').write_text('retain existing archive')
        project = ARCHIVE.Project(self.project)
        self.addCleanup(project.close)
        with patch.object(ARCHIVE, 'datetime') as clock:
            clock.now.return_value.strftime.return_value = directory.name.removesuffix('-plan-preservation')
            with self.assertRaises(FileExistsError):
                ARCHIVE.preserve_plan(project, 'PLAN.md', [], False)
        self.assertEqual((directory / 'sentinel').read_text(), 'retain existing archive')
        self.assertTrue((self.project / 'PLAN.md').exists())


    def test_plan_preservation_rejects_changed_sources_without_removing_them(self):
        project = ARCHIVE.Project(self.project)
        self.addCleanup(project.close)
        original = project.write_new
        def change_source(name, data):
            original(name, data)
            if name.endswith('/PLAN.md'):
                self.write('PLAN.md', 'changed during preservation')
        with patch.object(project, 'write_new', side_effect=change_source):
            with self.assertRaises(ARCHIVE.Refusal):
                ARCHIVE.preserve_plan(project, 'PLAN.md', [], False)
        self.assertEqual((self.project / 'PLAN.md').read_text(), 'changed during preservation')
        self.assertTrue((self.project / 'progress.md').exists())
        self.assertFalse(list((self.project / 'archive').glob('*/_preservation.json')))

    def test_preview_is_read_only(self):
        result = self.run_script('--dry-run')
        self.assertEqual(result['status'], 'preview')
        self.assertFalse((self.project / 'archive').exists())
        self.assertFalse(self.git_path('archive-run.lock').exists())
        self.assertEqual(self.git('status', '--porcelain').stdout, b'')
        self.assertEqual(len(result['files']), 4)

    def test_isolated_skill_copy_executes_from_an_unrelated_working_directory(self):
        bundle = self.project / 'installed-skill'
        shutil.copytree(SCRIPT.parent.parent, bundle)
        before = {str(path.relative_to(bundle)): path.read_bytes()
                  for path in bundle.rglob('*') if path.is_file()}
        result = subprocess.run([sys.executable, str(bundle / 'scripts/archive_run.py'),
                                 '--project', str(self.project), '--prd', 'tasks/prd-fixture.md',
                                 '--dry-run'], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'preview')
        after = {str(path.relative_to(bundle)): path.read_bytes()
                 for path in bundle.rglob('*') if path.is_file()}
        self.assertEqual(before, after)

    def test_flat_archive_preserves_bytes_and_repeated_invocation_is_read_only(self):
        sources = {name: (self.project / name).read_bytes() for name in
                   ('tasks/prd-fixture.md', 'PLAN.md', 'progress.md', 'memory.json')}
        first = self.run_script()
        self.assertEqual(first['status'], 'archived')
        directory = self.project / first['destination']
        for name, contents in sources.items():
            self.assertEqual((directory / Path(name).name).read_bytes(), contents)
            self.assertFalse((self.project / name).exists())
        self.assertFalse((directory / 'tasks').exists())
        self.assertFalse((directory / 'docs').exists())
        self.assertTrue((self.project / 'unrelated.md').exists())
        receipt = json.loads((directory / '_archive.json').read_text())
        self.assertEqual(receipt['run_id'], self.manifest['run_id'])
        self.assertEqual(receipt['stories'][0]['commit'], self.git('rev-parse', 'HEAD').stdout.decode().strip())
        second = self.run_script()
        self.assertEqual(second['status'], 'already_archived')
        self.assertEqual(second['destination'], first['destination'])

    def test_closeout_commit_leaves_a_clean_worktree(self):
        result = self.run_script()
        paths = [item['source'] for item in result['files']]
        paths += [result['destination'] + '/' + item['name']
                  for item in result['files']]
        paths.append(result['destination'] + '/_archive.json')
        self.git('add', '--', *paths)
        self.git('-c', 'user.name=Archive Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '-q', '-m', 'chore(fixture): archive completed run')
        self.assertEqual(self.git('status', '--porcelain').stdout, b'')

    def test_held_archive_lock_preserves_sources_and_releases_after_use(self):
        lock = self.git_path('archive-run.lock')
        with lock.open('w') as stream:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = self.run_script(expected=2)
            self.assertEqual(result['reason'], 'another archive writer is active')
            self.assertTrue((self.project / 'PLAN.md').exists())
            self.assertFalse((self.project / 'archive').exists())
        self.assertEqual(self.run_script()['status'], 'archived')
        with lock.open('r') as stream:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def test_linked_worktree_has_an_independent_metadata_lock(self):
        temporary = tempfile.TemporaryDirectory(dir=ROOT / 'tests')
        self.addCleanup(temporary.cleanup)
        linked = Path(temporary.name) / 'linked'
        self.git('worktree', 'add', '-q', '-b', 'feat/linked', str(linked))
        original = self.project
        lock = self.git_path('archive-run.lock')
        try:
            self.project = linked
            linked_lock = self.git_path('archive-run.lock')
            self.assertNotEqual(lock, linked_lock)
            with lock.open('w') as stream:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
                result = self.run_script()
            self.assertEqual(result['status'], 'archived')
            self.assertTrue(linked_lock.is_file())
            self.assertFalse((linked / 'archive/.archive.lock').exists())
            self.assertTrue((original / 'PLAN.md').exists())
        finally:
            self.project = original

    def test_symlink_archive_lock_is_refused_without_touching_its_target(self):
        lock = self.git_path('archive-run.lock')
        target = self.project / 'unrelated.md'
        before = target.read_bytes()
        lock.symlink_to(target)
        self.run_script(expected=2)
        self.assertEqual(target.read_bytes(), before)
        self.assertTrue((self.project / 'PLAN.md').exists())
        self.assertFalse((self.project / 'archive').exists())


    def test_retired_adapter_is_rejected_without_touching_old_artifacts(self):
        self.manifest.update(adapter='RalphJSON', task_source='plan.json')
        self.write_prd()
        self.write('plan.json', '{"userStories":[]}')
        self.commit('test(fixture): legacy adapter')
        before = (self.project / 'plan.json').read_bytes()
        result = self.run_script(expected=2)
        self.assertEqual(result['reason'], 'unknown adapter')
        self.assertEqual((self.project / 'plan.json').read_bytes(), before)
        self.assertFalse((self.project / 'archive').exists())

    def test_legacy_markdown_provenance_remains_readable_without_relabeling(self):
        self.manifest['adapter'] = 'CodexGoalMarkdown'
        self.record['review']['role'] = 'story-reviewer'
        self.write_prd()
        self.write_record()
        self.commit('test(fixture): legacy provenance')
        result = self.run_script()
        receipt = json.loads((self.project / result['destination'] / '_archive.json').read_text())
        self.assertEqual(receipt['manifest']['adapter'], 'CodexGoalMarkdown')
        self.assertEqual(receipt['stories'][0]['result']['review']['role'], 'story-reviewer')

    def test_legacy_manifest_can_continue_with_generic_reviewer(self):
        self.manifest['adapter'] = 'CodexGoalMarkdown'
        self.write_prd()
        self.commit('test(fixture): continue legacy enrollment')
        result = self.run_script()
        self.assertEqual(result['status'], 'archived')
        self.assertEqual(result['stories'][0]['result']['review']['role'], 'code-reviewer')

    def test_new_adapter_requires_generic_reviewer_provenance(self):
        self.record['review']['role'] = 'story-reviewer'
        self.write_record()
        self.commit('test(fixture): mismatched review role')
        result = self.run_script(expected=2)
        self.assertEqual(result['reason'], 'missing required reviewer provenance')
        self.assertTrue((self.project / 'PLAN.md').exists())

    def test_core_reviewer_provenance_is_archived_without_relabeling(self):
        self.record['review']['role'] = 'reviewer'
        self.write_record()
        self.commit('test(fixture): core reviewer evidence')
        result = self.run_script()
        receipt = json.loads((self.project / result['destination'] / '_archive.json').read_text())
        self.assertEqual('reviewer', receipt['stories'][0]['result']['review']['role'])

    def test_auditor_cannot_substitute_for_delivery_reviewer(self):
        self.record['review']['role'] = 'auditor'
        self.write_record()
        self.commit('test(fixture): wrong responsibility')
        result = self.run_script(expected=2)
        self.assertEqual('missing required reviewer provenance', result['reason'])
        self.assertTrue((self.project / 'PLAN.md').exists())

    def test_plan_preservation_keeps_unrelated_legacy_data(self):
        self.write('.ralph-stop', 'historical data')
        result = self.preserve_plan()
        self.assertEqual(result['status'], 'preserved')
        self.assertEqual((self.project / '.ralph-stop').read_text(), 'historical data')
        self.assertNotIn('.ralph-stop', [item['source'] for item in result['files']])

    def test_incomplete_plan_or_failed_evidence_preserves_sources(self):
        self.write('PLAN.md', '### US-001 - Fixture story\n- [ ] Story complete\n')
        self.commit('test(fixture): incomplete task')
        self.run_script(expected=2)
        self.write('PLAN.md', '### US-001 - Fixture story\n- [x] Story complete\n')
        self.record['checks'][0]['status'] = 'failed'
        self.write_record()
        self.commit('test(fixture): failed check')
        self.run_script(expected=2)
        self.assertTrue((self.project / 'progress.md').exists())
        self.assertFalse((self.project / 'archive').exists())

    def test_uncommitted_evidence_and_missing_story_records_are_refused(self):
        self.write('progress.md', (self.project / 'progress.md').read_text() + 'Uncommitted evidence.\n')
        self.run_script(expected=2)
        self.write('progress.md', '# Progress without structured evidence\n')
        self.commit('test(fixture): missing record')
        self.run_script(expected=2)

    def test_escaping_paths_and_filename_collisions_are_refused(self):
        for value in ('../progress.md', '.git/config', 'archive/old.md'):
            with self.subTest(path=value):
                self.manifest['journal'] = value
                self.write_prd()
                self.commit('test(fixture): invalid journal path')
                self.run_script(expected=2)
        self.manifest['journal'] = 'progress.md'
        self.manifest['prds'].append('other/prd-fixture.md')
        self.write_prd()
        self.write_prd('other/prd-fixture.md')
        self.commit('test(fixture): conflicting flattened PRDs')
        self.run_script(expected=2)

    def test_symlink_prd_parent_and_disabled_archival_are_refused(self):
        self.manifest['archive_on_completion'] = False
        self.write_prd()
        self.commit('test(fixture): disable closeout')
        self.run_script(expected=2)
        self.manifest['archive_on_completion'] = True
        self.write_prd()
        self.commit('test(fixture): enable closeout')
        (self.project / 'linked').symlink_to(self.project / 'tasks', target_is_directory=True)
        self.run_script(prd='linked/prd-fixture.md', expected=2)

    def test_existing_archive_and_modified_receipt_do_not_authorize_cleanup(self):
        first = self.run_script()
        directory = self.project / first['destination']
        (directory / 'progress.md').write_text('Changed archive bytes.\n')
        self.run_script(expected=2)
        self.assertTrue((self.project / 'unrelated.md').exists())

    def test_no_git_writes_are_performed(self):
        before = self.git('rev-parse', 'HEAD').stdout
        self.run_script()
        self.assertEqual(self.git('rev-parse', 'HEAD').stdout, before)
        self.assertEqual(self.git('diff', '--cached', '--name-only').stdout, b'')

    def test_prior_run_history_at_reused_paths_is_not_current_evidence(self):
        self.record['run_id'] = self.manifest['run_id'] = 'next-fixture-20261003'
        self.write_prd()
        self.write_record()
        self.commit('feat(fixture): complete next run')
        result = self.run_script()
        self.assertEqual(result['stories'][0]['commit'],
                         self.git('rev-parse', 'HEAD').stdout.decode().strip())

    def test_optional_memory_and_custom_task_path_flattening(self):
        self.manifest['task_source'] = 'plans/feature.md'
        self.write('plans/feature.md', (self.project / 'PLAN.md').read_text())
        self.write_prd()
        (self.project / 'memory.json').unlink()
        self.commit('test(fixture): custom task path without memory')
        result = self.run_script()
        destination = self.project / result['destination']
        self.assertTrue((destination / 'feature.md').exists())
        self.assertFalse((destination / 'memory.json').exists())
        self.assertTrue((self.project / 'PLAN.md').exists())

    def test_staged_artifact_changes_are_not_removed(self):
        original = (self.project / 'progress.md').read_text()
        self.write('progress.md', original + 'Staged change.\n')
        self.git('add', 'progress.md')
        self.write('progress.md', original)
        self.run_script(expected=2)
        self.assertTrue((self.project / 'progress.md').exists())


    def test_copy_failure_preserves_every_source_and_pending_evidence(self):
        original = ARCHIVE.Project.write_new
        calls = []

        def failing_copy(project, name, contents):
            calls.append(name)
            if len(calls) == 2:
                raise OSError('Injected copy failure')
            original(project, name, contents)

        project = ARCHIVE.Project(str(self.project))
        try:
            with patch.object(ARCHIVE.Project, 'write_new', failing_copy):
                with self.assertRaises(OSError):
                    ARCHIVE.execute(project, 'tasks/prd-fixture.md', False)
        finally:
            project.close()
        for source in ('tasks/prd-fixture.md', 'PLAN.md', 'progress.md', 'memory.json'):
            self.assertTrue((self.project / source).exists())
        self.assertTrue((self.project / 'archive/.pending-fixture-20261003/prd-fixture.md').exists())
        self.run_script(expected=2)

    def test_partial_removal_stops_and_never_retries_cleanup(self):
        original = ARCHIVE.Project.unlink_verified
        calls = []

        def failing_removal(project, name, contents):
            calls.append(name)
            if len(calls) == 2:
                raise OSError('Injected removal failure')
            original(project, name, contents)

        project = ARCHIVE.Project(str(self.project))
        try:
            with patch.object(ARCHIVE.Project, 'unlink_verified', failing_removal):
                with self.assertRaises(OSError):
                    ARCHIVE.execute(project, 'tasks/prd-fixture.md', False)
        finally:
            project.close()
        self.assertFalse((self.project / 'tasks/prd-fixture.md').exists())
        self.assertTrue((self.project / 'PLAN.md').exists())
        self.run_script(expected=2)
        self.assertTrue((self.project / 'PLAN.md').exists())

    def test_archival_is_allowed_after_merge_on_main_or_detached_head(self):
        self.git('checkout', '-q', '-b', 'main')
        self.run_script('--dry-run')
        self.git('checkout', '-q', '--detach')
        self.assertEqual(self.run_script()['branch'], None)

    def test_invalid_memory_entries_and_duplicate_manifest_keys_are_refused(self):
        self.write('memory.json', json.dumps({'version': 1, 'patterns': ['invalid'], 'suppressions': []}))
        self.commit('test(fixture): malformed memory')
        self.run_script(expected=2)
        self.write('memory.json', json.dumps({'version': 1, 'patterns': [], 'suppressions': []}))
        text = json.dumps(self.manifest).replace('"version": 1', '"version": 1, "version": 1')
        self.write('tasks/prd-fixture.md', '```work-run\n' + text + '\n```\n')
        self.commit('test(fixture): duplicate manifest key')
        self.run_script(expected=2)

    def test_success_does_not_require_unrelated_work_to_be_clean(self):
        self.write('unrelated.md', 'Uncommitted user change.\n')
        self.git('add', 'unrelated.md')
        result = self.run_script()
        self.assertEqual(result['status'], 'archived')
        self.assertEqual((self.project / 'unrelated.md').read_text(), 'Uncommitted user change.\n')
        self.assertEqual(self.git('diff', '--cached', '--name-only').stdout, b'unrelated.md\n')

    def test_pending_and_completed_markers_map_to_their_actual_story_commits(self):
        first_commit = self.git('rev-parse', 'HEAD').stdout.decode().strip()
        self.write('PLAN.md', '### US-001 - Fixture story\n- [x] Story complete\n\n'
                   '### US-002 - Later story\n- [ ] Story complete\n')
        self.commit('feat(fixture): prepare second story')
        second = dict(self.record, story_id='US-002')
        self.write('PLAN.md', '### US-001 - Fixture story\n- [x] Story complete\n\n'
                   '### US-002 - Later story\n- [x] Story complete\n')
        self.write('progress.md', (self.project / 'progress.md').read_text() +
                   '\n```story-result\n' + json.dumps(second) + '\n```\n')
        self.commit('feat(fixture): deliver second story')
        result = self.run_script()
        self.assertEqual(result['stories'][0]['commit'], first_commit)
        self.assertEqual(result['stories'][1]['commit'],
                         self.git('rev-parse', 'HEAD').stdout.decode().strip())


if __name__ == '__main__':
    unittest.main()
