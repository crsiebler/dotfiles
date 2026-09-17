"""Cross-skill packaging and actual execution from isolated, unrelated directories."""
import ast
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

ROOT = Path(__file__).resolve().parents[1]
PYTHON = os.environ.get('SKILL_TEST_PYTHON', sys.executable)
YAML_PYTHON = os.environ.get('SKILL_TEST_YAML_PYTHON', PYTHON)
BUNDLES = {'create-skill':'coding', 'create-gif':'producing',
           **{f'create-{kind}':'producing' for kind in ('docx','pptx','xlsx','pdf')},
           **{f'read-{kind}':'researching' for kind in ('docx','pptx','xlsx','pdf')}}


def snapshot(root):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


class DocumentSkillsContractTest(unittest.TestCase):
    def test_unique_discovery_resource_closure_and_attribution(self):
        discovered = {}
        for path in (ROOT/'ai/plugins').glob('*/skills/*/SKILL.md'):
            discovered.setdefault(path.parent.name,[]).append(path)
        self.assertEqual({p.parent.name for p in (ROOT/'ai/plugins/producing/skills').glob('*/SKILL.md')},
                         {'create-audio','create-sprites','create-gif','create-docx','create-pptx','create-xlsx','create-pdf'})
        for name, plugin in BUNDLES.items():
            with self.subTest(skill=name):
                source = ROOT/f'ai/plugins/{plugin}/skills/{name}'
                self.assertEqual(discovered[name],[source/'SKILL.md'])
                content = (source/'SKILL.md').read_text()
                self.assertRegex(content, rf'(?m)^name: {name}$')
                self.assertRegex(content, r'(?m)^description: .+')
                for resource in ('scripts','references/requirements.md','references/validation.md','requirements.txt',
                                 'references/reading.md' if name.startswith('read-') else 'references/authoring.md'):
                    self.assertTrue((source/resource).exists(),resource)
                self.assertTrue((source/'requirements.txt').read_text().strip())
                for document in source.rglob('*.md'):
                    for link in re.findall(r'\]\(([^)]+)\)',document.read_text()):
                        if re.match(r'^[a-z]+://',link) or link.startswith('#'):
                            continue
                        target = (document.parent/link.split('#',1)[0]).resolve()
                        self.assertTrue(target.is_relative_to(source),f'{document}: escaping link {link}')
                        self.assertTrue(target.exists(),f'{document}: missing {link}')
                for script in (source/'scripts').glob('*.py'):
                    tree=ast.parse(script.read_text())
                    for node in ast.walk(tree):
                        if isinstance(node,ast.ImportFrom) and node.module:
                            module=node.module.split('.')[0]
                            if module.startswith(('create_','read_','docx_','pptx_','xlsx_','pdf_','gif_','skill_')):
                                self.assertTrue((script.parent/f'{module}.py').exists(),f'sibling import {module}')
                if name in ('create-skill','create-gif'):
                    self.assertIn('Apache License',(source/'LICENSE.txt').read_text())
                    provenance=(source/'references/provenance.md').read_text()
                    self.assertIn('34040c9c568585f6929bedeaad110ad08f079624',provenance)
                    self.assertIn('Modified',content)

    def test_all_ten_isolated_bundles_execute_and_preserve_resources(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'tests') as directory:
            root=Path(directory);installed=root/'installed';project=root/'project';cwd=root/'unrelated'
            installed.mkdir();project.mkdir();cwd.mkdir()
            for name,plugin in BUNDLES.items():
                shutil.copytree(ROOT/f'ai/plugins/{plugin}/skills/{name}',installed/name,
                                ignore=shutil.ignore_patterns('__pycache__'))
            before=snapshot(installed)
            def invoke(name,*args,flags=()):
                python=YAML_PYTHON if name=='create-skill' else PYTHON
                script=installed/name/'scripts'/f"{name.replace('-','_')}.py"
                result=subprocess.run([python,*flags,str(script),'--project',str(project),*args],
                                      cwd=cwd,capture_output=True,text=True)
                return result
            for name in BUNDLES:
                with self.subTest(skill=name):
                    result=invoke(name,'check')
                    self.assertEqual(result.returncode,0,result.stderr)
                    missing=invoke(name,'check',flags=('-S',))
                    self.assertEqual(missing.returncode,3,missing.stderr)
            code="""from pathlib import Path
import reportlab,shutil,sys
fonts=Path(reportlab.__file__).parent/'fonts'
for name in ('Vera.ttf','bitstream-vera-license.txt'):shutil.copyfile(fonts/name,Path(sys.argv[1])/name)
"""
            subprocess.run([PYTHON,'-c',code,str(project)],cwd=cwd,check=True,capture_output=True)
            requests={
                'docx':{'blocks':[{'type':'paragraph','text':'Portable evidence'}]},
                'pptx':{'width':10,'height':6,'slides':[{'layout':'Blank','shapes':[
                    {'kind':'text','x':1,'y':1,'width':8,'height':2,'text':'Portable evidence'}]}]},
                'xlsx':{'sheets':[{'name':'Data','rows':[[{'type':'string','value':'Portable evidence'}]]}]},
                'pdf':{'font':'Vera.ttf','blocks':[{'kind':'paragraph','text':'Portable evidence'}]},
                'gif':{'width':32,'height':32,'frame_count':4,'duration_ms':50,'radius':3}}
            for kind,request in requests.items():
                (project/f'{kind}.json').write_text(json.dumps(request))
            sample=project/'example';sample.mkdir()
            (sample/'SKILL.md').write_text('---\nname: example\ndescription: Example packaging evidence.\n---\n# Example\n')
            inputs=snapshot(project)
            for kind in requests:
                action='procedural' if kind=='gif' else 'create'
                result=invoke(f'create-{kind}',action,f'{kind}.json',f'output.{kind}')
                self.assertEqual(result.returncode,0,result.stderr)
                self.assertGreater((project/f'output.{kind}').stat().st_size,0)
                inspected=invoke(f'create-{kind}','inspect',f'output.{kind}')
                self.assertEqual(inspected.returncode,0,inspected.stderr)
                if kind!='gif':
                    evidence=invoke(f'read-{kind}','read',f'output.{kind}')
                    self.assertEqual(evidence.returncode,0,evidence.stderr)
                    self.assertIn('Portable evidence',evidence.stdout)
                    self.assertFalse(json.loads(evidence.stdout)['truncated'])
            package=invoke('create-skill','package','example','example.skill')
            self.assertEqual(package.returncode,0,package.stderr)
            with zipfile.ZipFile(project/'example.skill') as archive:
                self.assertEqual(archive.read('example/SKILL.md'),(sample/'SKILL.md').read_bytes())
            self.assertEqual(before,snapshot(installed))
            after=snapshot(project)
            self.assertTrue(all(after[name]==digest for name,digest in inputs.items()))


if __name__=='__main__':
    unittest.main()
