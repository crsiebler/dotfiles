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
SCRIPT = ROOT / 'ai/plugins/coding/skills/prepare-implementation/scripts/archive_run.py'
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
            'adapter': 'CodexGoalMarkdown', 'task_source': 'PLAN.md',
            'prds': ['tasks/prd-fixture.md'], 'journal': 'progress.md',
            'memory': 'memory.json', 'archive_on_completion': True,
        }
        self.record = {
            'version': 1, 'run_id': self.manifest['run_id'], 'story_id': 'US-001',
            'checks': [{'command': 'fixture-check', 'status': 'passed',
                        'evidence': 'Fixture check succeeded.'}],
            'review': {'verdict': 'pass', 'kind': 'native', 'role': 'story-reviewer',
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

    def test_preview_is_read_only(self):
        result = self.run_script('--dry-run')
        self.assertEqual(result['status'], 'preview')
        self.assertFalse((self.project / 'archive').exists())
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

    def test_ralph_archive_requires_completed_unlocked_runner(self):
        self.manifest.update(adapter='RalphJSON', task_source='plan.json')
        self.record['review']['role'] = 'ralph-reviewer'
        self.write_prd()
        self.write_record()
        self.write('plan.json', json.dumps({'project': 'fixture', 'branchName': 'feat/fixture',
                   'description': 'fixture', 'userStories': [{'id': 'US-001', 'passes': True}]}))
        self.commit('feat(fixture): complete Ralph story')
        control = self.project / '.git/ralph'
        control.mkdir()
        state = {'version': 1, 'status': 'running',
                 'expected_plan': json.loads((self.project / 'plan.json').read_text())}
        (control / 'state.json').write_text(json.dumps(state))
        self.run_script(expected=2)
        state['status'] = 'completed'
        expected_plan = state['expected_plan']
        state['expected_plan'] = dict(expected_plan, description='Another run')
        (control / 'state.json').write_text(json.dumps(state))
        self.run_script(expected=2)
        state['expected_plan'] = expected_plan
        (control / 'state.json').write_text(json.dumps(state))
        result = self.run_script()
        self.assertEqual(result['status'], 'archived')
        self.assertTrue((control / 'state.json').exists())
        self.assertTrue((self.project / 'PLAN.md').exists())

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

    def test_held_runner_lock_and_stop_file_block_archival(self):
        control = self.project / '.git/ralph'
        control.mkdir()
        with (control / 'lock').open('w') as stream:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.run_script(expected=2)
        self.write('.ralph-stop', 'Stop.\n')
        self.run_script(expected=2)
        self.assertTrue((self.project / '.ralph-stop').exists())

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
