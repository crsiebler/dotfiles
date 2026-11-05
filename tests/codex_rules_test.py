import json
from pathlib import Path
import shutil
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / 'ai/codex/rules/dotfiles.rules'


class CodexRulesTest(unittest.TestCase):
    @unittest.skipUnless(shutil.which('codex'), 'Codex CLI is unavailable')
    def test_prefix_matching_with_native_policy_checker(self):
        cases = [
            (['git', 'status'], True),
            (['git', 'diff', '--output=/tmp/example'], True),
            (['gh', 'pr', 'view', '123'], True),
            (['gh', 'repo', 'view'], True),
            (['gh', 'pr', 'list'], True),
            (['git', 'add', '.'], False),
            (['git', 'push'], False),
            (['gh', 'pr', 'create'], False),
            (['gh', 'auth', 'status'], False),
            (['sh', '-c', 'git status'], False),
            (['python3', '-c', 'print(1)'], False),
            (['railway', 'status'], False),
        ]
        for command, expected in cases:
            with self.subTest(command=command):
                result = subprocess.run(
                    ['codex', 'execpolicy', 'check', '--rules', str(RULES), '--', *command],
                    capture_output=True, text=True, check=True)
                policy = json.loads(result.stdout)
                self.assertEqual(bool(policy['matchedRules']), expected)
                if expected:
                    self.assertEqual(policy['decision'], 'allow')
