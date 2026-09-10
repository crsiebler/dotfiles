"""Static blocker contracts; these do not simulate or prove native Goal behavior."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'ai/plugins/coding/skills/prepare-implementation'
REFS = SKILL / 'references'


def section(path, heading, next_heading):
    text = path.read_text().split(heading, 1)[1].split(next_heading, 1)[0]
    return ' '.join(text.split())


class StoryBlockerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gate = section(
            REFS / 'story-execution.md',
            '## Persistent blockers and Goal resumption',
            '## Bounded memory and durable knowledge',
        )
        cls.review = section(
            REFS / 'story-review.md',
            '### Final blocked verdict versus evidence recovery',
            '## Learning Discipline',
        )

    def assert_contracts(self, text, contracts):
        for contract in contracts:
            with self.subTest(contract=contract):
                self.assertIn(contract, text)

    def test_final_block_preserves_candidate_and_resolution_checkpoint(self):
        self.assert_contracts(self.gate, (
            'stop delivery and further review attempts for that story',
            'Preserve the staged/worktree candidate, incomplete task status',
            'findings and dispositions, check results, reviewer/session provenance',
            'historical evidence',
            'Do not update review memory or mark the story complete',
            'only when the existing write guards allow; otherwise report it',
            'specific blocking condition',
            'What must materially change',
            'evidence required to prove it',
            'initial/targeted passes already consumed',
        ))

    def test_goal_continuation_requires_verified_resolution_not_relabeling(self):
        self.assert_contracts(self.gate, (
            'automatic Goal continuation, elapsed time, a new turn, compaction, '
            'or a new reviewer session does not resolve a blocker or reset the review budget',
            'increasing output limits after repeated truncation',
            'replacing the reviewer does not by itself establish resolution',
            'Do not relabel unchanged work as a new story attempt',
            'only after verifying that the blocking condition has materially changed',
            'exact previously missing staged sections now being accessible through permitted tools',
            'Append the verified change, evidence, and remaining constraints before resuming',
            'Carry forward existing user authorization',
            'genuinely new authority or missing input, identifying the exact constraint',
            'do not repeatedly request the same approval or bypass an actual runtime denial',
        ))

    def test_recovery_and_remediation_are_distinct_from_final_block(self):
        self.assert_contracts(self.review, (
            "current review's permitted evidence-recovery budget; it is not a new pass",
            'A final `blocked` verdict ends this review',
            'specific blocker, what must change, and the evidence required for resolution',
            'in `residual_risks`, using the existing schema',
            'A blocked initial review cannot become a targeted pass',
            'actionable findings and verified remediation from a valid initial review',
        ))
        self.assert_contracts(self.gate, (
            "separate from the reviewer's evidence-reading budget",
            "retaining the failed attempt's history",
            'one initial and at most one targeted same-session remediation pass',
            'remaining targeted pass, not a fresh initial audit',
            'or use material-change language to evade an exhausted remediation budget',
        ))

    def test_other_story_requires_isolated_delivery_or_stops_work(self):
        self.assert_contracts(self.gate, (
            "independently eligible under the plan's dependencies and priority rules",
            'safely isolated from the blocked candidate',
            'Treat the blocked story as ineligible until the gate is met',
            "implementation, staging, checks, and the other story's commit",
            'without discarding or rewriting it',
            'report the blocker and stop work',
            'Do not manufacture additional experiments or bookkeeping to sustain activity',
        ))

    def test_lifecycle_and_ralph_cannot_reset_story_gate(self):
        self.assert_contracts(self.gate, (
            'story-review stop is immediate',
            'native lifecycle capabilities when their runtime conditions are met',
            'blocked-audit restart after user resumption does not reset this story gate',
            'Never invent a restart loop, continuation controller, unsupported Goal setting',
            'runner-validated retryable cycles, and persisted recovery counters',
            'neither authorize Ralph retries nor change their semantics',
            'Ralph does not independently skip to another story',
            'acceptance criteria, required native review/checks',
            'authorized commit gates',
        ))
        docs = ' '.join((ROOT / 'docs/codex-goals.md').read_text().split())
        self.assert_contracts(docs, (
            'at least three consecutive Goal turns, including the original turn',
            'User resumption starts a fresh native blocked audit',
            "Follow the actual runtime's lifecycle instructions",
            'without repeating reviews or inventing activity',
        ))

    def test_skill_handoff_and_manual_evaluations_cover_gate(self):
        skill = ' '.join((SKILL / 'SKILL.md').read_text().split())
        self.assertIn('persistent blocker gate before further story work or review', skill)
        data = json.loads((ROOT / 'tests/fixtures/implementation_planning_evals.json').read_text())
        scenarios = {item['id']: item for item in data['scenarios']}
        required = {
            'goal-unchanged-review-blocker', 'goal-output-recovery-before-verdict',
            'goal-final-truncation-blocker', 'goal-verified-blocker-resolution',
            'goal-blocker-existing-authority', 'goal-isolated-next-story',
            'goal-overlapping-next-story', 'goal-native-blocked-audit',
        }
        self.assertLessEqual(required, scenarios.keys())
        for name in required:
            with self.subTest(scenario=name):
                item = scenarios[name]
                for field in ('context', 'request', 'expected', 'prohibited'):
                    self.assertTrue(item[field])
                self.assertTrue(set(item['expected']).isdisjoint(item['prohibited']))


if __name__ == '__main__':
    unittest.main()
