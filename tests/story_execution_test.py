"""Static shared workflow contracts, not model-execution or enforcement tests."""

import json
from pathlib import Path
import re
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'ai/plugins/coding/skills/prepare-implementation'
REFS = SKILL / 'references'


class StoryExecutionTest(unittest.TestCase):
    def test_review_schema_is_shared_and_preserves_response_contract(self):
        protocol = (REFS / 'story-review.md').read_text()
        examples = re.findall(r'```json\n(.*?)\n```', protocol, re.S)
        self.assertEqual(len(examples), 1)
        schema = json.loads(examples[0])
        self.assertEqual(set(schema), {
            'verdict', 'pass_type', 'findings', 'resolved_findings',
            'executor_feedback', 'residual_risks', 'learning_candidates',
        })
        self.assertEqual(set(schema['findings'][0]), {
            'id', 'severity', 'lens', 'title', 'body', 'path', 'line',
            'acceptance_criterion', 'remediation', 'verification', 'confidence',
        })
        codex = tomllib.loads((ROOT / 'ai/codex/agents/story-reviewer.toml').read_text())
        self.assertEqual(codex['sandbox_mode'], 'read-only')
        for wrapper in (codex['developer_instructions'],
                        (ROOT / 'ai/opencode/agents/ralph-reviewer.md').read_text()):
            self.assertIn('references/story-review.md', wrapper)
            self.assertNotIn('"verdict":', wrapper)
            self.assertIn('supplied', wrapper)

    def test_both_adapters_require_installed_shared_contract(self):
        markdown = (REFS / 'markdown-checklist.md').read_text()
        template = markdown.split('```markdown\n', 1)[1].split('\n```', 1)[0]
        ralph = (ROOT / 'ai/opencode/agents/ralph.md').read_text()
        for adapter in (template, ralph):
            for name in ('story-execution.md', 'story-review.md',
                         'docs/progress.md', 'memory.json'):
                self.assertIn(name, adapter)
            self.assertIn('installed', adapter)
            self.assertNotIn('ai/plugins/', adapter)
        self.assertIn('story-reviewer', template)
        self.assertIn('`ralph-reviewer`', ralph)
        self.assertNotIn('#### Evidence', template)

    def test_ralph_recovery_is_explicit_and_not_a_goal_controller(self):
        ralph = (ROOT / 'ai/opencode/agents/ralph.md').read_text()
        execution = (REFS / 'story-execution.md').read_text()
        control = (REFS / 'ralph-control.md').read_text()
        self.assertIn('references/ralph-control.md', ralph)
        self.assertIn('An explicit request to run Ralph authorizes scoped implementation', ralph)
        self.assertIn('one commit per passing story', ralph)
        self.assertIn('does not arise from loading this role', ralph)
        self.assertIn('narrower user instructions', ralph)
        self.assertIn('runner validates a retryable', execution)
        self.assertIn('No automatic recovery loop is added to native Codex Goal', execution)
        self.assertNotIn('--authorize-story-commits', execution + ralph)
        examples = re.findall(r'```json\n(.*?)\n```', control, re.S)
        self.assertEqual(len(examples), 3)
        for example, status in zip(examples, ('completed', 'retryable', 'blocked')):
            outcome = json.loads(example)
            self.assertEqual(outcome['version'], 1)
            self.assertEqual(outcome['status'], status)
            self.assertTrue(outcome['iteration_id'])
            self.assertTrue(outcome['story_id'])
            if status == 'retryable':
                self.assertTrue(all(outcome[key] for key in
                                    ('finding_ids', 'attempted_action', 'next_action', 'evidence')))
            if status == 'blocked':
                self.assertTrue(outcome['reason'])

    def test_memory_entry_example_has_canonical_keys_and_consistent_counts(self):
        execution = (REFS / 'story-execution.md').read_text()
        examples = re.findall(r'```json\n(.*?)\n```', execution, re.S)
        self.assertEqual(len(examples), 1)
        memory = json.loads(examples[0])
        self.assertEqual(set(memory), {'version', 'patterns', 'suppressions'})
        self.assertEqual(memory['version'], 1)
        pattern = memory['patterns'][0]
        self.assertEqual(set(pattern), {
            'id', 'lens', 'scope', 'guidance', 'evidence_count', 'accepted_count',
            'rejected_count', 'last_validated_story', 'status',
        })
        self.assertEqual(pattern['evidence_count'],
                         pattern['accepted_count'] + pattern['rejected_count'])
        self.assertGreaterEqual(pattern['accepted_count'], 1)
        self.assertEqual(set(memory['suppressions'][0]), {
            'fingerprint', 'reason', 'scope', 'last_reviewed_story',
        })
        self.assertIn('Count an event only once', execution)
        self.assertIn('approved conversion', execution)

    def test_planning_fixtures_cover_failure_and_resumption_contracts(self):
        data = json.loads((ROOT / 'tests/fixtures/implementation_planning_evals.json').read_text())
        scenarios = data['scenarios']
        ids = [item['id'] for item in scenarios]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue({
            'goal-missing-reviewer', 'goal-invalid-memory', 'goal-branch-mismatch',
            'goal-failed-commit', 'goal-malformed-review', 'goal-same-session-memory',
        } <= set(ids))
        for item in scenarios:
            self.assertTrue(item['expected'])
            self.assertTrue(item['prohibited'])
        execution = (REFS / 'story-execution.md').read_text()
        self.assertIn('| RalphJSON |', execution)
        self.assertIn('| CodexGoalMarkdown |', execution)
        self.assertIn('read both in full', execution)
        self.assertIn('at most 20 patterns and 20 suppressions', execution)
        self.assertIn('same\nnative session', execution)
        self.assertIn('successful\nauthorized story commit', execution)


if __name__ == '__main__':
    unittest.main()
