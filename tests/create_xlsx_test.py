"""Literal data and cache correctness for original XLSX production helpers."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'ai/plugins/producing/skills/create-xlsx/scripts/create_xlsx.py'
PYTHON = os.environ.get('SKILL_TEST_PYTHON', sys.executable)
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def cell(kind, value=None, **extra):
    return dict(type=kind, **({} if kind == 'blank' else {'value': value}), **extra)


class CreateXlsxTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'tests')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.request = {'formats': {'cash': {'num_format': '$0.00'}}, 'sheets': [
            {'name': 'Data', 'table': True, 'freeze': [1, 0], 'widths': [24, 20], 'rows': [
                [cell('string', 'Label'), cell('string', 'Value')],
                [cell('string', '001'), cell('number', 12.5, format='cash')],
                [cell('string', '=SUM(A1:A2)'), cell('formula', '=B2*2', cached=25)],
                [cell('string', 'https://example.com'), cell('formula', '=B2+1')]],
             'charts': [{'at': [6, 0], 'category_column': 0, 'value_columns': [1]}]},
            {'name': 'Types', 'filter': True, 'rows': [
                [cell('string', 'Flag'), cell('string', 'Date')],
                [cell('boolean', True), cell('date', '2026-09-17')]]}]}

    def cli(self, *args, script=SCRIPT, flags=()):
        return subprocess.run([PYTHON, *flags, str(script), '--project', str(self.root), *args],
                              cwd=self.root, capture_output=True, text=True)

    def create(self, request=None, name='book.xlsx'):
        (self.root / 'request.json').write_text(json.dumps(self.request if request is None else request))
        return self.cli('create', 'request.json', name)

    def test_literal_strings_types_caches_and_workbook_features(self):
        result = self.create()
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual([f['cache_source'] for f in report['formulas']], ['supplied', 'writer_placeholder'])
        self.assertFalse(report['recalculated'])
        with zipfile.ZipFile(self.root / 'book.xlsx') as archive:
            sheet = ET.fromstring(archive.read('xl/worksheets/sheet1.xml'))
            strings = ET.fromstring(archive.read('xl/sharedStrings.xml'))
            values = [''.join(n.itertext()) for n in strings]
            for address, literal in [('A2', '001'), ('A3', '=SUM(A1:A2)'), ('A4', 'https://example.com')]:
                item = sheet.find(f'.//s:c[@r="{address}"]', NS)
                self.assertEqual(item.get('t'), 's')
                self.assertEqual(values[int(item.find('s:v', NS).text)], literal)
                self.assertIsNone(item.find('s:f', NS))
            self.assertIsNone(sheet.find('s:hyperlinks', NS))
            self.assertEqual(sheet.find('.//s:c[@r="B3"]/s:f', NS).text, 'B2*2')
            self.assertEqual(sheet.find('.//s:c[@r="B3"]/s:v', NS).text, '25')
            self.assertEqual(sheet.find('.//s:c[@r="B4"]/s:v', NS).text, '0')
            self.assertEqual(sheet.find('.//s:pane', NS).get('state'), 'frozen')
            self.assertIn('xl/tables/table1.xml', archive.namelist())
            self.assertIn('xl/charts/chart1.xml', archive.namelist())
            other = ET.fromstring(archive.read('xl/worksheets/sheet2.xml'))
            self.assertEqual(other.find('s:autoFilter', NS).get('ref'), 'A1:B2')
            workbook = ET.fromstring(archive.read('xl/workbook.xml'))
            self.assertEqual(workbook.find('s:calcPr', NS).get('fullCalcOnLoad'), '1')
        result = self.cli('inspect', 'book.xlsx')
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertFalse(data['truncated'])
        formulas = [c for s in data['sheets'] for c in s['cells'] if c['type'] == 'f']
        self.assertEqual([c['cached'] for c in formulas], [25, 0])
        self.assertTrue(all(c['cache_source'] == 'unknown' for c in formulas))

    def test_invalid_rows_names_truncation_collisions_and_boundaries(self):
        for change in (lambda r: r['sheets'][0].update(name='bad/name'),
                       lambda r: r['sheets'][1].update(name='data'),
                       lambda r: r['sheets'][0]['rows'].append([cell('string', 'short')]),
                       lambda r: r['sheets'][0]['rows'][1][0].update(value='x'*32768),
                       lambda r: r['sheets'][0].update(filter=True),
                       lambda r: r['sheets'][0]['rows'][1][1].update(value=float('inf'))):
            request = json.loads(json.dumps(self.request)); change(request)
            result = self.create(request)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertFalse((self.root / 'book.xlsx').exists())
        self.assertEqual(self.create().returncode, 0)
        before = (self.root / 'book.xlsx').read_bytes()
        self.assertEqual(self.create().returncode, 2)
        self.assertEqual((self.root / 'book.xlsx').read_bytes(), before)
        self.assertEqual(self.create(name='../escape.xlsx').returncode, 2)
        (self.root / 'alias.json').symlink_to(self.root / 'request.json')
        self.assertEqual(self.cli('create', 'alias.json', 'new.xlsx').returncode, 2)
        self.assertEqual(self.cli('check', flags=('-S',)).returncode, 3)
        self.assertEqual(self.cli('check').returncode, 0)

    def test_writer_failures_do_not_publish_or_modify_request(self):
        (self.root / 'request.json').write_text(json.dumps(self.request))
        before = (self.root / 'request.json').read_bytes()
        code = """import sys
from unittest.mock import patch
sys.dont_write_bytecode=True
sys.path.insert(0,sys.argv[1])
import create_xlsx
root=sys.argv[2]
for target,kwargs in [('xlsxwriter.worksheet.Worksheet.write_string',{'return_value':-2}),
                      ('xlsxwriter.workbook.Workbook.close',{'side_effect':OSError('PRIVATE DIAGNOSTIC')})]:
    sys.argv=['create_xlsx','--project',root,'create','request.json','failed.xlsx']
    with patch(target,**kwargs):
        assert create_xlsx.main()==4
"""
        result = subprocess.run([PYTHON, '-c', code, str(SCRIPT.parent), str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('PRIVATE', result.stderr)
        self.assertFalse((self.root / 'failed.xlsx').exists())
        self.assertEqual((self.root / 'request.json').read_bytes(), before)

    def test_documented_recipe_isolated_and_readonly_resources(self):
        installed = self.root / 'installed' / 'create-xlsx'
        shutil.copytree(SCRIPT.parents[1], installed, ignore=shutil.ignore_patterns('__pycache__'))
        before = {p.relative_to(installed): p.read_bytes() for p in installed.rglob('*') if p.is_file()}
        recipe = re.search(r'```json\n(.*?)\n```', (installed / 'references/authoring.md').read_text(), re.S).group(1)
        (self.root / 'recipe.json').write_text(recipe)
        result = self.cli('create', 'recipe.json', 'recipe.xlsx', script=installed / 'scripts/create_xlsx.py')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, {p.relative_to(installed): p.read_bytes() for p in installed.rglob('*') if p.is_file()})
        self.assertEqual(self.cli('create', 'recipe.json', 'installed/create-xlsx/no.xlsx',
                                 script=installed / 'scripts/create_xlsx.py').returncode, 2)


if __name__ == '__main__':
    unittest.main()
