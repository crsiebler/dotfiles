"""Independent workbook reading fixtures; formula caches are never calculation."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'ai/plugins/researching/skills/read-xlsx/scripts/read_xlsx.py'
PYTHON = os.environ.get('SKILL_TEST_PYTHON', sys.executable)


class ReadXlsxTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'tests')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        code = '''import xlsxwriter
w=xlsxwriter.Workbook('fixture.xlsx',{'strings_to_formulas':False,'strings_to_urls':False})
s=w.add_worksheet('Data')
s.write_string('A1','001');s.write_string('B1','=literal');s.write_string('C1','https://example.com')
s.write_formula('A2','=1+2',None,3);s.write_formula('B2','=1+3',None,0);s.write_formula('C2','=1+4',None,0)
s.set_row(1,None,None,{'hidden':True});s.set_column('B:C',None,None,{'hidden':True})
s=w.add_worksheet('Secret');s.hide();s.write_string('A1','Hidden evidence')
w.close()
'''
        result = subprocess.run([PYTHON, '-c', code], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        # Independently remove B2's formula cache and falsify the dimension hint.
        with zipfile.ZipFile(self.root / 'fixture.xlsx') as source, zipfile.ZipFile(self.root / 'source.xlsx', 'w') as target:
            for name in source.namelist():
                content = source.read(name)
                if name == 'xl/worksheets/sheet1.xml':
                    xml = ET.fromstring(content);ns = {'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                    cell = xml.find('.//s:c[@r="B2"]', ns);cell.remove(cell.find('s:v', ns))
                    xml.find('s:dimension', ns).set('ref', 'A1:A1')
                    content = ET.tostring(xml)
                target.writestr(name, content)

    def cli(self, *args, script=SCRIPT, flags=()):
        return subprocess.run([PYTHON, *flags, str(script), '--project', str(self.root), *args],
                              cwd=self.root, capture_output=True, text=True)

    def test_cells_hidden_spans_formula_cache_and_preservation(self):
        before = (self.root / 'source.xlsx').read_bytes()
        result = self.cli('read', 'source.xlsx')
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data['sha256'], hashlib.sha256(before).hexdigest())
        self.assertEqual((self.root / 'source.xlsx').read_bytes(), before)
        self.assertFalse(data['truncated'])
        self.assertEqual(data['sheets'][1]['state'], 'hidden')
        cells = {c['coordinate']:c for c in data['sheets'][0]['cells']}
        self.assertEqual(cells['A1']['value'], '001')
        self.assertEqual(cells['B1']['value'], '=literal')
        self.assertEqual(cells['C1']['value'], 'https://example.com')
        self.assertEqual(cells['A2']['formula'], '=1+2')
        self.assertEqual(cells['A2']['cached'], 3)
        self.assertEqual(cells['B2']['cache_status'], 'missing')
        self.assertIsNone(cells['B2']['cached'])
        self.assertEqual(cells['C2']['cache_status'], 'present')
        self.assertEqual(cells['C2']['cached'], 0)
        self.assertTrue(cells['A2']['row_hidden'])
        self.assertTrue(cells['B1']['column_hidden'])
        self.assertTrue(cells['C1']['column_hidden'])
        self.assertFalse(cells['A1']['column_hidden'])

    def test_ranges_limits_and_invalid_inputs(self):
        result = self.cli('read', 'source.xlsx', '--sheet', 'Data', '--range', 'B1:C2')
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual([c['coordinate'] for c in data['sheets'][0]['cells']], ['B1','C1','B2','C2'])
        self.assertEqual(len(data['sheets']), 1)
        partial = json.loads(self.cli('read', 'source.xlsx', '--sheet', 'Data', '--max-cells', '5').stdout)
        self.assertEqual([c['coordinate'] for c in partial['sheets'][0]['cells']], ['A1','B1','C1','A2','B2'])
        self.assertTrue(partial['truncated'])
        result = self.cli('read', 'source.xlsx', '--max-cells', '2', '--max-chars', '2')
        data = json.loads(result.stdout)
        self.assertTrue(data['truncated'])
        self.assertEqual(sum(len(s['cells']) for s in data['sheets']), 2)
        for region in ('A:A','2:3','B2:A1','A0','XFE1','Sheet!A1'):
            self.assertEqual(self.cli('read', 'source.xlsx', '--range', region).returncode, 2)
        self.assertEqual(self.cli('read', 'source.xlsx', '--sheet', 'Absent').returncode, 2)
        self.assertEqual(self.cli('check', flags=('-S',)).returncode, 3)
        self.assertEqual(self.cli('check').returncode, 0)
        (self.root / 'link.xlsx').symlink_to(self.root / 'source.xlsx')
        self.assertEqual(self.cli('read', 'link.xlsx').returncode, 2)
        self.assertEqual(self.cli('read', '../escape.xlsx').returncode, 2)
        (self.root / 'bad.xlsx').write_text('PRIVATE INPUT')
        result = self.cli('read', 'bad.xlsx')
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('PRIVATE', result.stderr)

    def test_isolated_bundle_preserves_all_files(self):
        installed = self.root / 'installed' / 'read-xlsx'
        shutil.copytree(SCRIPT.parents[1], installed, ignore=shutil.ignore_patterns('__pycache__'))
        before = {p.relative_to(self.root):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = self.cli('read', 'source.xlsx', script=installed / 'scripts/read_xlsx.py')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, {p.relative_to(self.root):p.read_bytes() for p in self.root.rglob('*') if p.is_file()})


if __name__ == '__main__':
    unittest.main()
