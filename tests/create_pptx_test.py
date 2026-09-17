"""Artifact checks for the independent original PowerPoint creation helper."""
import hashlib
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
SCRIPT = ROOT / 'ai/plugins/producing/skills/create-pptx/scripts/create_pptx.py'
PYTHON = os.environ.get('SKILL_TEST_PYTHON', sys.executable)
NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart'}


class CreatePptxTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'tests')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run([PYTHON, '-c', "from PIL import Image; Image.new('RGB',(80,40),'blue').save('image.png')"],
                       cwd=self.root, check=True, capture_output=True)
        self.request = {'width': 10, 'height': 5.625, 'slides': [
            {'layout': 'Title Only', 'placeholders': [{'idx': 0, 'text': 'Résumé & results'}], 'shapes': [
                {'kind': 'text', 'x': .5, 'y': 1.4, 'width': 4, 'height': .6, 'text': 'Editable text', 'size': 24},
                {'kind': 'table', 'x': .5, 'y': 2.2, 'width': 4, 'height': 1, 'rows': [['Team', 'Count'], ['A', '12']]},
                {'kind': 'image', 'x': 6, 'y': 1.5, 'width': 3, 'height': 3, 'path': 'image.png'}]},
            {'layout': 'Blank', 'shapes': [
                {'kind': 'chart', 'x': 1, 'y': 1, 'width': 8, 'height': 4,
                 'categories': ['Q1', 'Q2'], 'series': [{'name': 'Units', 'values': [12, 18]}]}]}]}

    def cli(self, *args, script=SCRIPT, flags=()):
        return subprocess.run([PYTHON, *flags, str(script), '--project', str(self.root), *args],
                              cwd=self.root, capture_output=True, text=True)

    def create(self, request=None, name='deck.pptx'):
        (self.root / 'request.json').write_text(json.dumps(self.request if request is None else request))
        return self.cli('create', 'request.json', name)

    def test_artifact_xml_content_geometry_images_and_native_chart(self):
        image_hash = hashlib.sha256((self.root / 'image.png').read_bytes()).hexdigest()
        result = self.create()
        self.assertEqual(result.returncode, 0, result.stderr)
        with zipfile.ZipFile(self.root / 'deck.pptx') as archive:
            presentation = ET.fromstring(archive.read('ppt/presentation.xml'))
            self.assertEqual(len(presentation.findall('p:sldIdLst/p:sldId', NS)), 2)
            self.assertEqual(presentation.find('p:sldSz', NS).get('cx'), '9144000')
            slide = ET.fromstring(archive.read('ppt/slides/slide1.xml'))
            texts = [node.text for node in slide.findall('.//a:t', NS)]
            for value in ('Résumé & results', 'Editable text', 'Team', 'Count', 'A', '12'):
                self.assertIn(value, texts)
            picture = slide.find('.//p:pic/p:spPr/a:xfrm/a:ext', NS)
            self.assertEqual(int(picture.get('cx')), 2743200)
            self.assertEqual(int(picture.get('cy')), 1371600)
            self.assertIn('ppt/embeddings/Microsoft_Excel_Sheet1.xlsx', archive.namelist())
            chart = ET.fromstring(archive.read('ppt/charts/chart1.xml'))
            self.assertEqual([n.text for n in chart.findall('.//c:val/c:numRef/c:numCache/c:pt/c:v', NS)], ['12', '18'])
            self.assertEqual([n.text for n in chart.findall('.//c:cat/c:strRef/c:strCache/c:pt/c:v', NS)], ['Q1', 'Q2'])
        self.assertEqual(image_hash, hashlib.sha256((self.root / 'image.png').read_bytes()).hexdigest())
        report = self.cli('inspect', 'deck.pptx')
        self.assertEqual(report.returncode, 0, report.stderr)
        data = json.loads(report.stdout)
        self.assertEqual(data['slide_count'], 2)
        self.assertFalse(data['truncated'])

    def test_layout_inventory_and_rejected_inputs_preserve_files(self):
        result = self.cli('layouts')
        self.assertEqual(result.returncode, 0, result.stderr)
        layouts = json.loads(result.stdout)['layouts']
        title = next(layout for layout in layouts if layout['name'] == 'Title Only')
        self.assertTrue(any(p['idx'] == 0 for p in title['placeholders']))
        for mutate in (lambda r: r.update(width=-1),
                       lambda r: r['slides'][0].update(layout='missing'),
                       lambda r: r['slides'][0]['shapes'][0].update(x=9),
                       lambda r: r['slides'][0]['placeholders'][0].update(idx=999),
                       lambda r: r['slides'][1]['shapes'][0]['series'][0].update(values=[1]),
                       lambda r: r['slides'][0]['shapes'][1].update(rows=[['a'], ['b','c']])):
            request = json.loads(json.dumps(self.request)); mutate(request)
            self.assertEqual(self.create(request).returncode, 2)
            self.assertFalse((self.root / 'deck.pptx').exists())
        self.assertEqual(self.create().returncode, 0)
        before = (self.root / 'deck.pptx').read_bytes()
        self.assertEqual(self.create().returncode, 2)
        self.assertEqual(before, (self.root / 'deck.pptx').read_bytes())
        self.assertEqual(self.create(name='../escape.pptx').returncode, 2)
        (self.root / 'link.png').symlink_to(self.root / 'image.png')
        self.request['slides'][0]['shapes'][2]['path'] = 'link.png'
        self.assertEqual(self.create(name='fresh.pptx').returncode, 2)
        self.assertFalse((self.root / 'fresh.pptx').exists())

    def test_oversized_content_invalid_image_and_source_preservation(self):
        self.request['slides'][0]['shapes'][2]['path'] = 'bad.png'
        (self.root / 'bad.png').write_text('PRIVATE INVALID IMAGE')
        result = self.create()
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('PRIVATE', result.stderr)
        self.assertFalse((self.root / 'deck.pptx').exists())
        self.request = {'width': 10, 'height': 6, 'slides': [{'layout': 'Blank', 'shapes': [
            {'kind': 'text', 'x': 0, 'y': 0, 'width': 5, 'height': 1, 'text': 'a' * 19000}
            for _ in range(3)]}]}
        result = self.create()
        self.assertEqual(result.returncode, 2)
        self.assertIn('budget', result.stderr)
        self.assertFalse((self.root / 'deck.pptx').exists())
        source = self.root / 'request.json'
        before = source.read_bytes()
        self.assertEqual(self.cli('create', 'request.json', 'deck.pptx').returncode, 2)
        self.assertEqual(source.read_bytes(), before)

    def test_missing_dependency_isolation_and_documented_recipe(self):
        self.assertEqual(self.cli('check', flags=('-S',)).returncode, 3)
        self.assertEqual(self.cli('check').returncode, 0)
        installed = self.root / 'installed' / 'create-pptx'
        shutil.copytree(SCRIPT.parents[1], installed, ignore=shutil.ignore_patterns('__pycache__'))
        before = {p.relative_to(installed): p.read_bytes() for p in installed.rglob('*') if p.is_file()}
        recipe = re.search(r'```json\n(.*?)\n```', (installed / 'references/authoring.md').read_text(), re.S).group(1)
        (self.root / 'recipe.json').write_text(recipe)
        result = self.cli('create', 'recipe.json', 'recipe.pptx', script=installed / 'scripts/create_pptx.py')
        self.assertEqual(result.returncode, 0, result.stderr)
        after = {p.relative_to(installed): p.read_bytes() for p in installed.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        result = self.cli('create', 'recipe.json', 'installed/create-pptx/no.pptx', script=installed / 'scripts/create_pptx.py')
        self.assertEqual(result.returncode, 2)


if __name__ == '__main__':
    unittest.main()
