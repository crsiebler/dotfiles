"""Backend-independent workflow tests; no model runtime or network required."""

import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'ai/plugins/coding/skills/create-audio/scripts'))

from audio_domain import AudioRequest
from audio_files import ProjectFiles
from audio_service import AudioService


class ExampleBackend:
    protected_paths = ()

    def normalize(self, payload):
        return AudioRequest.from_dict(payload)

    def preview(self, request, paths):
        return {'backend': 'example', 'output_encoding': 'fixture bytes'}

    def status(self):
        return {'ready': True}

    def generate(self, request, paths):
        paths.output.write_bytes(b'backend output')


class AudioServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.request = {
            'model': 'example-hosted', 'prompt': 'Read the project narration',
            'negative_prompt': '', 'settings': {'voice': 'project-selected'},
            'output': 'assets/narration.audio', 'cache': '.cache/audio',
        }
        self.path = self.project / 'request.json'
        self.path.write_text(json.dumps(self.request))
        self.backend = ExampleBackend()
        self.service = AudioService({'example-hosted': self.backend}, ProjectFiles())

    def test_other_backend_needs_no_mlx_settings_or_model_directory(self):
        result = self.service.generate(self.project, self.path)
        self.assertEqual(result['request'], self.request)
        self.assertEqual(result['status'], 'generated')
        self.assertEqual((self.project / self.request['output']).read_bytes(), b'backend output')
        self.assertNotIn('command', result)

    def test_dry_run_does_not_check_or_invoke_backend(self):
        def unexpected(*args):
            self.fail('dry-run invoked a backend effect')
        self.backend.status = unexpected
        self.backend.generate = unexpected
        self.service.plan(self.project, self.path)
        self.assertEqual(list(self.project.iterdir()), [self.path])

    def test_unknown_model_does_not_fallback(self):
        service = AudioService({}, ProjectFiles())
        with self.assertRaisesRegex(ValueError, 'unsupported audio model'):
            service.generate(self.project, self.path)
        self.assertEqual(list(self.project.iterdir()), [self.path])

    def test_backend_failure_records_full_plan_without_error_secrets(self):
        def fail(*args):
            raise RuntimeError('private provider message')
        self.backend.generate = fail
        with self.assertRaises(RuntimeError):
            self.service.generate(self.project, self.path)
        evidence = self.project / (self.request['output'] + '.provenance.json')
        record = json.loads(evidence.read_text())
        self.assertEqual(record['backend'], 'example')
        self.assertEqual(record['status'], 'failed')
        self.assertIn('completed_at', record)
        self.assertNotIn('private provider message', evidence.read_text())

    def test_hashing_or_output_reservation_failure_leaves_valid_evidence(self):
        for operation in ('fingerprint', 'reserve_output'):
            with self.subTest(operation=operation):
                self.request['output'] = f'assets/{operation}.audio'
                self.path.write_text(json.dumps(self.request))
                with patch(f'audio_files.FileArtifacts.{operation}', side_effect=OSError('fixture failure')):
                    with self.assertRaises(OSError):
                        self.service.generate(self.project, self.path)
                evidence = self.project / (self.request['output'] + '.provenance.json')
                record = json.loads(evidence.read_text())
                self.assertEqual(record['status'], 'failed')
                self.assertEqual(record['backend'], 'example')
                self.assertIn('completed_at', record)


if __name__ == '__main__':
    unittest.main()
