"""Accessibility skill packaging/contracts, not browser or model evaluations."""
import json
from pathlib import Path
import re
import shutil
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'ai/plugins/coding/skills'
NAMES = {'verify-interface', 'run-tests'}


class AccessibilityGuidanceTest(unittest.TestCase):
    def test_each_bundle_reaches_its_own_accessibility_guidance_after_relocation(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as scratch:
            for name in NAMES:
                destination = Path(scratch) / name
                shutil.copytree(SKILLS / name, destination)
                visited, pending = set(), [destination / 'SKILL.md']
                while pending:
                    source = pending.pop().resolve()
                    if source in visited:
                        continue
                    visited.add(source)
                    for link in re.findall(r'\]\(([^)]+)\)', source.read_text()):
                        if '://' in link or link.startswith('#'):
                            continue
                        target = (source.parent / link.split('#')[0]).resolve()
                        self.assertTrue(target.is_relative_to(destination.resolve()), link)
                        self.assertTrue(target.is_file(), link)
                        if target.suffix == '.md':
                            pending.append(target)
                for reference in ('requirements.md', 'playwright-accessibility.md'):
                    self.assertIn((destination / 'references' / reference).resolve(), visited)

    def test_conditional_dependencies_are_documented_without_new_runtime_config(self):
        # Prevent publishing an adapter workflow whose setup inventory omits it.
        for name in NAMES:
            requirements = (SKILLS / name / 'references/requirements.md').read_text()
            for dependency in ('Playwright', '@axe-core/playwright', 'axe-core'):
                self.assertIn(dependency, requirements)
            inventory = (ROOT / 'docs/skill-dependencies.md').read_text()
            row = next(line for line in inventory.splitlines()
                       if f'/skills/{name}/references/requirements.md' in line)
            self.assertIn('@axe-core/playwright', row)
        for config in (ROOT / 'ai/codex').glob('*.toml'):
            parsed = tomllib.loads(config.read_text())
            self.assertFalse(any('axe' in name or 'accessibility' in name
                                 for name in parsed.get('mcp_servers', {})))

    def test_review_guidance_uses_existing_executable_reviewer_contract(self):
        role = tomllib.loads((ROOT / 'ai/codex/agents/reviewer.toml').read_text())
        self.assertNotEqual('read-only', role.get('sandbox_mode'))
        for name in NAMES:
            reference = (SKILLS / name / 'references/playwright-accessibility.md').read_text()
            self.assertIn('`reviewer`', reference)
            # Safety-critical distinctions shared with the generic review contract.
            self.assertIn('inspection-only', reference)
            self.assertIn('before and after', reference)
            self.assertIn('incomplete', reference)
        self.assertFalse((ROOT / 'ai/codex/agents/accessibility-tester.toml').exists())

    def test_evaluation_scenarios_reference_packaged_skills_and_actual_role(self):
        fixture = json.loads((ROOT / 'tests/fixtures/accessibility_skill_evals.json').read_text())
        self.assertEqual('not-run', fixture['status'])
        ids = set()
        for case in fixture['evals']:
            self.assertNotIn(case['id'], ids)
            ids.add(case['id'])
            self.assertEqual('reviewer', case['role'])
            self.assertTrue((ROOT / 'ai/codex/agents' / (case['role'] + '.toml')).is_file())
            self.assertTrue(set(case['skills']) <= NAMES)
            self.assertTrue(case['prompt'] and case['expected_output'] and case['expectations'])
            self.assertNotIn('actual_output', case)
        self.assertEqual({'prepared', 'inspection', 'missing', 'stale', 'incomplete',
                          'suppression', 'manual', 'side-effects'}, ids)


if __name__ == '__main__':
    unittest.main()
