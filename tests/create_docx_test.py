"""DOCX artifacts inspected independently of the creation helper."""
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
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'ai/plugins/producing/skills/create-docx/scripts/create_docx.py'
PYTHON = os.environ.get('SKILL_TEST_PYTHON', sys.executable)
NS = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


class CreateDocxTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'tests')
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def cli(self, operation, spec=None, output='result.docx', flags=()):
        args=[PYTHON,*flags,str(SCRIPT),'--project',str(self.root),operation]
        if spec is not None:
            (self.root/'request.json').write_text(json.dumps(spec))
            args+=['request.json',output]
        elif operation=='inspect':
            args+=[output]
        return subprocess.run(args,cwd=self.root,capture_output=True,text=True)

    def test_full_document_content_relationships_styles_and_layout(self):
        code="from PIL import Image; Image.new('RGB',(20,10),'blue').save('image.png')"
        subprocess.run([PYTHON,'-c',code],cwd=self.root,check=True)
        original=(self.root/'image.png').read_bytes()
        spec={'styles':{'Body':{'font_name':'Arial','size_pt':12,'bold':True}},
              'page':{'left_margin_inches':1.25}, 'blocks':[
                  {'type':'heading','text':'Résumé 世界','level':1},
                  {'type':'paragraph','text':'Literal <tags> & café','style':'Body'},
                  {'type':'table','rows':[['A','B'],['01','two']]},
                  {'type':'image','path':'image.png','width_inches':2},
                  {'type':'page_break'},
                  {'type':'section','page':{'width_inches':11,'height_inches':8.5}},
                  {'type':'paragraph','text':'Landscape'}]}
        result=self.cli('create',spec)
        self.assertEqual(result.returncode,0,result.stderr)
        with zipfile.ZipFile(self.root/'result.docx') as archive:
            self.assertIsNone(archive.testzip())
            document=ET.fromstring(archive.read('word/document.xml'))
            text=''.join(document.itertext())
            self.assertIn('Résumé 世界',text)
            self.assertIn('Literal <tags> & café',text)
            self.assertEqual(len(document.findall('.//w:tbl',NS)),1)
            self.assertEqual(len(document.findall('.//w:br',NS)),1)
            sections=document.findall('.//w:sectPr',NS)
            self.assertEqual(len(sections),2)
            self.assertEqual(sections[-1].find('w:pgSz',NS).get('{'+NS['w']+'}w'),'15840')
            self.assertEqual(sections[0].find('w:pgMar',NS).get('{'+NS['w']+'}left'),'1800')
            styles=ET.fromstring(archive.read('word/styles.xml'))
            style=next(s for s in styles.findall('w:style',NS) if s.get('{'+NS['w']+'}styleId')=='Body')
            self.assertEqual(style.find('w:rPr/w:sz',NS).get('{'+NS['w']+'}val'),'24')
            self.assertIsNotNone(style.find('w:rPr/w:b',NS))
            relationships=archive.read('word/_rels/document.xml.rels').decode()
            self.assertIn('relationships/image',relationships)
            self.assertEqual(archive.read('word/media/image1.png'),original)
        self.assertEqual((self.root/'image.png').read_bytes(),original)
        inspected=self.cli('inspect')
        self.assertEqual(inspected.returncode,0,inspected.stderr)
        data=json.loads(inspected.stdout)
        self.assertEqual(data['inline_images'],1)
        self.assertEqual(data['page_breaks'],1)
        self.assertFalse(data['truncated'])

    def test_invalid_input_does_not_publish_or_overwrite(self):
        valid={'blocks':[{'type':'paragraph','text':'keep'}]}
        self.assertEqual(self.cli('create',valid).returncode,0)
        original=(self.root/'result.docx').read_bytes()
        self.assertEqual(self.cli('create',valid).returncode,2)
        self.assertEqual((self.root/'result.docx').read_bytes(),original)
        for spec in ({'blocks':[{'type':'unknown'}]},
                     {'blocks':[{'type':'table','rows':[['a'],['b','c']]}]},
                     {'page':{'width_inches':1},'blocks':valid['blocks']},
                     {'blocks':[{'type':'paragraph','text':'secret\x01'}]},
                     {'blocks':[{'type':'image','path':'missing.png','width_inches':2}]}):
            result=self.cli('create',spec,'bad.docx')
            self.assertNotEqual(result.returncode,0)
            self.assertFalse((self.root/'bad.docx').exists())
            self.assertNotIn('secret',result.stderr)
            self.assertNotIn('Traceback',result.stderr)
        self.assertEqual(self.cli('create',valid,'../escape.docx').returncode,2)
        (self.root/'link.docx').symlink_to(self.root/'result.docx')
        self.assertEqual(self.cli('inspect',output='link.docx').returncode,2)

    def test_bad_image_reports_error_without_traceback(self):
        (self.root/'bad.png').write_bytes(b'invalid image data')
        result=self.cli('create',{'blocks':[{'type':'image','path':'bad.png','width_inches':1}]})
        self.assertNotEqual(result.returncode,0)
        self.assertNotIn('Traceback',result.stderr)
        self.assertFalse((self.root/'result.docx').exists())

    def test_isolated_bundle_preserves_installed_resources(self):
        installed=self.root/'installed'/'create-docx'
        shutil.copytree(SCRIPT.parents[1],installed,ignore=shutil.ignore_patterns('__pycache__'))
        (self.root/'request.json').write_text(json.dumps({'blocks':[{'type':'paragraph','text':'independent'}]}))
        before={p.relative_to(installed):p.read_bytes() for p in installed.rglob('*') if p.is_file()}
        command=[PYTHON,str(installed/'scripts/create_docx.py'),'--project',str(self.root),'create','request.json']
        result=subprocess.run(command+['isolated.docx'],cwd=installed.parent,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(before,{p.relative_to(installed):p.read_bytes() for p in installed.rglob('*') if p.is_file()})
        result=subprocess.run(command+[str(installed/'forbidden.docx')],capture_output=True,text=True)
        self.assertEqual(result.returncode,2,result.stderr)
        self.assertFalse((installed/'forbidden.docx').exists())

    def test_documented_recipe_generates_a_document(self):
        reference=(SCRIPT.parents[1]/'references/authoring.md').read_text()
        spec=json.loads(re.search(r'```json\n(.*?)\n```',reference,re.DOTALL)[1])
        result=self.cli('create',spec)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout)['sections'],2)

    def test_dependency_check_and_missing_package(self):
        self.assertEqual(self.cli('check').returncode,0)
        result=self.cli('check',flags=('-S',))
        self.assertEqual(result.returncode,3)
        self.assertIn('python-docx',result.stderr)

    def test_bounded_inspection_and_invalid_package(self):
        spec={'blocks':[{'type':'paragraph','text':str(i)} for i in range(110)]}
        self.assertEqual(self.cli('create',spec).returncode,0)
        result=self.cli('inspect')
        data=json.loads(result.stdout)
        self.assertEqual(len(data['paragraphs']),100)
        self.assertTrue(data['truncated'])
        (self.root/'bad.docx').write_text('not a ZIP')
        self.assertEqual(self.cli('inspect',output='bad.docx').returncode,2)


if __name__=='__main__':
    unittest.main()
