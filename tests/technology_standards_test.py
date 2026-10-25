"""Current standards and portable resources; no model-behavior claims."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / 'ai/codex/agents'
SKILLS = ROOT / 'ai/plugins/coding/skills'
DISCOVERY = ROOT / 'ai/plugins/delegating/skills/use-subagents'
STANDARDS = {p.parent.name for p in SKILLS.glob('apply-*-standards/SKILL.md')}


class TechnologyStandardsTest(unittest.TestCase):
    def test_standards_resource_closure_survives_relocation(self):
        bundles = STANDARDS | {'create-mcp-server'}
        self.assertTrue(STANDARDS)
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as scratch:
            for name in bundles:
                bundle = Path(scratch) / name
                shutil.copytree(SKILLS / name, bundle)
                visited, pending = set(), [bundle / 'SKILL.md']
                while pending:
                    path = pending.pop().resolve()
                    if path in visited:
                        continue
                    visited.add(path)
                    for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                        if '://' in link or link.startswith('#'):
                            continue
                        target = (path.parent / link.split('#')[0]).resolve()
                        self.assertTrue(target.is_relative_to(bundle.resolve()), link)
                        self.assertTrue(target.is_file(), link)
                        if target.suffix == '.md':
                            pending.append(target)
                self.assertIn((bundle / 'references/requirements.md').resolve(), visited)

    def test_discovery_uses_native_generic_role_without_aliases(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as scratch:
            project = Path(scratch)
            native = project / '.codex/agents'
            native.mkdir(parents=True)
            source = AGENTS / 'reviewer.toml'
            shutil.copy2(source, native / source.name)
            def fetch(name):
                return subprocess.run(
                    ['sh', str(DISCOVERY / 'scripts/subagents'), '--project', str(project),
                     '--harness', 'codex', '--scope', 'project', 'fetch', name],
                    cwd=project, env=os.environ, text=True, capture_output=True)
            result = fetch('reviewer')
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(source.read_text(), result.stdout)
            self.assertNotEqual(0, fetch('unknown-role').returncode)

    def test_evaluation_inputs_resolve_without_claiming_model_results(self):
        names = STANDARDS
        for name in names:
            fixture = ROOT / 'tests/fixtures/workflow_skill_evals' / name / 'evals.json'
            data = json.loads(fixture.read_text())
            self.assertEqual(name, data['skill_name'])
            self.assertEqual('not-run', data['status'])
            self.assertEqual({'representative', 'held-out'}, {row['split'] for row in data['evals']})
            for row in data['evals']:
                if 'native_agents' in row:
                    self.assertNotIn('role', row)
                    self.assertEqual({'codex': 'worker', 'opencode': 'general'}, row['native_agents'])
                else:
                    self.assertTrue((AGENTS / (row['role'] + '.toml')).is_file())
                # Some scenarios target the whole skill rather than one reference.
                target = SKILLS / name / row.get('reference', 'SKILL.md')
                self.assertTrue(target.is_file())
                self.assertTrue(row['prompt'] and row['expectations'])


if __name__ == '__main__':
    unittest.main()
