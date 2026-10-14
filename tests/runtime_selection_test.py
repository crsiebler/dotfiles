"""Offline runtime selection contracts; no model calls or installed edits."""

import json
from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RuntimeSelectionTest(unittest.TestCase):
    def test_opencode_role_defaults_do_not_override_session_selection(self):
        for name in ('opencode.json', 'astra.json', 'sol.json'):
            config = json.loads((ROOT / 'ai/opencode' / name).read_text())
            for role, settings in config.get('agent', {}).items():
                with self.subTest(config=name, role=role):
                    self.assertTrue({'model', 'variant', 'options'}.isdisjoint(settings))

    def test_explicit_session_profiles_remain_separate_from_roles(self):
        codex = tomllib.loads((ROOT / 'ai/codex/config.toml').read_text())
        astra = tomllib.loads((ROOT / 'ai/codex/astra.config.toml').read_text())
        self.assertEqual(codex['model'], 'gpt-6.1-sol')
        self.assertEqual(astra['model'], 'gpt-6-astra')
        self.assertEqual(astra['model_reasoning_effort'], 'high')
        for name, expected in (('astra.json', 'openai/gpt-6-astra'),
                               ('sol.json', 'openai/gpt-6.1-sol')):
            config = json.loads((ROOT / 'ai/opencode' / name).read_text())
            self.assertEqual(config['model'], expected)

    def test_small_model_is_only_an_explicit_utility_default(self):
        config = json.loads((ROOT / 'ai/opencode/opencode.json').read_text())
        self.assertEqual(config['small_model'], 'openai/gpt-6-luna')
        self.assertNotEqual(config['small_model'], config['model'])
        self.assertNotIn('subagents', config.get('agent', {}))


if __name__ == '__main__':
    unittest.main()
