"""Portable bundle/resource contracts, not model-behavior evaluations."""

import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'ai/plugins/coding/skills'


class CodingWorkflowContractTest(unittest.TestCase):
    def test_final_coding_catalog_has_only_current_entry_points(self):
        expected = {'develop-code', 'review-code', 'resolve-review-feedback',
                    'format-code', 'run-tests', 'verify-interface', 'manage-changes',
                    'write-requirements', 'prepare-implementation', 'map-codebase',
                    'recover-ralph', 'create-skill', 'create-mcp-server'}
        actual = {path.parent.name for path in SKILLS.glob('*/SKILL.md')}
        self.assertEqual(actual, expected)
        for path in SKILLS.glob('*/SKILL.md'):
            header = path.read_text().split('---', 2)[1]
            self.assertEqual(re.findall(r'^name: (.+)$', header, re.M),
                             [path.parent.name])

    def test_review_copy_contains_reachable_scopes_and_local_resources(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            bundle = Path(directory) / 'review-code'
            shutil.copytree(SKILLS / 'review-code', bundle)
            root = bundle / 'SKILL.md'
            root_links = re.findall(r'\]\(([^)]+)\)', root.read_text())
            scopes = {'local-changes', 'pull-request', 'component-review', 'codebase-audit'}
            self.assertTrue({f'references/scopes/{name}.md' for name in scopes}
                            .issubset(root_links))
            for path in bundle.rglob('*.md'):
                for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                    if '://' in link or link.startswith('#'):
                        continue
                    target = (path.parent / link.split('#')[0]).resolve()
                    self.assertTrue(target.is_relative_to(bundle.resolve()), link)
                    self.assertTrue(target.is_file(), link)

    def test_development_bundle_has_unique_matching_metadata(self):
        source = SKILLS / 'develop-code/SKILL.md'
        self.assertTrue(source.is_file(), 'Missing unified development entry point')
        header = source.read_text().split('---', 2)[1]
        self.assertEqual(re.findall(r'^name: (.+)$', header, re.M), ['develop-code'])
        descriptions = re.findall(r'^description: (.+)$', header, re.M)
        self.assertEqual(len(descriptions), 1)
        self.assertTrue(descriptions[0].strip())
        names = []
        for path in (ROOT / 'ai/plugins').glob('*/skills/*/SKILL.md'):
            header = path.read_text().split('---', 2)[1]
            names.extend(re.findall(r'^name: (.+)$', header, re.M))
        self.assertEqual(names.count('develop-code'), 1)

    def test_development_copy_resolves_all_bundled_links(self):
        source = SKILLS / 'develop-code'
        self.assertTrue(source.is_dir(), 'Missing development bundle')
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            bundle = Path(directory) / 'isolated/develop-code'
            shutil.copytree(source, bundle)
            required = {'SKILL.md', 'references/testing-strategy.md',
                        'references/testing-anti-patterns.md',
                        'references/actions/feature.md',
                        'references/actions/bugfix.md',
                        'references/actions/refactor.md'}
            self.assertTrue(required.issubset(
                {str(p.relative_to(bundle)) for p in bundle.rglob('*.md')}))
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
            self.assertTrue(required.issubset(
                {str(p.relative_to(bundle.resolve())) for p in visited}))

    def test_substantive_testing_reference_preserves_baseline_bytes(self):
        fixture = json.loads((ROOT / 'tests/fixtures/coding_workflow_evals.json').read_text())
        original = 'ai/plugins/coding/skills/develop-with-tests/references/testing-anti-patterns.md'
        digest = next(item['sha256'] for item in fixture['baseline']['artifacts']
                      if item['path'] == original)
        target = SKILLS / 'develop-code/references/testing-anti-patterns.md'
        self.assertTrue(target.is_file(), 'Missing preserved testing guidance')
        self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), digest)


if __name__ == '__main__':
    unittest.main()
