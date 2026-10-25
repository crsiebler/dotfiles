"""Offline runtime selection contracts; no model calls or installed edits."""

import json
from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RuntimeSelectionTest(unittest.TestCase):
    def test_opencode_role_defaults_do_not_override_session_selection(self):
        config = json.loads((ROOT / 'ai/opencode/opencode.json').read_text())
        for role, settings in config.get('agents', {}).items():
            if role == 'title':
                continue
            with self.subTest(role=role):
                self.assertTrue({'model', 'variant', 'options'}.isdisjoint(settings))

    def test_session_model_defaults_remain_separate_from_roles(self):
        codex = tomllib.loads((ROOT / 'ai/codex/config.toml').read_text())
        self.assertEqual(codex['model'], 'gpt-6.1-sol')
        opencode = json.loads((ROOT / 'ai/opencode/opencode.json').read_text())
        self.assertEqual(opencode['model'], 'openai/gpt-6-astra')

    def test_title_model_is_only_an_explicit_utility_default(self):
        config = json.loads((ROOT / 'ai/opencode/opencode.json').read_text())
        self.assertEqual(config['agents']['title']['model'], 'openai/gpt-6-luna')
        self.assertNotEqual(config['agents']['title']['model'], config['model'])
        self.assertNotIn('subagents', config.get('agents', {}))


if __name__ == '__main__':
    unittest.main()
