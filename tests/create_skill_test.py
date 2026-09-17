"""Exercise portable skill packaging, evaluation evidence, and output boundaries."""
import hashlib
import json
import os
import re
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'ai/plugins/coding/skills/create-skill'
PYTHON = os.environ.get('SKILL_TEST_PYTHON', sys.executable)


class CreateSkillTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'tests')
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.source = self.project / 'example'
        self.source.mkdir()
        (self.source / 'SKILL.md').write_text(
            '---\nname: example\ndescription: Create example artifacts.\n---\n# Example\n')
        (self.source / 'data.txt').write_text('café')

    def run_cli(self, *args, python=PYTHON, flags=()):
        return subprocess.run([python, *flags, str(SKILL / 'scripts/create_skill.py'),
                               '--project', str(self.project), *map(str, args)],
                              cwd=self.project, capture_output=True, text=True)

    def test_package_reopens_and_preserves_input(self):
        before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in self.source.iterdir()}
        result = self.run_cli('package', 'example', 'example.skill')
        self.assertEqual(result.returncode, 0, result.stderr)
        with zipfile.ZipFile(self.project / 'example.skill') as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(set(archive.namelist()),
                             {'example/SKILL.md', 'example/data.txt'})
            self.assertEqual(archive.read('example/data.txt').decode(), 'café')
        self.assertEqual(before, {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in self.source.iterdir()})
        result = self.run_cli('package', 'example', 'example.skill')
        self.assertEqual(result.returncode, 2)

    def test_rejects_escape_symlink_and_source_output(self):
        for output in ('../escape.skill', 'example/output.skill'):
            result = self.run_cli('package', 'example', output)
            self.assertEqual(result.returncode, 2, result.stderr)
        (self.project / 'linked').symlink_to(self.source, target_is_directory=True)
        self.assertEqual(self.run_cli('package', 'linked', 'bad.skill').returncode, 2)
        (self.source / 'linked.txt').symlink_to(self.source / 'data.txt')
        self.assertEqual(self.run_cli('package', 'example', 'bad.skill').returncode, 2)
        self.assertFalse((self.project / 'bad.skill').exists())

    def test_missing_dependency_and_invalid_frontmatter(self):
        result = self.run_cli('validate', 'example', flags=('-S',))
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertIn('PyYAML', result.stderr)
        (self.source / 'SKILL.md').write_text('---\nname: other\ndescription: test\n---\n')
        result = self.run_cli('package', 'example', 'invalid.skill')
        self.assertEqual(result.returncode, 5, result.stderr)
        self.assertFalse((self.project / 'invalid.skill').exists())

    def put_run(self, config, expectations, timing=None):
        path = self.project / 'evaluation' / 'eval-1' / config / 'run-1'
        path.mkdir(parents=True)
        (path / 'grading.json').write_text(json.dumps({
            'expectations': expectations, 'execution_metrics': {'output_chars': 9999}}))
        if timing is not None:
            (path / 'timing.json').write_text(json.dumps(timing))
        return path

    def test_benchmark_preserves_missing_metrics_and_generates_report(self):
        self.put_run('with_skill', [{'text': 'Correct', 'passed': True, 'evidence': 'Artifact inspected'}])
        self.put_run('without_skill', [{'text': 'Correct', 'passed': False, 'evidence': 'Output absent'}],
                     {'total_duration_seconds': 2.5, 'total_tokens': 17})
        result = self.run_cli('benchmark', 'evaluation', 'benchmark.json')
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((self.project / 'benchmark.json').read_text())
        runs = {r['configuration']: r for r in data['runs']}
        self.assertIsNone(runs['with_skill']['result']['tokens'])
        self.assertIsNone(data['run_summary']['with_skill']['tokens']['mean'])
        self.assertEqual(runs['without_skill']['result']['tokens'], 17)
        self.assertEqual(data['run_summary']['delta']['pass_rate'], 1)
        self.assertIsNone(data['run_summary']['delta']['tokens'])
        self.assertIn('eval-1/with_skill/run-1/grading.json', runs['with_skill']['source'])
        result = self.run_cli('report', 'benchmark.json', 'report.md')
        self.assertEqual(result.returncode, 0, result.stderr)
        report = (self.project / 'report.md').read_text()
        self.assertIn('unavailable', report)
        self.assertIn('1/1', report)
        self.assertEqual(self.run_cli('report', 'benchmark.json', 'report.md').returncode, 2)

    def test_invalid_evidence_is_not_silently_skipped(self):
        path = self.put_run('with_skill', [{'text': 'Secret content', 'passed': 'yes', 'evidence': ''}])
        result = self.run_cli('benchmark', 'evaluation', 'bad.json')
        self.assertEqual(result.returncode, 5, result.stderr)
        self.assertNotIn('Secret content', result.stderr)
        self.assertFalse((self.project / 'bad.json').exists())
        (path / 'grading.json').write_text('{invalid')
        self.assertEqual(self.run_cli('benchmark', 'evaluation', 'bad.json').returncode, 2)

    def test_installed_benchmark_is_read_only_and_independent(self):
        installed = self.project / 'installation' / 'create-skill'
        shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns('__pycache__'))
        self.put_run('with_skill', [{'text': 'Correct', 'passed': True, 'evidence': 'Checked'}])
        before = {p.relative_to(installed): p.read_bytes()
                  for p in installed.rglob('*') if p.is_file()}
        result = subprocess.run([PYTHON, str(installed / 'scripts/create_skill.py'),
                                 '--project', str(self.project), 'benchmark',
                                 'evaluation', 'isolated.json'], cwd=self.source,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        after = {p.relative_to(installed): p.read_bytes()
                 for p in installed.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        result = subprocess.run([PYTHON, str(installed / 'scripts/create_skill.py'),
                                 '--project', str(self.project), 'report', 'isolated.json',
                                 str(installed / 'forbidden.md')], cwd=self.source,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn('read-only', result.stderr)

    def test_invalid_measurements_summary_and_missing_run(self):
        path = self.put_run('with_skill', [{'text': 'Correct', 'passed': True, 'evidence': 'Checked'}])
        original = json.loads((path / 'grading.json').read_text())
        for timing in ({'total_tokens': -1}, {'total_tokens': True},
                       {'total_duration_seconds': float('nan')}):
            (path / 'timing.json').write_text(json.dumps(timing))
            result = self.run_cli('benchmark', 'evaluation', 'bad.json')
            self.assertEqual(result.returncode, 5, result.stderr)
        (path / 'timing.json').write_text('{}')
        bad = dict(original, summary={'passed': 0, 'failed': 1, 'total': 1, 'pass_rate': 0})
        (path / 'grading.json').write_text(json.dumps(bad))
        self.assertEqual(self.run_cli('benchmark', 'evaluation', 'bad.json').returncode, 5)
        (path / 'grading.json').write_text(json.dumps(original))
        (path.parent / 'run-2').mkdir()
        self.assertEqual(self.run_cli('benchmark', 'evaluation', 'bad.json').returncode, 5)

    def documented_example(self, section):
        content=(SKILL/'references/schemas.md').read_text()
        body=content.split('## '+section+'\n',1)[1]
        return json.loads(re.search(r'```json\n(.*?)\n```',body,re.DOTALL)[1])

    def test_documented_grading_example_is_accepted(self):
        path=self.project/'evaluation/eval-1/with_skill/run-1'
        path.mkdir(parents=True)
        (path/'grading.json').write_text(json.dumps(self.documented_example('grading.json')))
        result=self.run_cli('benchmark','evaluation','documented.json')
        self.assertEqual(result.returncode,0,result.stderr)

    def test_documented_benchmark_example_is_accepted(self):
        (self.project/'documented.json').write_text(json.dumps(self.documented_example('benchmark.json')))
        result=self.run_cli('report','documented.json','documented.md')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('## Evidence',(self.project/'documented.md').read_text())

    def test_check_and_installed_resource_write_refusal(self):
        result = self.run_cli('check')
        self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run([PYTHON, str(SKILL / 'scripts/create_skill.py'),
                                 '--project', str(ROOT), 'report', 'PLAN.md',
                                 str(SKILL / 'forbidden.md')], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((SKILL / 'forbidden.md').exists())


if __name__ == '__main__':
    unittest.main()
