"""Offline bundle/graph/Git contracts; no native agents, models or activation."""

import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / 'ai/plugins/coding/skills/run-agent-team'
ARCHIVE = ROOT / 'ai/plugins/coding/skills/archive-run'
CONCURRENCY = ROOT / 'ai/plugins/coding/skills/run-agent-team/references/task-concurrency.md'


def reference_functions():
    code = CONCURRENCY.read_text().split('```python\n', 1)[1].split('\n```', 1)[0]
    namespace = {}
    exec(compile(code, str(CONCURRENCY), 'exec'), namespace)
    return namespace


class AgentTeamContractTest(unittest.TestCase):
    def test_bundle_resources_are_local_and_evaluations_are_well_formed(self):
        entry = (BUNDLE / 'SKILL.md').read_text()
        header = entry.split('---', 2)[1]
        self.assertEqual(re.findall(r'^name: (.+)$', header, re.M), ['run-agent-team'])
        for source in BUNDLE.rglob('*.md'):
            for link in re.findall(r'\]\(([^)]+)\)', source.read_text()):
                if '://' in link or link.startswith('#'):
                    continue
                target = (source.parent / link.split('#')[0]).resolve()
                self.assertTrue(target.is_relative_to(BUNDLE.resolve()), link)
                self.assertTrue(target.is_file(), link)
        evaluations = json.loads((ROOT / 'tests/fixtures/workflow_skill_evals/run-agent-team/evals.json').read_text())
        self.assertEqual(evaluations['skill_name'], 'run-agent-team')
        ids = [case['id'] for case in evaluations['evals']]
        self.assertEqual(len(ids), len(set(ids)))
        for case in evaluations['evals']:
            self.assertTrue(case['prompt'] and case['expected_output'] and case['expectations'])

    def test_planning_is_atomic_and_execution_resources_have_one_owner(self):
        planning = ROOT / 'ai/plugins/coding/skills/prepare-implementation'
        develop = ROOT / 'ai/plugins/coding/skills/develop-code/SKILL.md'
        self.assertNotIn('run-agent-team', develop.read_text())
        for source in planning.rglob('*.md'):
            self.assertNotIn('run-agent-team', source.read_text(), str(source))
            for link in re.findall(r'\]\(([^)]+)\)', source.read_text()):
                if '://' not in link and not link.startswith('#'):
                    target = (source.parent / link.split('#')[0]).resolve()
                    self.assertTrue(target.is_relative_to(planning.resolve()))
                    self.assertTrue(target.is_file(), link)
        for name in ('story-execution.md', 'story-review.md'):
            self.assertTrue((BUNDLE / 'references' / name).is_file())
            self.assertFalse((planning / 'references' / name).exists())
        self.assertFalse((planning / 'scripts/archive_run.py').exists())
        self.assertTrue((ARCHIVE / 'scripts/archive_run.py').is_file())
        self.assertFalse((BUNDLE / 'scripts/archive_run.py').exists())
        for consumer in ('ai/opencode/agents/ralph.md',
                         'ai/opencode/agents/ralph-reviewer.md',
                         'ai/plugins/coding/skills/recover-ralph/SKILL.md'):
            text = (ROOT / consumer).read_text()
            self.assertNotIn('story-delivery', text)
            self.assertNotIn('run-agent-team', text)
            self.assertNotIn('prepare-implementation', text)
        reviewer = (ROOT / 'ai/codex/agents/story-reviewer.toml').read_text()
        self.assertIn('run-agent-team', reviewer)
        entry = ' '.join((BUNDLE / 'SKILL.md').read_text().split())
        self.assertIn('main thread is the sole integration owner', entry)
        self.assertIn('main thread is the sole integration owner and the only dispatcher', entry)
        self.assertIn('multi-agent-coordinator', entry)
        self.assertIn('No custom coordinator selection, nested delegation', entry)
        self.assertIn('do not invoke a planner', entry)

    def test_archival_capability_has_closed_resources_and_no_delivery_framework(self):
        for source in ARCHIVE.rglob('*.md'):
            text = source.read_text()
            for forbidden in ('story-delivery', 'multi-agent-coordinator',
                              'task-concurrency.md', 'gpt-6-luna', 'Kahn'):
                self.assertNotIn(forbidden, text, str(source))
            for link in re.findall(r'\]\(([^)]+)\)', text):
                if '://' not in link and not link.startswith('#'):
                    target = (source.parent / link.split('#')[0]).resolve()
                    self.assertTrue(target.is_relative_to(ARCHIVE.resolve()))
                    self.assertTrue(target.is_file(), link)
        self.assertFalse((ARCHIVE / 'references/story-execution.md').exists())
        self.assertFalse((ARCHIVE / 'references/story-review.md').exists())
        self.assertFalse((ROOT / 'ai/plugins/coding/skills/story-delivery').exists())
        entry = (BUNDLE / 'SKILL.md').read_text()
        self.assertIn('archive-run', entry)
        self.assertIn('Never invoke Ralph', entry)

    def test_main_session_dispatches_without_custom_coordinator_or_primary(self):
        role = ROOT / 'ai/codex/agents/multi-agent-coordinator.toml'
        self.assertTrue(role.is_file())
        self.assertFalse((role.parent / 'multi-agent-orchestration.toml').exists())
        text = ' '.join(role.read_text().split())
        self.assertIn('optional role is not an orchestration prerequisite', text)
        self.assertIn('run-agent-team', text)
        self.assertIn('never dispatch workers/reviewers, stage, commit, merge', text)
        packet = ' '.join((BUNDLE / 'references/team-execution.md').read_text().split())
        for guard in ('main AI session directly owns dispatch, Git, integration',
                      'quiesce', 'proxy-spawning', 'required reviewer',
                      'same-session continuation', 'consumed budgets',
                      'Worker results do not release dependencies'):
            self.assertIn(guard.lower(), packet.lower())
        self.assertIn('No coordinator role, primary-agent switch, nesting', packet)
        self.assertIn('Its definition need not be loaded', packet)
        for path in ('bin/swarm', 'ai/codex/swarm.md', 'docs/swarm.md',
                     'tests/swarm_launcher_test.py'):
            self.assertFalse((ROOT / path).exists(), path)
        for path in ('AGENTS.md', 'README.md', 'docs/agent-team-verification.md'):
            self.assertNotIn('bin/swarm', (ROOT / path).read_text())

    def test_goal_entry_explicitly_selects_skill_and_keeps_host_prerequisites(self):
        packet = ' '.join((BUNDLE / 'references/codex.md').read_text().split())
        for text in ('/skills', '$run-agent-team', '/goal <objective>',
                     'it does not by itself select this skill',
                     'Do not assume combined slash-command/skill parsing',
                     'This example is not an execution grant'):
            self.assertIn(text, packet)
        entry = (BUNDLE / 'SKILL.md').read_text()
        self.assertIn('[Codex CLI entry](references/codex.md) only for a Codex CLI', entry)
        requirements = ' '.join((BUNDLE / 'references/requirements.md').read_text().split())
        for capability in ('spawn/follow-up/wait/session inspection',
                           'known capacity', 'same-session continuation',
                           'approved clean committed integration/task branches'):
            self.assertIn(capability, requirements)
        self.assertIn('selection is optional unless needed to satisfy a user requirement',
                      requirements)

    def test_core_workflow_is_harness_agnostic_and_capability_gated(self):
        for name in ('team-execution.md', 'task-concurrency.md', 'requirements.md',
                     'runtime-selection.md', 'story-execution.md', 'story-review.md',
                     'verification.md'):
            text = (BUNDLE / 'references' / name).read_text()
            with self.subTest(reference=name):
                for token in ('Codex', 'OpenCode', '/goal', '/skills'):
                    self.assertNotIn(token, text)
        entry = (BUNDLE / 'SKILL.md').read_text()
        self.assertIn('AI harness agnostic', entry)
        self.assertIn('[team execution contract](references/team-execution.md)', entry)
        self.assertNotIn('Codex-only', entry)
        self.assertFalse((BUNDLE / 'references/codex-concurrency.md').exists())
        contract = ' '.join((BUNDLE / 'references/team-execution.md').read_text().split())
        for guard in ('inspect the tools actually exposed',
                      'inspect actual entry/tool schemas',
                      'exact story-reviewer invocation and same-session continuation',
                      'No custom coordinator selection or nested manager is needed'):
            self.assertIn(guard.lower(), contract.lower())

    def test_ready_frontier_requires_integration_delivery_not_worker_results(self):
        ready = reference_functions()['ready_story_ids']
        stories = [
            dict(id='A', priority=2, depends_on=[], worker_finished=True),
            dict(id='B', priority=1, depends_on=[], worker_finished=True),
            dict(id='C', priority=3, depends_on=['A', 'B']),
        ]
        self.assertEqual(ready(stories, []), ['B', 'A'])
        self.assertEqual(ready(stories, ['A']), ['B'])
        self.assertEqual(ready(stories, ['A', 'B']), ['C'])
        self.assertEqual(ready(stories, ['A', 'B', 'C']), [])

    def test_invalid_graphs_and_directory_ownership_conflicts(self):
        functions = reference_functions()
        for graph in (
            [dict(id='A', priority=1, depends_on=['missing'])],
            [dict(id='A', priority=1, depends_on=['A'])],
            [dict(id='A', priority=1, depends_on=['B']),
             dict(id='B', priority=2, depends_on=['A'])],
        ):
            with self.subTest(graph=graph), self.assertRaises((ValueError, RuntimeError)):
                functions['ready_story_ids'](graph, [])
        conflict = functions['owned_paths_conflict']
        self.assertTrue(conflict(['src'], ['src/shared.py']))
        self.assertFalse(conflict(['src/a.py'], ['src/b.py']))
        with self.assertRaises(ValueError):
            conflict(['../escape'], ['src/b.py'])

    def test_disposable_two_worktree_git_roots_and_stale_dependency_base(self):
        # This checks Git conditions, not model dispatch, review, or containment.
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            root = Path(directory).resolve()
            repo = root / 'repo'
            repo.mkdir()
            env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
            env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')

            def git(path, *args, check=True):
                return subprocess.run(['git', '-C', str(path), *args], env=env,
                                      check=check, capture_output=True, text=True)

            git(repo, 'init', '-q', '-b', 'fixture/integration')
            git(repo, 'config', 'user.name', 'Team Fixture')
            git(repo, 'config', 'user.email', 'fixture@example.invalid')
            git(repo, 'config', 'commit.gpgsign', 'false')
            (repo / 'a.txt').write_text('baseline A\n')
            (repo / 'b.txt').write_text('baseline B\n')
            git(repo, 'add', 'a.txt', 'b.txt')
            git(repo, 'commit', '-qm', 'fixture baseline')
            base = git(repo, 'rev-parse', 'HEAD').stdout.strip()
            a, b = root / 'worker-a', root / 'worker-b'
            for path, branch in ((a, 'fixture/a'), (b, 'fixture/b')):
                git(repo, 'worktree', 'add', '-q', '-b', branch, str(path), base)
                self.assertEqual(git(path, 'rev-parse', '--show-toplevel').stdout.strip(), str(path))
                self.assertEqual(git(path, 'status', '--porcelain').stdout, '')
            (a / 'a.txt').write_text('candidate A\n')
            (b / 'b.txt').write_text('candidate B\n')
            self.assertEqual(git(a, 'diff', '--name-only').stdout.strip(), 'a.txt')
            self.assertEqual(git(b, 'diff', '--name-only').stdout.strip(), 'b.txt')
            self.assertEqual(git(repo, 'status', '--porcelain').stdout, '')
            git(a, 'add', 'a.txt')
            git(a, 'commit', '-qm', 'fixture worker revision')
            candidate = git(a, 'rev-parse', 'HEAD').stdout.strip()
            git(repo, 'cherry-pick', candidate)
            integrated = git(repo, 'rev-parse', 'HEAD').stdout.strip()
            self.assertNotEqual(git(b, 'merge-base', '--is-ancestor', integrated, 'HEAD', check=False).returncode, 0)
            self.assertEqual((b / 'b.txt').read_text(), 'candidate B\n')
            self.assertEqual((repo / 'b.txt').read_text(), 'baseline B\n')


if __name__ == '__main__':
    unittest.main()
