"""Offline V2 source contracts; these do not claim native runtime validation.

Field projections checked against anomalyco/opencode dev on 2026-10-24:
packages/schema/src/config/{provider,model,agent,mcp}.ts and
https://opencode.ai/v2/cli.json. No network or installed configuration writes.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class OpenCodeV2Test(unittest.TestCase):
    def setUp(self):
        self.source = ROOT / 'ai/opencode'
        self.config = json.loads((self.source / 'opencode.json').read_text())

    def test_native_fields_and_ordered_rules(self):
        self.assertEqual(set(self.config), {'$schema', 'model', 'agents', 'commands',
                                           'permissions', 'providers', 'plugins', 'mcp'})
        self.assertIn('create-audio', self.config['commands'])
        self.assertEqual(set(self.config['mcp']), {'servers'})
        for rule in self.config['permissions']:
            self.assertEqual(set(rule), {'action', 'resource', 'effect'})
            self.assertIsInstance(rule['action'], str)
            self.assertIsInstance(rule['resource'], str)
            self.assertIn(rule['effect'], ('allow', 'ask', 'deny'))
            self.assertNotIn(rule['action'], ('bash', 'task', 'write', 'patch'))
        for server in self.config['mcp']['servers'].values():
            self.assertIs(type(server['disabled']), bool)
            self.assertNotIn('enabled', server)
            if 'timeout' in server:
                self.assertEqual(server['timeout'], {'catalog': 60000, 'execution': 60000})

    def test_bonsai_preserves_endpoint_limits_timeouts_and_reasoning_field(self):
        self.assertEqual(set(self.config['providers']), {'bonsai'})
        provider = self.config['providers']['bonsai']
        self.assertEqual(set(provider), {'name', 'package', 'settings', 'models'})
        self.assertEqual(provider['package'], 'aisdk:@ai-sdk/openai-compatible')
        self.assertEqual(provider['settings'], {
            'apiKey': 'none', 'baseURL': 'http://127.0.0.1:8081/v1',
            'chunkTimeout': 120000, 'headerTimeout': 600000, 'timeout': False})
        model = provider['models']['prism-ml/Ternary-Bonsai-2-27B-mlx-2bit']
        self.assertEqual(set(model), {'name', 'limit', 'capabilities', 'compatibility'})
        self.assertEqual(model['limit'], {'context': 65536, 'output': 8192})
        self.assertEqual(model['capabilities'], {'tools': True, 'input': ['text'], 'output': ['text']})
        self.assertEqual(model['compatibility'], {'reasoningField': 'reasoning_content'})

    def test_builtin_notifications_and_optional_image_provider(self):
        cli = json.loads((self.source / 'cli.json').read_text())
        self.assertEqual(cli['$schema'], 'https://opencode.ai/v2/cli.json')
        self.assertEqual(set(cli), {'$schema', 'theme', 'attention'})
        self.assertEqual(cli['theme'], {'name': 'opencode', 'mode': 'system'})
        self.assertEqual(cli['attention'], {'notifications': True, 'sound': True,
                                           'volume': 0.4, 'sound_pack': 'opencode.default'})
        self.assertEqual(self.config['plugins'], [])
        for retired in ('tui.json', 'opencode-notifier.json'):
            self.assertFalse((self.source / retired).exists())
        requirements = (ROOT / 'ai/plugins/producing/skills/create-sprites/references/requirements.md').read_text()
        self.assertIn('opencode-img@0.2.0', requirements)
        self.assertIn('API', requirements)


if __name__ == '__main__':
    unittest.main()
