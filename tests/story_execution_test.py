"""Workflow safeguard invariants; no live agent/model enforcement claims."""

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
TEAM = ROOT / 'ai/plugins/coding/skills/run-agent-team'
TEAM_REFS = TEAM / 'references'
RALPH = ROOT / 'ai/opencode/agents/ralph.md'
REVIEWER = ROOT / 'ai/opencode/agents/ralph-reviewer.md'
ARCHIVE = ROOT / 'ai/plugins/coding/skills/archive-run'


def marked(text, name):
    begin, end = f'<!-- BEGIN {name} -->', f'<!-- END {name} -->'
    assert text.count(begin) == text.count(end) == 1
    return text.split(begin, 1)[1].split(end, 1)[0].strip()


def examples(text, language='json'):
    return [json.loads(value) for value in re.findall(
        rf'```{language}\n(.*?)\n```', text, re.S)]


def compact(text):
    return ' '.join(text.split())


class StoryExecutionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lives = {'team': (TEAM_REFS / 'story-execution.md').read_text(),
                     'ralph': RALPH.read_text()}
        cls.protocols = {'team': (TEAM_REFS / 'story-review.md').read_text(),
                         'ralph': marked(REVIEWER.read_text(), 'RALPH REVIEW PROTOCOL')}

    def test_workflows_own_distinct_complete_protocols_with_compatible_schema(self):
        schemas = {name: examples(text) for name, text in self.protocols.items()}
        self.assertTrue(all(len(values) == 1 for values in schemas.values()))
        self.assertEqual(schemas['team'][0], schemas['ralph'][0])
        schema = schemas['team'][0]
        self.assertEqual(set(schema), {
            'verdict', 'pass_type', 'findings', 'resolved_findings',
            'executor_feedback', 'residual_risks', 'learning_candidates'})
        self.assertEqual(set(schema['findings'][0]), {
            'id', 'severity', 'lens', 'title', 'body', 'path', 'line',
            'acceptance_criterion', 'remediation', 'verification', 'confidence'})
        for name, text in self.protocols.items():
            with self.subTest(workflow=name):
                self.assertIn('All listed keys are required', text)
                self.assertIn('must explain missing input in', text)
                self.assertIn('Never return `pass` with unresolved', text)
        self.assertNotEqual(self.protocols['team'], self.protocols['ralph'])

    def test_each_workflow_has_only_its_own_profile_and_native_role(self):
        for name, profile, role, other in (
            ('team', 'expanded-initial', 'story-reviewer', 'three-step'),
            ('ralph', 'three-step', 'ralph-reviewer', 'expanded-initial')):
            text = self.protocols[name]
            self.assertIn(f'Review profile: {profile}', text)
            self.assertIn(role, text)
            self.assertNotIn(other, text)
            self.assertIn('missing, unknown, or conflicting profile', compact(text))
            self.assertIn('Do not infer the harness', text)
        codex = tomllib.loads((ROOT / 'ai/codex/agents/story-reviewer.toml').read_text())
        self.assertEqual(codex['sandbox_mode'], 'read-only')
        self.assertIn('run-agent-team', codex['developer_instructions'])
        self.assertNotIn('story-delivery', codex['developer_instructions'])

    def test_initial_and_targeted_budgets_are_workflow_specific(self):
        codex, ralph = (compact(self.protocols[key]) for key in ('team', 'ralph'))
        self.assertIn('permit up to 40 small, read-only evidence-gathering calls', codex)
        self.assertIn('Count each call separately', codex)
        self.assertIn('40 calls is a ceiling, not a target', codex)
        self.assertIn('at most one evidence-recovery tool turn', ralph)
        self.assertIn('steps: 3', ralph)
        self.assertNotIn('40 calls', ralph)
        for text in (codex, ralph):
            self.assertIn('at most two evidence-gathering tool turns', text)
            self.assertIn('one initial pass and at most one targeted remediation pass', text)
            self.assertIn('same actual native session', text)
            self.assertIn('Do not broaden a targeted pass into a fresh audit', text)

    def test_evidence_recovery_retains_staged_authority_and_hard_boundaries(self):
        for name, raw in self.protocols.items():
            text = compact(raw)
            with self.subTest(workflow=name):
                for safeguard in (
                    'before patch reads', 'internal coverage checklist',
                    'not a file or an added JSON field',
                    'retrieve only missing sections', 'same oversized request',
                    'cannot replace missing authoritative staged evidence',
                    'unlisted shell commands, pipelines, or external reads',
                    'Do not spend a targeted pass retrying a blocked initial review',
                    'No MCP, external-directory, credential-store, or network access',
                    'Do not edit files, run checks, browse, fetch documentation, delegate work, stage changes, commit',
                ):
                    self.assertIn(safeguard, text)

    def test_final_blockers_cannot_reset_or_turn_into_targeted_reviews(self):
        for name, protocol in self.protocols.items():
            text = compact(protocol)
            with self.subTest(workflow=name):
                self.assertIn('A final `blocked` verdict ends this review', text)
                self.assertIn('A blocked initial review cannot become a targeted pass', text)
                self.assertIn('replacement reviewer', text)
                self.assertIn('specific blocker, what must change', text)
        for name, raw in self.lives.items():
            text = compact(raw)
            with self.subTest(workflow=name):
                self.assertIn('Preserve', text)
                self.assertIn('consumed passes', text)
                self.assertIn('materially', text)
                self.assertIn('blocker', text)
        self.assertIn('persisted recovery counters', compact(self.lives['ralph']))
        self.assertIn('does not resolve a blocker or reset the review budget',
                      compact(self.lives['team']))

    def test_executor_packets_require_complete_protocol_and_native_session_identity(self):
        for name, raw in self.lives.items():
            text = compact(raw)
            with self.subTest(workflow=name):
                for safeguard in (
                    'actual invocation message', 'complete, unabridged protocol',
                    'Do not substitute a path, link, summary, parent tool-output reference',
                    'current candidate', 'fresh reviewer session for each story',
                    'recorded story/attempt/session mapping',
                    'Never substitute `code-reviewer`',
                ):
                    self.assertIn(safeguard, text)
        self.assertIn('BEGIN RALPH REVIEW PROTOCOL', self.lives['ralph'])
        self.assertIn('actual installed ralph-reviewer definition', self.lives['ralph'])
        self.assertNotIn('run-agent-team', self.lives['ralph'])
        self.assertNotIn('story-delivery', self.lives['ralph'])

    def test_native_definition_fetch_preserves_full_packet_and_rejects_duplicates(self):
        helper = ROOT / 'ai/plugins/delegating/skills/use-subagents/scripts/subagents.py'
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            scratch = Path(directory)
            home, project = scratch / 'home', scratch / 'project'
            agents = home / '.config/opencode/agents'
            agents.mkdir(parents=True)
            project.mkdir()
            (agents / 'ralph-reviewer.md').write_bytes(REVIEWER.read_bytes())
            env = dict(os.environ, HOME=str(home), XDG_CONFIG_HOME=str(home / '.config'))
            argv = [sys.executable, str(helper), '--harness', 'opencode',
                    '--project', str(project), 'fetch', 'ralph-reviewer']
            result = subprocess.run(argv, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(marked(result.stdout, 'RALPH REVIEW PROTOCOL'),
                             self.protocols['ralph'])
            local = project / '.opencode/agents'
            local.mkdir(parents=True)
            (local / 'ralph-reviewer.md').write_bytes(REVIEWER.read_bytes())
            duplicate = subprocess.run(argv, env=env, capture_output=True, text=True)
            self.assertNotEqual(duplicate.returncode, 0)
            self.assertIn('duplicate definitions', duplicate.stderr)

    def test_memory_schema_and_bounds_remain_compatible(self):
        shapes = {}
        for name, text in self.lives.items():
            memory = text.split('## Bounded memory and durable knowledge', 1)[1].split(
                '## Progress and commit finalization', 1)[0]
            shapes[name] = examples(memory)[0]
            self.assertIn('at most 20 patterns and 20 suppressions', compact(memory))
            self.assertIn('Invalid/unreadable memory blocks', memory)
            self.assertIn('Count an event only once', memory)
            self.assertIn('do not read/create the missing file', memory)
            self.assertIn('only after passing review', memory)
        self.assertEqual(shapes['team'], shapes['ralph'])
        self.assertEqual(set(shapes['team']), {'version', 'patterns', 'suppressions'})
        pattern = shapes['team']['patterns'][0]
        self.assertEqual(pattern['evidence_count'],
                         pattern['accepted_count'] + pattern['rejected_count'])

    def test_mode_risk_budgets_do_not_drift_between_workflows(self):
        tables = {}
        for name, text in self.lives.items():
            tables[name] = re.findall(r'\| Mode \|.*?(?=\n\n)', text, re.S)
            self.assertIn('Never invoke more than two implementation advisors', text)
        self.assertEqual(len(tables['team']), 2)
        self.assertEqual(tables['team'], tables['ralph'])

    def test_finalization_and_sensitive_operation_guards_remain_in_each_workflow(self):
        for name, raw in self.lives.items():
            text = compact(raw)
            with self.subTest(workflow=name):
                for safeguard in (
                    'Reject detached HEAD, `main`, and `master`',
                    'exact equality with the required branch',
                    'including local/test operations, need explicit approval',
                    'no unrelated staged work',
                    'This marker is not delivery until commit succeeds',
                    'restore that scoped marker', 'Commit status: not_attempted',
                    'If commit fails, do not claim delivery',
                    'without retrying, amending, bypassing hooks, or broad reset',
                    'only after passing review', 'same story commit',
                ):
                    self.assertIn(safeguard, text)

    def test_ralph_control_outcomes_and_serial_authority_remain_local(self):
        control = marked(self.lives['ralph'], 'RALPH RUNNER CONTROL')
        outcomes = examples(control)
        self.assertEqual([value['status'] for value in outcomes],
                         ['completed', 'retryable', 'blocked'])
        for value in outcomes:
            self.assertEqual(value['version'], 1)
            self.assertTrue(value['iteration_id'] and value['story_id'])
        self.assertIn('one story at a time', self.lives['ralph'])
        self.assertIn('never select another independently', compact(self.lives['ralph']))
        self.assertIn('Ralph never creates, switches, or repairs a branch', self.lives['ralph'])
        self.assertIn('validates Python 3.11+', control)
        self.assertNotIn('resolves `python3.11`', control)
        self.assertNotIn('RALPH RUNNER CONTROL', self.lives['team'])
        self.assertNotIn('ralph-control.md', self.lives['team'])

    def test_archival_shares_only_executable_capability_and_enrolls_at_execution(self):
        self.assertFalse((ROOT / 'ai/plugins/coding/skills/story-delivery').exists())
        contract = (ARCHIVE / 'references/completed-run-archive.md').read_text()
        self.assertNotIn('Planning owns', contract)
        self.assertIn('authorized execution owner', compact(contract))
        self.assertIn('first execution checkpoint', compact(contract))
        manifest = examples(contract, 'work-run')[0]
        self.assertEqual(manifest['journal'], 'progress.md')
        self.assertEqual(manifest['memory'], 'memory.json')
        self.assertTrue((ARCHIVE / 'scripts/archive_run.py').is_file())
        for text in self.lives.values():
            self.assertIn('installed archive-run', text)
            self.assertIn('--preserve-plan', text)

    def concurrency_reference(self):
        text = (TEAM_REFS / 'task-concurrency.md').read_text()
        code = text.split('```python\n', 1)[1].split('\n```', 1)[0]
        namespace = {}
        exec(compile(code, str(TEAM_REFS / 'task-concurrency.md'), 'exec'), namespace)
        return namespace

    def test_dependency_readiness_uses_delivered_predecessors_and_stable_order(self):
        ready = self.concurrency_reference()['ready_story_ids']
        stories = [
            {'id': 'C', 'priority': 2, 'depends_on': ['A']},
            {'id': 'A', 'priority': 1, 'depends_on': []},
            {'id': 'B', 'priority': 1, 'depends_on': []},
            {'id': 'D', 'priority': 3, 'depends_on': ['B', 'C']},
        ]
        self.assertEqual(ready(stories, []), ['A', 'B'])
        self.assertEqual(ready(stories, ['A']), ['B', 'C'])
        self.assertEqual(ready(stories, ['A', 'B', 'C']), ['D'])
        self.assertEqual(ready(stories, ['A', 'B', 'C', 'D']), [])

    def test_dependency_graph_rejects_missing_duplicate_and_cyclic_references(self):
        ready = self.concurrency_reference()['ready_story_ids']
        invalid = [
            [{'id': 'A', 'priority': 1, 'depends_on': ['missing']}],
            [{'id': 'A', 'priority': 1, 'depends_on': ['A']}],
            [{'id': 'A', 'priority': 1, 'depends_on': ['B']},
             {'id': 'B', 'priority': 2, 'depends_on': ['A']}],
            [{'id': 'A', 'priority': 1, 'depends_on': []},
             {'id': 'A', 'priority': 2, 'depends_on': []}],
            [{'id': 'A', 'priority': 1, 'depends_on': []},
             {'id': 'B', 'priority': 2, 'depends_on': ['A', 'A']}],
        ]
        for stories in invalid:
            with self.subTest(stories=stories), self.assertRaises(ValueError):
                ready(stories, [])
        with self.assertRaises(ValueError):
            ready(invalid[2], ['A', 'B'])  # Completion cannot hide a cycle.

    def test_delivered_state_requires_dependency_evidence_reconciliation(self):
        ready = self.concurrency_reference()['ready_story_ids']
        stories = [{'id': 'A', 'priority': 1, 'depends_on': []},
                   {'id': 'B', 'priority': 2, 'depends_on': ['A']}]
        for delivered in (['unknown'], ['B']):
            with self.subTest(delivered=delivered), self.assertRaises(ValueError):
                ready(stories, delivered)

    def test_owned_paths_include_descendants_without_prefix_false_positives(self):
        conflict = self.concurrency_reference()['owned_paths_conflict']
        self.assertTrue(conflict(['src'], ['src/api/handler.py']))
        self.assertTrue(conflict(['src/api'], ['src']))
        self.assertTrue(conflict(['src/api'], ['src/api']))
        self.assertFalse(conflict(['src/api'], ['src/apiv2']))
        self.assertFalse(conflict(['src/a'], ['src/b']))
        self.assertFalse(conflict(['src'], ['src-other']))

    def test_owned_paths_reject_ambiguous_or_escaping_assignments(self):
        conflict = self.concurrency_reference()['owned_paths_conflict']
        for paths in ([], [''], ['.'], ['../src'], ['/src'], ['src/../lib'],
                      ['src//api'], ['src/'], ['src\\api'], ['src/*'], ['src\x00x']):
            with self.subTest(paths=paths), self.assertRaises(ValueError):
                conflict(paths, ['tests'])


if __name__ == '__main__':
    unittest.main()
