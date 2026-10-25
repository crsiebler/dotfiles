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
REVIEW = ROOT / 'ai/plugins/coding/skills/review-story'
ARCHIVE = ROOT / 'ai/plugins/coding/skills/archive-run'


def examples(text, language='json'):
    return [json.loads(value) for value in re.findall(
        rf'```{language}\n(.*?)\n```', text, re.S)]


def compact(text):
    return ' '.join(text.split())


class StoryExecutionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lives = {'team': (TEAM_REFS / 'story-execution.md').read_text()}
        cls.protocols = {'team': (REVIEW / 'references/contract.md').read_text()}

    def test_review_skill_owns_one_complete_schema(self):
        schemas = {name: examples(text) for name, text in self.protocols.items()}
        self.assertTrue(all(len(values) == 1 for values in schemas.values()))
        schema = schemas['team'][0]
        self.assertEqual(set(schema), {
            'verdict', 'pass_type', 'verification', 'findings', 'resolved_findings',
            'executor_feedback', 'residual_risks', 'learning_candidates'})
        self.assertEqual(set(schema['findings'][0]), {
            'id', 'severity', 'lens', 'title', 'body', 'path', 'line',
            'acceptance_criterion', 'remediation', 'verification', 'confidence'})
        for name, text in self.protocols.items():
            with self.subTest(workflow=name):
                self.assertIn('All listed keys are required', text)
                self.assertIn('must explain missing input in', text)
                self.assertIn('Never return `pass` with unresolved', text)


    def test_generic_reviewer_inherits_runtime_and_uses_supplied_contract(self):
        data = tomllib.loads((ROOT / 'ai/codex/agents/reviewer.toml').read_text())
        self.assertNotIn('sandbox_mode', data)
        self.assertNotIn('model', data)
        text = compact(data['developer_instructions'])
        for obligation in ('inspection-only', 'authorized focused verification',
                           'workflow-supplied review contract', 'Do not edit source',
                           'before and after execution', 'bypass denials'):
            self.assertIn(obligation, text)
        self.assertFalse((ROOT / 'ai/codex/agents/story-reviewer.toml').exists())

    def test_verification_preserves_candidate_and_separates_evidence_provenance(self):
        text = compact(self.protocols['team'])
        for obligation in ('inspection-only', 'execute mode',
                           'mixed staged/unstaged content', 'before checks',
                           'identity and tracked status again afterward',
                           'Candidate drift', 'unexpected tracked writes',
                           'required check cannot run', 'Optional unavailable checks',
                           'Prior supplied results and reviewer-executed results are distinct',
                           'per-command timeouts', 'Count commands and polls'):
            self.assertIn(obligation, text)
        schema = examples(self.protocols['team'])[0]
        self.assertEqual(set(schema['verification'][0]),
                         {'command', 'provenance', 'candidate', 'result', 'evidence'})
        self.assertEqual(schema['verification'][0]['provenance'], 'supplied|executed')

    def test_review_reading_and_verification_budgets_are_separate(self):
        text = compact(self.protocols['team'])
        for obligation in ('40 small, read-only evidence-gathering calls',
                           'Count individual calls in parallel batches separately',
                           '40 calls is a ceiling, not a target',
                           'at most two evidence-gathering tool turns',
                           'one initial pass and at most one targeted remediation pass',
                           'same actual native session',
                           'cannot be used to evade reading budgets'):
            self.assertIn(obligation, text)
        self.assertIn('120-second timeout', self.lives['team'])
        self.assertIn('360-second total', self.lives['team'])

    def test_skill_resources_resolve_after_isolated_copy(self):
        import shutil
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            destination = Path(directory) / 'review-story'
            shutil.copytree(REVIEW, destination)
            for path in destination.rglob('*.md'):
                for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                    if '://' in link or link.startswith('#'):
                        continue
                    target = (path.parent / link.split('#')[0]).resolve()
                    self.assertTrue(target.is_relative_to(destination.resolve()), link)
                    self.assertTrue(target.is_file(), link)


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
                    'Never substitute an unqualified role',
                    'BEGIN REVIEWER ROLE', 'END REVIEWER ROLE',
                    'Never reuse an implementation worker as its own reviewer',
                    'prose is not a substitute for sandbox or permission enforcement',
                ):
                    self.assertIn(safeguard, text)


    def test_generic_native_discovery_preserves_source_and_rejects_duplicates(self):
        helper = ROOT / 'ai/plugins/delegating/skills/use-subagents/scripts/subagents.py'
        source = ROOT / 'ai/codex/agents/reviewer.toml'
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            scratch = Path(directory)
            home, project = scratch / 'home', scratch / 'project'
            agents = home / '.codex/agents'
            agents.mkdir(parents=True)
            project.mkdir()
            (agents / source.name).write_bytes(source.read_bytes())
            env = dict(os.environ, HOME=str(home), CODEX_HOME=str(home / '.codex'))
            argv = [sys.executable, str(helper), '--harness', 'codex',
                    '--project', str(project), 'fetch', 'reviewer']
            result = subprocess.run(argv, env=env, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, source.read_bytes())
            local = project / '.codex/agents'
            local.mkdir(parents=True)
            (local / source.name).write_bytes(source.read_bytes())
            duplicate = subprocess.run(argv, env=env, capture_output=True, text=True)
            self.assertNotEqual(duplicate.returncode, 0)
            self.assertIn('duplicate definitions', duplicate.stderr)

    def test_retired_runtime_has_no_active_entry_points(self):
        for path in ('bin/ralph', 'ai/opencode/agents/ralph.md',
                     'ai/opencode/agents/ralph-reviewer.md',
                     'ai/opencode/commands/recover-ralph.md',
                     'ai/plugins/coding/skills/recover-ralph',
                     'ai/codex/agents/story-reviewer.toml'):
            self.assertFalse((ROOT / path).exists(), path)
        self.assertNotIn('ralph', (ROOT / 'Makefile').read_text().lower())
        self.assertNotIn('ralph', (ROOT / 'scripts/install-ai.py').read_text().lower())

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

    def test_plan_launch_commit_authority_includes_initial_and_continuing_scope(self):
        # Instruction-contract regression, not an executed agent behavior test.
        text = compact(self.lives['team'])
        for obligation in (
            'authorizes the initial and subsequent scoped local commits',
            'Do not ask for another commit approval at launch, between stories or on continuation',
            'initial plan/checkpoint commit',
            'does not mark a story delivered',
            'Explicit planning-only, read-only, source-only or no-commit instructions take precedence',
            'does not authorize push, publication, installation or destructive cleanup',
        ):
            self.assertIn(obligation, text)


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
