"""Current role and skill packaging invariants, not model behavior tests."""
import json
from pathlib import Path
import re
import shutil
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGINS = ROOT / 'ai/plugins'
AGENTS = ROOT / 'ai/codex/agents'
LOOKUP = PLUGINS / 'delegating/skills/use-subagents/references'
CORE = {'researcher', 'planner', 'reviewer', 'auditor', 'operator'}


class CoreRolesTest(unittest.TestCase):
    def test_exact_roles_and_no_permission_escalation(self):
        self.assertEqual(CORE, {p.stem for p in AGENTS.glob('*.toml')})
        for name in CORE:
            data = tomllib.loads((AGENTS / f'{name}.toml').read_text())
            self.assertEqual(name, data['name'])
            self.assertFalse({'model', 'model_provider', 'model_reasoning_effort',
                              'approval_policy'} & data.keys())
            self.assertEqual('read-only' if name == 'auditor' else None,
                             data.get('sandbox_mode'))

    def test_role_selection_documents_exact_current_contracts(self):
        text = (LOOKUP / 'core-roles.md').read_text()
        rows = set(re.findall(r'^\| ([a-z]+) \|', text, re.M))
        self.assertEqual(CORE, rows)

    def test_current_bundle_resources_survive_relocation(self):
        bundles = sorted(PLUGINS.glob('*/skills/*/SKILL.md'))
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as scratch:
            for entry in bundles:
                destination = Path(scratch) / entry.parents[2].name / entry.parent.name
                shutil.copytree(entry.parent, destination)
                visited, pending = set(), [destination / 'SKILL.md']
                while pending:
                    source = pending.pop().resolve()
                    if source in visited:
                        continue
                    visited.add(source)
                    # Fenced templates/examples are not bundle resource links.
                    prose = re.sub(r'^```.*?^```[^\n]*$', '', source.read_text(),
                                   flags=re.M | re.S)
                    for link in re.findall(r'\]\(([^)]+)\)', prose):
                        if '://' in link or link.startswith('#'):
                            continue
                        target = (source.parent / link.split('#')[0]).resolve()
                        self.assertTrue(target.is_relative_to(destination.resolve()), link)
                        self.assertTrue(target.is_file(), link)
                        if target.suffix == '.md':
                            pending.append(target)
                self.assertIn((destination / 'references/requirements.md').resolve(), visited)

    def test_pr_review_dispatch_uses_one_reviewer_and_optional_auditor(self):
        text = (ROOT / 'ai/opencode/commands/review-pr.md').read_text()
        rows = re.findall(r'^\| `([a-z]+)` \| ([^|]+) \|', text, re.M)
        self.assertEqual(['reviewer', 'auditor'], [role for role, _ in rows])
        self.assertIn('Default', rows[0][1])
        self.assertIn('Optional', rows[1][1])
        sources = re.search(r'"source": "([^"]+)"', text).group(1).split('|')
        self.assertEqual({'reviewer', 'auditor', 'summary'}, set(sources))
        self.assertIn('verify-interface', text)
        self.assertIn('inspection-only', text)
        self.assertNotIn('skipped or\n  simulated', text)

    def test_active_dispatch_hints_name_real_roles(self):
        candidates = list((ROOT / 'ai/opencode/commands').glob('*.md'))
        candidates.append(PLUGINS / 'coding/skills/write-requirements/references/prd-format.md')
        for source in candidates:
            text = source.read_text()
            for name in re.findall(r'(?<!\w)@([a-z][a-z0-9-]*)', text):
                self.assertIn(name, CORE | {'sprite-artist'}, str(source))
            for name in re.findall(r'^agent: (\S+)$', text, re.M):
                self.assertIn(name, CORE | {'sprite-artist'}, str(source))

    def test_skills_and_dependencies_are_unique_and_indexed(self):
        skills = list(PLUGINS.glob('*/skills/*/SKILL.md'))
        self.assertEqual(47, len(skills))
        names = []
        inventory = (ROOT / 'docs/skill-dependencies.md').read_text()
        for source in skills:
            names.extend(re.findall(r'^name: (.+)$', source.read_text(), re.M))
            self.assertTrue((source.parent / 'references/requirements.md').is_file())
            self.assertIn('/' + source.parent.name + '/references/requirements.md', inventory)
        self.assertEqual(len(names), len(set(names)))

    def test_core_scenarios_reference_available_roles_and_skills(self):
        fixture = json.loads((ROOT / 'tests/fixtures/core_role_evals.json').read_text())
        self.assertEqual('not-run', fixture['status'])
        self.assertEqual(CORE, {case['role'] for case in fixture['evals'] if 'role' in case})
        names = {p.parent.name for p in PLUGINS.glob('*/skills/*/SKILL.md')}
        for case in fixture['evals']:
            if 'native_agents' in case:
                self.assertNotIn('role', case)
                self.assertEqual({'codex': 'worker', 'opencode': 'general'}, case['native_agents'])
            self.assertIn(case['skill'], names)
            self.assertTrue(case['prompt'] and case['expected_output'])


if __name__ == '__main__':
    unittest.main()
