"""Artifact-level GIF timing, palette, disposal, and path regression tests."""
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'ai/plugins/producing/skills/create-gif/scripts/create_gif.py'
PYTHON = os.environ.get('SKILL_TEST_PYTHON', sys.executable)


class GifTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'tests')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        # Fixture construction runs under the same explicitly selected dependency runtime.
        code = '''from PIL import Image, ImageDraw
for name, color in [('a','red'),('b','blue')]:
    Image.new('RGB',(16,8),color).save(name+'.png')
for index in range(2):
    im=Image.new('RGBA',(16,16),(0,0,0,0))
    ImageDraw.Draw(im).rectangle((index*8,0,index*8+3,3),fill='red')
    im.save('alpha'+str(index)+'.png')
'''
        result = subprocess.run([PYTHON, '-c', code], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def cli(self, action, spec=None, output='result.gif', flags=()):
        args = [PYTHON, *flags, str(SCRIPT), '--project', str(self.root), action]
        if spec is not None:
            (self.root / 'request.json').write_text(json.dumps(spec))
            args += ['request.json', output]
        elif action == 'inspect':
            args += [output]
        return subprocess.run(args, cwd=self.root, capture_output=True, text=True)

    def spec(self, **changes):
        return dict(frames=['a.png', 'a.png', 'b.png'], durations_ms=[35, 75, 120],
                    width=16, height=16, **changes)

    def test_duplicate_and_reduction_preserve_encoded_elapsed_time(self):
        for stride in (1, 2, 3):
            with self.subTest(stride=stride):
                result = self.cli('assemble', self.spec(reduce_every=stride), f'{stride}.gif')
                self.assertEqual(result.returncode, 0, result.stderr)
                data = json.loads(result.stdout)
                self.assertEqual(data['duration_ms'], 240)
                self.assertEqual(data['requested_duration_ms'], 230)
                inspection = self.cli('inspect', output=f'{stride}.gif')
                decoded = json.loads(inspection.stdout)
                self.assertEqual(sum(decoded['durations_ms']), 240)
                self.assertEqual(decoded['format'], 'GIF')
                self.assertEqual(decoded['size_bytes'], (self.root / f'{stride}.gif').stat().st_size)
                self.assertEqual(decoded['frame_count'], 1 if stride == 3 else 2)

    def test_aspect_ratio_nearest_and_solid_background(self):
        result = self.cli('assemble', self.spec(background='#00ff00', loop=None))
        self.assertEqual(result.returncode, 0, result.stderr)
        code = '''from PIL import Image
im=Image.open('result.gif').convert('RGB')
assert im.getpixel((0,0)) == (0,255,0)
assert im.getpixel((8,8)) == (255,0,0)
assert set(im.getdata()) == {(0,255,0),(255,0,0)}
'''
        check = subprocess.run([PYTHON, '-c', code], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertIsNone(json.loads(result.stdout)['loop'])

    def test_nearest_resizes_pixel_blocks_without_interpolated_edges(self):
        code = """from PIL import Image
im=Image.new('RGB',(2,2))
im.putdata([(255,0,0),(0,0,255),(0,0,255),(255,0,0)])
im.save('pixels.png')
"""
        subprocess.run([PYTHON, '-c', code], cwd=self.root, check=True)
        result = self.cli('assemble', dict(frames=['pixels.png'], durations_ms=[100],
                                          width=8,height=8,colors=256,sampling='nearest'))
        self.assertEqual(result.returncode, 0, result.stderr)
        code = """from PIL import Image
im=Image.open('result.gif').convert('RGB')
for y in range(8):
    for x in range(8):
        expected=(255,0,0) if (x//4)==(y//4) else (0,0,255)
        assert im.getpixel((x,y)) == expected, (x,y,im.getpixel((x,y)))
"""
        result = subprocess.run([PYTHON,'-c',code],cwd=self.root,capture_output=True,text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_transparent_disposal_clears_previous_artwork(self):
        spec = dict(frames=['alpha0.png','alpha1.png'], durations_ms=[100,200],
                    width=16,height=16,background='transparent',loop=2)
        result = self.cli('assemble', spec)
        self.assertEqual(result.returncode, 0, result.stderr)
        code = '''from PIL import Image
im=Image.open('result.gif')
assert im.info['loop'] == 2
im.seek(1)
rgba=im.convert('RGBA')
assert rgba.getpixel((0,0))[3] == 0
assert rgba.getpixel((8,0)) == (255,0,0,255)
assert im.disposal_method == 2
'''
        check = subprocess.run([PYTHON, '-c', code], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(check.returncode, 0, check.stderr)

    def test_collision_limits_invalid_input_and_missing_dependency(self):
        self.assertEqual(self.cli('assemble', self.spec()).returncode, 0)
        before = (self.root / 'result.gif').read_bytes()
        self.assertEqual(self.cli('assemble', self.spec()).returncode, 2)
        self.assertEqual(before, (self.root / 'result.gif').read_bytes())
        for changes in ({'max_bytes':1}, {'durations_ms':[100]}, {'width':0},
                        {'frames':['../escape.png']}, {'unknown':True}):
            spec = self.spec(); spec.update(changes)
            self.assertNotEqual(self.cli('assemble', spec, 'bad.gif').returncode, 0)
            self.assertFalse((self.root / 'bad.gif').exists())
        (self.root / 'link.png').symlink_to(self.root / 'a.png')
        spec=self.spec(); spec['frames'][0]='link.png'
        self.assertEqual(self.cli('assemble', spec, 'bad.gif').returncode, 2)
        self.assertEqual(self.cli('check', flags=('-S',)).returncode, 3)

    def test_isolated_bundle_preserves_sources_and_resources(self):
        installed = self.root / 'installed' / 'create-gif'
        shutil.copytree(SCRIPT.parents[1], installed,
                        ignore=shutil.ignore_patterns('__pycache__'))
        before = {p.relative_to(self.root): p.read_bytes()
                  for p in self.root.rglob('*') if p.is_file()}
        (self.root / 'request.json').write_text(json.dumps(self.spec()))
        result = subprocess.run([PYTHON, str(installed / 'scripts/create_gif.py'),
                                 '--project', str(self.root), 'assemble', 'request.json',
                                 'isolated.gif'], cwd=installed.parent,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        for name, content in before.items():
            self.assertEqual((self.root / name).read_bytes(), content)
        self.assertFalse(list(installed.rglob('__pycache__')))
        result = subprocess.run([PYTHON, str(installed / 'scripts/create_gif.py'),
                                 '--project', str(self.root), 'assemble', 'request.json',
                                 str(installed / 'forbidden.gif')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertFalse((installed / 'forbidden.gif').exists())

    def test_procedural_and_variable_duration_inspection(self):
        result = self.cli('procedural', dict(frame_count=8,duration_ms=80,width=32,height=32,radius=3))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['duration_ms'], 640)
        code = '''from PIL import Image
images=[Image.new('RGB',(4,4),c) for c in ['red','blue','green']]
images[0].save('external.gif',save_all=True,append_images=images[1:],duration=[20,70,130],loop=3)
'''
        subprocess.run([PYTHON,'-c',code],cwd=self.root,check=True)
        result=self.cli('inspect',output='external.gif')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['durations_ms'],[20,70,130])
        self.assertEqual(json.loads(result.stdout)['duration_ms'],220)


if __name__ == '__main__':
    unittest.main()
