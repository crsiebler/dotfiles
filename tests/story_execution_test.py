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

    def test_expanded_initial_budget_and_output_recovery_are_consistent(self):
        codex = tomllib.loads((ROOT / 'ai/codex/agents/story-reviewer.toml').read_text())
        texts = {
            'native': codex['developer_instructions'],
            'review': (REFS / 'story-review.md').read_text(),
            'execution': (REFS / 'story-execution.md').read_text(),
        }
        for name, text in texts.items():
            with self.subTest(source=name):
                text = ' '.join(text.replace('`', '').split())
                self.assertRegex(text, r'initial review,? (?:use|permit) up to 40 small, read-only evidence-gathering calls')
                self.assertIn('an aggregate patch is not required', text)
                self.assertIn('staged filenames, status, and statistics', text)
                self.assertIn('manageable', text)
                self.assertIn('retrieve only missing sections', text)
                self.assertIn('same oversized request', text)
                self.assertIn('directly affected contracts', text)
                self.assertIn('holistic review', text)
                self.assertIn('40 calls is a ceiling, not a target', text)
                self.assertIn('required evidence remains unavailable', text)
                self.assertIn('exact missing sections', text)
                self.assertIn('residual_risks', text)
                self.assertIn('configurable', text)
                self.assertIn('steps: 3', text)
                self.assertNotIn('Preserve three steps:', text)
                self.assertNotIn('Begin with the staged file list, status, statistics, and aggregate patch', text)

    def test_review_budget_counts_calls_and_preserves_staged_authority(self):
        protocol = ' '.join((REFS / 'story-review.md').read_text().split())
        self.assertIn('Count each call separately', protocol)
        self.assertIn('including inventory reads, searches, recovery reads', protocol)
        self.assertIn('batching does not reset or evade the ceiling', protocol)
        self.assertIn('before patch reads', protocol)
        self.assertIn('internal coverage checklist', protocol)
        self.assertIn('not a file or an added JSON field', protocol)
        self.assertIn('cannot replace missing authoritative staged evidence', protocol)
        self.assertIn('unlisted shell commands, pipelines, or external reads', protocol)
        self.assertIn('Do not spend a targeted pass retrying a blocked initial review', protocol)
        self.assertIn('without speculative findings', protocol)

    def test_targeted_budget_session_and_review_boundaries_are_preserved(self):
        protocol = ' '.join((REFS / 'story-review.md').read_text().split())
        self.assertIn('Targeted review retains at most two evidence-gathering tool turns', protocol)
        self.assertIn('one initial pass and at most one targeted remediation pass in the same actual native session', protocol)
        self.assertIn('Keep each staged candidate immutable', protocol)
        self.assertIn('Do not broaden a targeted pass into a fresh audit', protocol)
        self.assertIn('No MCP, external-directory, credential-store, or network access', protocol)
        self.assertIn('Do not edit files, run checks, browse, fetch documentation, delegate work, stage changes, commit', protocol)
        self.assertIn('`critical`, `high`, and `medium` findings block completion', protocol)
        self.assertIn('must explain missing input in `residual_risks`', protocol)

    def test_explicit_profile_routing_matches_native_wrappers(self):
        execution = (REFS / 'story-execution.md').read_text()
        rows = re.findall(
            r'^\| (RalphJSON|CodexGoalMarkdown) \| `([^`]+)` \| `([^`]+)` \|$',
            execution, re.M,
        )
        self.assertEqual(rows, [
            ('RalphJSON', 'ralph-reviewer', 'three-step'),
            ('CodexGoalMarkdown', 'story-reviewer', 'expanded-initial'),
        ])
        codex = tomllib.loads(
            (ROOT / 'ai/codex/agents/story-reviewer.toml').read_text()
        )['developer_instructions']
        ralph = (ROOT / 'ai/opencode/agents/ralph-reviewer.md').read_text()
        for wrapper, profile in ((codex, 'expanded-initial'),
                                 (ralph, 'three-step')):
            with self.subTest(profile=profile):
                text = ' '.join(wrapper.split())
                self.assertIn(f'This role uses the {profile} review profile.', text)
                self.assertIn(f'Require Review profile: {profile}', text)
                self.assertIn('on both initial and targeted invocations', text)
                self.assertIn('missing, unknown, or conflicting profile', text)
                self.assertIn('residual_risks', text)
                self.assertIn('Do not infer the harness', text)
        self.assertNotIn('You are the Codex Goal', codex)
        self.assertIn('staged-story reviewer for the Markdown Goal adapter', codex)

    def test_profiles_are_input_only_and_fail_closed_before_evidence(self):
        protocol = ' '.join((REFS / 'story-review.md').read_text().split())
        for contract in (
            'Review profile: expanded-initial',
            'Pass type: initial',
            'Before gathering evidence',
            'missing, unknown, or conflicting profile',
            'return `blocked`',
            'explain the exact profile problem in `residual_risks`',
            'Do not infer the harness',
            'tools, binaries, paths, or role names',
            'A profile never grants tools or overrides tighter runtime limits',
            'input metadata only; do not add it to the response JSON',
        ):
            with self.subTest(contract=contract):
                self.assertIn(contract, protocol)
        execution = ' '.join((REFS / 'story-execution.md').read_text().split())
        self.assertIn('already-selected task-source adapter', execution)
        self.assertIn('Include `Review profile: <profile>` and `Pass type: initial`',
                      execution)
        self.assertIn('same `Review profile: <profile>` and `Pass type: targeted`',
                      execution)
        self.assertIn('For self-review, explicitly select the same adapter profile',
                      execution)
        self.assertNotIn('For a Codex initial review', execution + protocol)

    def test_each_profile_keeps_its_own_initial_and_targeted_budget(self):
        protocol = (REFS / 'story-review.md').read_text()
        budgets = protocol.split('## Review Profile Budgets\n', 1)[1].split(
            '## Shared Output-Aware Evidence Procedure\n', 1
        )[0]
        sections = re.findall(r'^### ([^\n]+)\n(.*?)(?=^### |\Z)',
                              budgets, re.M | re.S)
        self.assertEqual([name for name, _ in sections], [
            'expanded-initial', 'three-step', 'Targeted passes under either profile',
        ])
        expanded, three_step, targeted = (
            ' '.join(text.split()) for _, text in sections
        )
        self.assertIn('For an initial review, permit up to 40', expanded)
        self.assertIn('Count each call separately', expanded)
        self.assertIn('at most one evidence-recovery tool turn', three_step)
        self.assertIn('separately enforced `steps: 3`', three_step)
        self.assertIn('exact Git allowlist', three_step)
        self.assertNotIn('permit up to 40', three_step)
        self.assertIn('at most two evidence-gathering tool turns', targeted)
        self.assertIn('Keep the same profile on resumption', targeted)
        self.assertIn('does not give targeted review a new 40-call', targeted)

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
