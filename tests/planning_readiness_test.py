"""Static planning/launch instruction contracts, not live-agent evaluations."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PLANNING = 'ai/plugins/coding/skills/prepare-implementation/'


def text(path):
    return ' '.join((ROOT / path).read_text().split())


class PlanningReadinessTest(unittest.TestCase):
    def test_readiness_is_required_and_has_blocking_dispositions(self):
        entry = text(PLANNING + 'SKILL.md')
        self.assertIn('[execution readiness](references/execution-readiness.md) for every plan', entry)
        contract = text(PLANNING + 'references/execution-readiness.md')
        for disposition in ('Resolved: authorized', 'Resolved: completed',
                            'Resolved: changed approach', 'Blocked'):
            self.assertIn(disposition, contract)
        for guard in ('all applicable human gates and manual prerequisites are resolved',
                      'Unknown required capability is a blocker',
                      'acceptance coverage has no unresolved gaps',
                      'A promise to do it later is not completion'):
            self.assertIn(guard, contract)

    def test_audit_covers_closeout_and_does_not_self_authorize(self):
        contract = text(PLANNING + 'references/execution-readiness.md')
        for boundary in ('verification/review, integration, and closeout',
                         'Carry forward existing grants without asking again',
                         'do not invent a separate commit gate',
                         'silence or elapsed time is not approval',
                         'Do not perform setup as a planning side effect',
                         'planning and plan approval alone never begin implementation',
                         'never collect credentials in the plan'):
            self.assertIn(boundary, contract)

    def test_future_result_and_runtime_gates_cannot_be_preapproved_away(self):
        contract = text(PLANNING + 'references/execution-readiness.md')
        for guard in ('blanket advance approval cannot satisfy that requirement',
                      'mandatory per-call runtime prompt blocks unattended readiness',
                      'Never relax runtime restrictions, disable safeguards',
                      'Do not replace explicitly required human acceptance with an automated check unless the user approves'):
            self.assertIn(guard, contract)

    def test_verification_is_automatable_without_inventing_release_gates(self):
        entry = text(PLANNING + 'SKILL.md')
        for rule in ('Include only agent-executable, noninteractive verification',
                     'Do not add manual QA, human test-result confirmation',
                     'Deployment or deployment verification belongs only when explicitly in scope and automatable',
                     'command or tool-driven procedure, inputs/fixtures, expected result and story',
                     'New tests or automation may be implemented as scoped work',
                     'Optional manual follow-up is outside this goal and cannot block its completion'):
            self.assertIn(rule, entry)
        contract = text(PLANNING + 'references/execution-readiness.md')
        self.assertIn('an implementation dependency, not a manual prerequisite', contract)
        self.assertIn('Never include unresolved manual verification as an executable story', contract)
        template = text(PLANNING + 'references/markdown-checklist.md')
        self.assertIn('automated check: command/tool procedure, inputs and expected result', template)
        self.assertIn('Explicit non-automatable requirements remain planning conflicts', template)

    def test_template_and_opencode_entry_carry_readiness(self):
        template = text(PLANNING + 'references/markdown-checklist.md')
        for field in ('## Execution readiness', 'Requested endpoint:',
                      'Audited revision / runtime / environment:',
                      'Unattended readiness: blocked | ready',
                      'Authority / resolution evidence', 'Remaining blockers:',
                      'Recheck at launch:'):
            self.assertIn(field, template)
        command = text('ai/opencode/commands/plan-work.md')
        self.assertIn('Resolve them upfront', command)
        self.assertIn('keeps the plan a blocked draft', command)

    def test_requirements_define_automated_acceptance_without_claiming_execution(self):
        bundle = 'ai/plugins/coding/skills/write-requirements/'
        entry = text(bundle + 'SKILL.md')
        for rule in ('agent-executable, noninteractive verification',
                     'Do not add manual QA, human confirmation of test results',
                     'New test automation may be scoped implementation work',
                     'preserve the source requirement and surface the conflict',
                     'Optional human follow-up stays outside implementation completion',
                     'requirements drafting neither runs checks nor requires tests to exist already'):
            self.assertIn(rule, entry)
        template = text(bundle + 'references/prd-format.md')
        self.assertIn('autonomous acceptance scope', template)
        self.assertIn('Automated tests verify the specified behavior and edge cases', template)
        self.assertIn('Agent-executable browser checks', template)
        self.assertNotIn('Generate and run migration successfully', template)
        self.assertNotIn('Verify in browser using verify-interface skill', template)
        self.assertIn('Drafting does not run tests or launch implementation',
                      text('ai/opencode/commands/define-requirements.md'))

    def test_team_supports_unattended_execution_with_scoped_automated_checks(self):
        bundle = 'ai/plugins/coding/skills/run-agent-team/'
        entry = text(bundle + 'SKILL.md')
        self.assertNotIn('or unattended runner execution', entry)
        self.assertIn('Unattended work in the current session is supported', entry)
        self.assertIn('not additional per-plan delivery gates', entry)
        delivery = text(bundle + 'references/story-execution.md')
        for guard in ('Known missing authority for required archival or other closeout blocks launch',
                      'Deployment verification belongs only when explicitly in the approved scope and automatable',
                      'Do not infer deployment authority from a deployment-related code change',
                      'Optional manual follow-up is outside goal completion and cannot block delivery',
                      'No required check is waived merely because it fails or is unavailable'):
            self.assertIn(guard, delivery)

    def test_worker_packets_preserve_automation_contract(self):
        bundle = 'ai/plugins/coding/skills/run-agent-team/references/'
        packet = text(bundle + 'team-execution.md')
        self.assertIn('test inputs/fixtures, expected results, check ownership and budgets', packet)
        self.assertIn('prerequisite test/automation authoring', packet)
        self.assertIn('no manual QA, human result-confirmation or added release gate', packet)
        for name in ('team-execution.md', 'requirements.md', 'codex.md'):
            with self.subTest(reference=name):
                self.assertIn('(story-execution.md#autonomous-execution-scope)', text(bundle + name))

    def test_browser_reviewer_authority_matches_the_supplied_contract(self):
        delivery = text('ai/plugins/coding/skills/run-agent-team/references/story-execution.md')
        self.assertNotIn('reviewers only assess supplied evidence', delivery)
        self.assertIn('packet-authorized focused browser flows in execute mode', delivery)
        self.assertIn('Inspection-only reviewers do not operate browsers', delivery)
        self.assertIn('candidate-preservation rules and budgets', delivery)

    def test_both_execution_paths_check_readiness_and_legacy_plans(self):
        for name in ('develop-code', 'run-agent-team'):
            with self.subTest(skill=name):
                entry = text(f'ai/plugins/coding/skills/{name}/SKILL.md')
                self.assertIn('execution-readiness record', entry)
                self.assertIn('before implementation edits', entry.lower())
                self.assertIn('a blocked record is not an executable handoff', entry)
                self.assertIn('legacy plan without a record', entry)
                self.assertIn('without regenerating the plan', entry)
                self.assertIn('New mandatory gates stop affected work', entry)
        self.assertIn('Direct coding requests without a plan do not require creating a plan',
                      text('ai/plugins/coding/skills/develop-code/SKILL.md'))

    def test_authored_scenarios_cover_success_and_blocked_handoffs(self):
        data = json.loads((ROOT / 'tests/fixtures/implementation_planning_evals.json').read_text())
        self.assertIn('not recorded model results', data['purpose'])
        cases = data['scenarios']
        self.assertEqual(len(cases), len({case['id'] for case in cases}))
        readiness = {case['id']: case for case in cases if case['id'].startswith('readiness-')}
        required = {'existing-grants', 'missing-scoped-authority', 'manual-promise',
                    'manual-completed', 'future-payload', 'approved-endpoint-change',
                    'runtime-prompt', 'unknown-capability', 'changed-context',
                    'legacy-plan', 'planning-only', 'closeout-gate', 'untrusted-grant',
                    'automated-verification-only', 'new-test-automation',
                    'explicit-manual-acceptance', 'automated-deployment',
                    'optional-manual-followup'}
        self.assertTrue({f'readiness-{name}' for name in required}.issubset(readiness))
        for case in readiness.values():
            self.assertTrue(case['context'] and case['request'])
            self.assertTrue(case['expected'] and case['prohibited'])


if __name__ == '__main__':
    unittest.main()
