import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'ai/plugins/coding/skills/create-audio/scripts'
sys.path.insert(0, str(SCRIPTS))

from audio_files import ProjectFiles, sha256
from audio_service import AudioService
from stable_audio_mlx import FLOAT_WAV_LAUNCHER, StableAudioBackend


class AudioGenerationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        spec = importlib.util.spec_from_file_location('create_audio', SCRIPTS / 'create_audio.py')
        self.audio = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.audio)
        self.backend = StableAudioBackend(self.project / 'models')
        self.service = AudioService({'stable-audio-3-small-sfx': self.backend}, ProjectFiles())
        self.request = {
            'model': 'stable-audio-3-small-sfx',
            'prompt': 'A latch opening',
            'negative_prompt': 'speech',
            'seconds': 2.5,
            'steps': 4,
            'seed': 19,
            'cfg': 2.0,
            'apg': 0.5,
            'output': 'assets/audio/latch.wav',
            'cache': '.cache/audio',
        }

    def write_request(self):
        path = self.project / 'audio.json'
        path.write_text(json.dumps(self.request))
        return path

    def test_project_supplies_settings_and_paths(self):
        plan = self.service.plan(self.project, self.write_request())
        self.assertEqual(plan['output'], str(self.project / self.request['output']))
        for flag, value in [('--steps', '4'), ('--seed', '19'), ('--cfg', '2.0'), ('--apg', '0.5')]:
            self.assertEqual(plan['command'][plan['command'].index(flag) + 1], value)
        self.assertNotIn('new-zion', json.dumps(plan))

    def test_missing_and_unknown_settings_are_not_silently_defaulted(self):
        for key in ('prompt', 'steps', 'cache'):
            with self.subTest(key=key):
                original = self.request.pop(key)
                with self.assertRaises(ValueError):
                    self.service.plan(self.project, self.write_request())
                self.request[key] = original
        self.request['stepz'] = 8
        with self.assertRaises(ValueError):
            self.service.plan(self.project, self.write_request())

    def test_rejects_escape_and_symlink_output(self):
        for value in ('../escape.wav', '/outside.wav'):
            self.request['output'] = value
            with self.assertRaises(ValueError):
                self.service.plan(self.project, self.write_request())
        (self.project / 'escape').symlink_to(self.project.parent, target_is_directory=True)
        self.request['output'] = 'escape/file.wav'
        with self.assertRaises(ValueError):
            self.service.plan(self.project, self.write_request())

    def test_rejects_invalid_numeric_settings(self):
        for key, value in [('seconds', float('nan')), ('steps', True), ('seed', -1),
                           ('apg', 2), ('steps', 10 ** 400), ('cfg', 10 ** 400)]:
            with self.subTest(key=key):
                old = self.request[key]
                self.request[key] = value
                with self.assertRaises(ValueError):
                    self.service.plan(self.project, self.write_request())
                self.request[key] = old

    def test_generation_is_offline_with_project_caches_and_provenance(self):
        request = self.write_request()
        def run(command, **kwargs):
            env = kwargs['env']
            self.assertEqual(env['HF_HUB_OFFLINE'], '1')
            self.assertEqual(env['TRANSFORMERS_OFFLINE'], '1')
            for key in ('HF_HOME', 'XDG_CACHE_HOME', 'TMPDIR', 'UV_CACHE_DIR'):
                self.assertTrue(Path(env[key]).is_relative_to(self.project / '.cache/audio'))
            Path(command[command.index('--out') + 1]).write_bytes(b'generated-wave-fixture')
        with patch.object(self.backend, 'inspect', return_value={'ready': True}), \
                patch.object(self.backend, 'run', side_effect=run):
            result = self.service.generate(self.project, request)
        self.assertEqual(result['request'], self.request)
        output = self.project / self.request['output']
        self.assertTrue(output.with_suffix('.wav.provenance.json').is_file())
        self.assertEqual(result['output_sha256'], sha256(output))

    def test_existing_source_or_provenance_is_preserved(self):
        output = self.project / self.request['output']
        output.parent.mkdir(parents=True)
        evidence = output.with_suffix('.wav.provenance.json')
        evidence.write_text('original evidence')
        with patch.object(self.backend, 'inspect', return_value={'ready': True}), \
                patch.object(self.backend, 'run') as run:
            with self.assertRaises((ValueError, FileExistsError)):
                self.service.generate(self.project, self.write_request())
            run.assert_not_called()
        self.assertEqual(evidence.read_text(), 'original evidence')

    def test_dry_run_requires_no_model_installation_and_writes_nothing(self):
        request = self.write_request()
        result = subprocess.run([
            sys.executable, str(SCRIPTS / 'create_audio.py'), 'generate',
            '--project-root', str(self.project), '--request', str(request),
            '--models-root', str(self.project / 'missing-models'), '--dry-run',
        ], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(self.project.iterdir()), [request])
        self.assertEqual(json.loads(result.stdout)['request'], self.request)

    def test_setup_preserves_existing_installation(self):
        import stable_audio_runtime as audio_runtime
        existing = self.project / 'models'
        existing.mkdir()
        marker = existing / 'keep'
        marker.write_text('existing runtime')
        with patch.object(audio_runtime.shutil, 'which', return_value='/fixture/tool'), \
                patch.object(audio_runtime.platform, 'system', return_value='Darwin'), \
                patch.object(audio_runtime.platform, 'machine', return_value='arm64'), \
                patch.object(audio_runtime.subprocess, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'new models root'):
                audio_runtime.setup(existing, accept_model_terms=True)
            run.assert_not_called()
        self.assertEqual(marker.read_text(), 'existing runtime')

    def test_setup_requires_model_terms_before_mutation(self):
        import stable_audio_runtime as audio_runtime
        destination = self.project / 'models'
        with self.assertRaisesRegex(ValueError, 'accept-model-terms'):
            audio_runtime.setup(destination)
        self.assertFalse(destination.exists())

    def test_setup_reuses_verified_weights_without_downloading_them(self):
        import stable_audio_runtime as audio_runtime
        weights = self.project / 'weights'
        weights.mkdir()
        (weights / 'fixture.npz').write_bytes(b'weights')
        destination = self.project / 'models'
        expected = sha256(weights / 'fixture.npz')
        with patch.object(audio_runtime, 'WEIGHTS', {'fixture.npz': expected}), \
                patch.object(audio_runtime.shutil, 'which', return_value='/fixture/tool'), \
                patch.object(audio_runtime.platform, 'system', return_value='Darwin'), \
                patch.object(audio_runtime.platform, 'machine', return_value='arm64'), \
                patch.object(audio_runtime.subprocess, 'run') as run, \
                patch.object(audio_runtime, 'check_runtime', return_value={'ready': True}):
            audio_runtime.setup(destination, weights, accept_model_terms=True)
        link = audio_runtime.runtime_path(destination) / 'models/mlx/fixture.npz'
        self.assertEqual(link.read_bytes(), b'weights')
        self.assertNotEqual(link.resolve(), weights / 'fixture.npz')
        self.assertEqual((weights / 'fixture.npz').read_bytes(), b'weights')
        self.assertFalse(any('download' in call.args[0] for call in run.call_args_list))

    def test_failed_model_retains_failure_evidence_and_rejects_retry(self):
        request = self.write_request()
        with patch.object(self.backend, 'inspect', return_value={'ready': True}), \
                patch.object(self.backend, 'run', side_effect=subprocess.CalledProcessError(1, 'model')):
            with self.assertRaises(subprocess.CalledProcessError):
                self.service.generate(self.project, request)
        output = self.project / self.request['output']
        evidence = json.loads(output.with_suffix('.wav.provenance.json').read_text())
        self.assertEqual(evidence['status'], 'failed')
        with self.assertRaises(FileExistsError):
            self.service.generate(self.project, request)

    def test_cache_children_cannot_redirect_writes_outside_the_project(self):
        cache = self.project / self.request['cache']
        cache.mkdir(parents=True)
        (cache / 'huggingface').symlink_to(self.project.parent, target_is_directory=True)
        with patch.object(self.backend, 'inspect', return_value={'ready': True}), \
                patch.object(self.backend, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'cache'):
                self.service.generate(self.project, self.write_request())
            run.assert_not_called()

    def test_cache_cannot_contain_the_models_root(self):
        backend = StableAudioBackend(self.project / '.cache/audio/huggingface')
        service = AudioService({'stable-audio-3-small-sfx': backend}, ProjectFiles())
        with self.assertRaisesRegex(ValueError, 'overlap model infrastructure'):
            service.plan(self.project, self.write_request())

    def test_float_launcher_preserves_amplitude_and_rejects_nonfinite_samples(self):
        from unittest.mock import Mock
        writer = Mock()
        finite = SimpleNamespace(all=lambda: True)
        model = SimpleNamespace(
            SAMPLE_RATE=44100, np=SimpleNamespace(isfinite=lambda value: finite),
            main=lambda: None,
        )
        with patch.dict(sys.modules, {'soundfile': SimpleNamespace(write=writer),
                                      'sa3_mlx': model}), patch.object(sys, 'path', list(sys.path)):
            exec(FLOAT_WAV_LAUNCHER, {})
            samples = SimpleNamespace(T='transposed samples')
            model.save_wav('output.wav', samples)
            writer.assert_called_once_with('output.wav', 'transposed samples', 44100,
                                           subtype='FLOAT', format='WAV')
            finite.all = lambda: False
            with self.assertRaisesRegex(RuntimeError, 'non-finite'):
                model.save_wav('output.wav', samples)
            self.assertEqual(writer.call_count, 1)


if __name__ == '__main__':
    unittest.main()
