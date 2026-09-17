"""Independent PDF reader fixtures, including image-only and blank pages."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'ai/plugins/researching/skills/read-pdf/scripts/read_pdf.py'
PYTHON = os.environ.get('SKILL_TEST_PYTHON', sys.executable)


class ReadPdfTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'tests')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        code = '''from reportlab.pdfgen import canvas
from PIL import Image
Image.new('RGB',(10,10),'blue').save('image.png')
c=canvas.Canvas('source.pdf',pagesize=(400,600));c.setTitle('Evidence title');c.setAuthor('Fixture')
c.drawString(40,500,'First page has sufficient extractable evidence.');c.showPage()
c.drawImage('image.png',40,200,width=200,height=200);c.showPage()
c.drawString(40,500,'Third page contains more evidence for selection.');c.showPage()
c.showPage();c.save()
'''
        result = subprocess.run([PYTHON,'-c',code],cwd=self.root,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)

    def cli(self,*args,script=SCRIPT,flags=()):
        return subprocess.run([PYTHON,*flags,str(script),'--project',str(self.root),*args],
                              cwd=self.root,capture_output=True,text=True)

    def test_page_locations_metadata_scan_indicators_and_preservation(self):
        source=self.root/'source.pdf';before=source.read_bytes()
        result=self.cli('read','source.pdf')
        self.assertEqual(result.returncode,0,result.stderr)
        data=json.loads(result.stdout)
        self.assertEqual(data['page_count'],4)
        self.assertEqual(data['metadata']['title'],'Evidence title')
        self.assertEqual(data['sha256'],hashlib.sha256(before).hexdigest())
        self.assertEqual(source.read_bytes(),before)
        self.assertEqual(data['pages'][0]['location'],'page-1')
        self.assertEqual(data['pages'][0]['width'],400)
        self.assertFalse(data['pages'][0]['insufficient_text'])
        for index in (1,3):
            page=data['pages'][index]
            self.assertEqual(page['text'],'')
            self.assertTrue(page['missing_text'])
            self.assertTrue(page['possible_scan'])
            self.assertFalse(page['truncated'])
        self.assertFalse(data['truncated'])

    def test_selection_truncation_invalid_input_and_missing_dependency(self):
        result=self.cli('read','source.pdf','--pages','3,1-1')
        self.assertEqual(result.returncode,0,result.stderr)
        data=json.loads(result.stdout)
        self.assertEqual(data['selected_pages'],[1,3])
        self.assertEqual([p['page'] for p in data['pages']],[1,3])
        result=self.cli('read','source.pdf','--pages','1','--max-chars','5')
        data=json.loads(result.stdout)
        self.assertEqual(data['pages'][0]['text'],'First')
        self.assertTrue(data['pages'][0]['truncated'])
        self.assertFalse(data['pages'][0]['missing_text'])
        self.assertTrue(data['truncated'])
        for value in ('0','5','3-1','a','1,'):
            self.assertEqual(self.cli('read','source.pdf','--pages',value).returncode,2)
        self.assertEqual(self.cli('check',flags=('-S',)).returncode,3)
        self.assertEqual(self.cli('check').returncode,0)
        (self.root/'bad.pdf').write_bytes(b'%PDF-1.7\nPRIVATE BROKEN PDF')
        result=self.cli('read','bad.pdf')
        self.assertEqual(result.returncode,4)
        self.assertNotIn('PRIVATE',result.stderr)
        (self.root/'link.pdf').symlink_to(self.root/'source.pdf')
        self.assertEqual(self.cli('read','link.pdf').returncode,2)
        self.assertEqual(self.cli('read','../escape.pdf').returncode,2)

    def test_isolated_bundle_leaves_all_files_unchanged(self):
        installed=self.root/'installed'/'read-pdf'
        shutil.copytree(SCRIPT.parents[1],installed,ignore=shutil.ignore_patterns('__pycache__'))
        before={p.relative_to(self.root):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result=self.cli('read','source.pdf',script=installed/'scripts/read_pdf.py')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(before,{p.relative_to(self.root):p.read_bytes() for p in self.root.rglob('*') if p.is_file()})


if __name__=='__main__':
    unittest.main()
