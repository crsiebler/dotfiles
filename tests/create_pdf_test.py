"""Original PDF helper tests with licensed font, literal text and failure checks."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'ai/plugins/producing/skills/create-pdf/scripts/create_pdf.py'
PYTHON = os.environ.get('SKILL_TEST_PYTHON', sys.executable)


class CreatePdfTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'tests')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        code = '''from pathlib import Path
import reportlab, shutil
from PIL import Image
fonts=Path(reportlab.__file__).parent/'fonts'
for name in ('Vera.ttf','bitstream-vera-license.txt'):shutil.copyfile(fonts/name,name)
Image.new('RGB',(80,40),'blue').save('image.png')
'''
        result = subprocess.run([PYTHON, '-c', code], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.request = {'font':'Vera.ttf','blocks':[
            {'kind':'heading','text':'Résumé & results'},
            {'kind':'paragraph','text':'Literal <tag> & text.'},
            {'kind':'table','rows':[['Region','Units'],['East','12'],['West','18']]},
            {'kind':'image','path':'image.png','width':2},
            {'kind':'page_break'},
            {'kind':'paragraph','text':'Second page evidence.'}]}

    def cli(self, *args, script=SCRIPT, flags=()):
        return subprocess.run([PYTHON, *flags, str(script), '--project', str(self.root), *args],
                              cwd=self.root, capture_output=True, text=True)

    def create(self, request=None, name='report.pdf'):
        (self.root / 'request.json').write_text(json.dumps(self.request if request is None else request))
        return self.cli('create', 'request.json', name)

    def test_pages_text_table_image_font_geometry_and_input_preservation(self):
        before = {name:(self.root/name).read_bytes() for name in ('Vera.ttf','image.png')}
        result = self.create()
        self.assertEqual(result.returncode, 0, result.stderr)
        code = '''import json
from pypdf import PdfReader
p=PdfReader('report.pdf')
fonts=[f.get_object() for page in p.pages for f in page['/Resources']['/Font'].get_object().values()]
print(json.dumps({'pages':len(p.pages),'text':[page.extract_text() for page in p.pages],
 'sizes':[[float(page.mediabox.width),float(page.mediabox.height)] for page in p.pages],
 'embedded':any('/FontDescriptor' in f and '/FontFile2' in f['/FontDescriptor'] for f in fonts),
 'images':sum(len(page.images) for page in p.pages)}))
'''
        check = subprocess.run([PYTHON, '-c', code], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(check.returncode, 0, check.stderr)
        data = json.loads(check.stdout)
        self.assertEqual(data['pages'], 2)
        self.assertEqual(data['sizes'], [[612,792],[612,792]])
        for value in ('Résumé & results','Literal <tag> & text.','Region','East','12','Page 1'):
            self.assertIn(value, data['text'][0])
        self.assertIn('Second page evidence.', data['text'][1])
        self.assertIn('Page 2', data['text'][1])
        self.assertTrue(data['embedded']);self.assertEqual(data['images'], 1)
        self.assertEqual(before, {name:(self.root/name).read_bytes() for name in before})
        self.assertEqual(self.cli('inspect','report.pdf').returncode, 0)

    def test_invalid_fonts_glyphs_size_layout_and_collisions(self):
        for change in (lambda r:r.update(font='missing.ttf'),
                       lambda r:r['blocks'][0].update(text='Missing glyph 😀'),
                       lambda r:r['blocks'][3].update(width=20),
                       lambda r:r.update(page={'width':3,'height':3,'margin':2}),
                       lambda r:r['blocks'][2].update(rows=[['x'*20000]])):
            request=json.loads(json.dumps(self.request));change(request)
            result=self.create(request)
            self.assertIn(result.returncode,(2,4),result.stderr)
            self.assertFalse((self.root/'report.pdf').exists())
        self.assertEqual(self.create().returncode,0)
        before=(self.root/'report.pdf').read_bytes()
        self.assertEqual(self.create().returncode,2)
        self.assertEqual((self.root/'report.pdf').read_bytes(),before)
        self.assertEqual(self.create(name='../escape.pdf').returncode,2)
        (self.root/'link.ttf').symlink_to(self.root/'Vera.ttf');self.request['font']='link.ttf'
        self.assertEqual(self.create(name='fresh.pdf').returncode,2)
        self.assertEqual(self.cli('check',flags=('-S',)).returncode,3)
        self.assertEqual(self.cli('check').returncode,0)

    def test_table_paginates_with_repeated_headers(self):
        request = {'font':'Vera.ttf','blocks':[{'kind':'table','rows':
            [['Record','Description']]+[[str(i),f'Entry {i}'] for i in range(80)]}]}
        result = self.create(request)
        self.assertEqual(result.returncode,0,result.stderr)
        data = json.loads(self.cli('inspect','report.pdf').stdout)
        self.assertGreater(data['page_count'],1)
        self.assertFalse(data['truncated'])
        self.assertTrue(all('Record' in page['text'] for page in data['pages']))
        self.assertIn('Entry 79',data['pages'][-1]['text'])

    def test_isolated_documented_recipe(self):
        installed=self.root/'installed'/'create-pdf'
        shutil.copytree(SCRIPT.parents[1],installed,ignore=shutil.ignore_patterns('__pycache__'))
        before={p.relative_to(installed):p.read_bytes() for p in installed.rglob('*') if p.is_file()}
        recipe=re.search(r'```json\n(.*?)\n```',(installed/'references/authoring.md').read_text(),re.S).group(1)
        (self.root/'recipe.json').write_text(recipe)
        result=self.cli('create','recipe.json','recipe.pdf',script=installed/'scripts/create_pdf.py')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(before,{p.relative_to(installed):p.read_bytes() for p in installed.rglob('*') if p.is_file()})


if __name__ == '__main__':
    unittest.main()
