"""Static packaging and approval-gate contracts, not live agent behavior tests."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'ai/plugins/coding/skills'


class RecoveryContractTest(unittest.TestCase):
    def test_command_routes_interactive_build_to_packaged_skill(self):
        skill = (SKILLS / 'recover-ralph/SKILL.md').read_text()
        command = (ROOT / 'ai/opencode/commands/recover-ralph.md').read_text()
        self.assertIn('name: recover-ralph', skill)
        self.assertIn('agent: build', command)
        self.assertNotIn('agent: ralph\n', command)
        self.assertIn('`recover-ralph` skill', command)
        self.assertIn('$ARGUMENTS', command)
        for reference in ('ralph-control.md', 'story-execution.md'):
            self.assertTrue((SKILLS / 'prepare-implementation/references' / reference).is_file())
            self.assertIn(reference, skill)
        self.assertIn('relative to the installed skill', skill)
        self.assertIn('explicit confirmation after that preview', skill)
        self.assertIn('Never edit/delete the runner ledger', skill)
        self.assertIn('recheck the branch/HEAD', skill)

    def test_manual_scenarios_cover_mutation_and_restart_gates(self):
        data = json.loads((ROOT / 'tests/fixtures/ralph_recovery_evals.json').read_text())
        scenarios = data['scenarios']
        ids = [row['id'] for row in scenarios]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue({'diagnose-only', 'approved-repair-only',
                         'explicit-clear-and-launch', 'stale-approval',
                         'corrupt-state-or-exhausted-budget', 'live-or-unknown-process',
                         'old-runner', 'sensitive-approval-blocker'} <= set(ids))
        for scenario in scenarios:
            self.assertTrue(scenario['expected'])
            self.assertTrue(scenario['prohibited'])


if __name__ == '__main__':
    unittest.main()
