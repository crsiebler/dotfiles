"""Exercise the installed skills CLI with only disposable project-local homes."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('skills'), 'skills CLI unavailable')
class NativeSkillsTest(unittest.TestCase):
    def test_scoped_removal_preserves_other_agent_copy_and_cleans_tracking(self):
        spec = importlib.util.spec_from_file_location('retirement', ROOT / 'scripts/ai_retirement.py')
        assert spec and spec.loader
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        cli = shutil.which('skills')
        assert cli
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            root = Path(directory)
            home = root / 'home'
            home.mkdir()
            env = {'HOME': str(home), 'XDG_CONFIG_HOME': str(home / '.config'),
                   'CODEX_HOME': str(home / '.codex'), 'TMPDIR': str(root),
                   'PATH': os.environ['PATH'], 'DISABLE_TELEMETRY': '1', 'DO_NOT_TRACK': '1'}

            def run(argv):
                result = subprocess.run([cli, *argv[1:]], cwd=root, env=env,
                                        capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stderr)
                return result.stdout

            if run(['skills', '--version']).strip() != '1.5.24':
                self.skipTest('native contract targets skills 1.5.24')
            source = root / 'source/old'
            source.mkdir(parents=True)
            (source / 'SKILL.md').write_text('---\nname: old\ndescription: Fixture\n---\nOriginal\n')
            for name in ('.git', '__pycache__', '__pypackages__'):
                (source / name).mkdir()
                (source / name / 'generated').write_text('excluded')
            (source / 'metadata.json').write_text('{"excluded":true}')
            run(['skills', 'add', str(source), '--global', '--agent', 'opencode', '--copy', '--yes'])
            shared = home / '.agents/skills'
            lock = home / '.agents/.skill-lock.json'
            lock.parent.mkdir(parents=True, exist_ok=True)
            lock.write_text(json.dumps({'version': 3, 'skills': {
                'old': {'source': str(source), 'sourceType': 'local'},
                'unrelated': {'source': 'example/other', 'sourceType': 'github'}
            }}))
            target = home / '.config/opencode'
            expected = m.skill_copy_fingerprint(source)
            self.assertEqual(expected, {'SKILL.md': m.fingerprint(source)['SKILL.md']})
            manager = m.Skills(root, target, shared, {'old': expected}, {})
            manager.prepare()
            manager.record(verify=True)
            # Keep an unrelated private Codex copy. Scoped OpenCode removal
            # must leave it byte-identical even when its name matches.
            other = home / '.codex/skills/old'
            other.mkdir(parents=True)
            (other / 'SKILL.md').write_text('private unrelated copy')
            manager = m.Skills(root, target, shared, {}, {})
            manager.prepare()
            manager.apply(run)
            manager.record()
            self.assertFalse((shared / 'old').exists())
            self.assertFalse((target / 'skills/old').exists())
            self.assertEqual((other / 'SKILL.md').read_text(), 'private unrelated copy')
            # Metadata may remain when another agent legitimately retains a copy.
            # A second fixture without that copy checks stale lock-only cleanup.
            shutil.rmtree(other)
            run(['skills', 'remove', 'old', '--global', '--agent', 'opencode', '--yes'])
            self.assertNotIn('old', json.loads(lock.read_text())['skills'])
            self.assertIn('unrelated', json.loads(lock.read_text())['skills'])


if __name__ == '__main__':
    unittest.main()
