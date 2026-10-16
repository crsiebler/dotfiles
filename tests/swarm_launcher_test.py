"""Checkout launcher contract; fake Codex only, no model or installed changes."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / 'bin/swarm'


class SwarmLauncherTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(dir=ROOT / 'tests')
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.project = self.root / 'project with spaces'
        self.project.mkdir()
        self.plan = self.project / 'plan $(touch unexpected).md'
        self.plan.write_text('# Approved plan\n')
        self.capture = self.root / 'arguments.json'
        self.tools = self.root / 'tools'
        self.tools.mkdir()
        fake = self.tools / 'codex'
        fake.write_text(
            f'#!{sys.executable}\n'
            'import json, os, pathlib, sys\n'
            'pathlib.Path(os.environ["SWARM_CAPTURE"]).write_text('
            'json.dumps(sys.argv[1:]))\n'
        )
        fake.chmod(0o755)
        self.env = dict(os.environ, PATH=f'{self.tools}:/usr/bin:/bin',
                        SWARM_CAPTURE=str(self.capture))

    def run_launcher(self, *args):
        return subprocess.run([str(LAUNCHER), *args], cwd=self.root,
                              env=self.env, text=True, capture_output=True)

    def test_fresh_sol_session_exact_root_and_literal_scope(self):
        scope = 'Scoped edits; no commits. $(touch unexpected) `false`'
        result = self.run_launcher('--project', str(self.project), '--plan',
                                   self.plan.name, '--scope', scope)
        self.assertEqual(result.returncode, 0, result.stderr)
        argv = json.loads(self.capture.read_text())
        self.assertEqual(argv[:4], ['--model', 'gpt-6.1-sol', '--cd',
                                   str(self.project.resolve())])
        self.assertEqual(len(argv), 5)
        self.assertIn('# Swarm top-level Codex entry instructions', argv[4])
        self.assertIn(str(self.plan), argv[4])
        self.assertIn(scope, argv[4])
        self.assertIn('installed run-agent-team skill', argv[4])
        self.assertIn('sole dispatch, version control', argv[4])
        self.assertFalse((self.root / 'unexpected').exists())
        self.assertEqual(self.plan.read_text(), '# Approved plan\n')

    def test_default_plan_and_dry_run_never_launch_codex(self):
        (self.project / 'PLAN.md').write_text('# Default plan\n')
        result = self.run_launcher('--project', str(self.project), '--dry-run')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Model: gpt-6.1-sol', result.stdout)
        self.assertIn(str(self.project / 'PLAN.md'), result.stdout)
        self.assertIn('No additional authority supplied', result.stdout)
        self.assertFalse(self.capture.exists())

    def test_foreign_or_symlinked_plan_is_rejected(self):
        foreign = self.root / 'other-plan.md'
        foreign.write_text('# Other worktree plan\n')
        link = self.project / 'linked-plan.md'
        link.symlink_to(foreign)
        directory = self.project / 'outside'
        directory.symlink_to(self.root, target_is_directory=True)
        for plan in (str(foreign), '../other-plan.md', str(link),
                     'outside/other-plan.md'):
            with self.subTest(plan=plan):
                result = self.run_launcher('--project', str(self.project),
                                           '--plan', plan)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.capture.exists())

    def test_invalid_input_never_launches(self):
        for args in ([], ['--project'], ['--project', str(self.project)],
                     ['--project', '/nonexistent/swarm-project'],
                     ['--project', str(self.project), '--model', 'other'],
                     ['--project', str(self.project), '--plan', self.plan.name,
                      '--scope', '--dry-run'],
                     ['--dangerously-bypass-approvals-and-sandbox']):
            with self.subTest(args=args):
                result = self.run_launcher(*args)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.capture.exists())


if __name__ == '__main__':
    unittest.main()
