# Requirements

- Python 3.11+; standard library handles aggregation and Markdown reports.
- PyYAML is required for frontmatter validation and packaging. Tested with PyYAML 6.0.3 under Python 3.11 in the authorized project-local
  test environment; requirements.txt pins that verified version. `check` reports absence without installing anything.
- No optional Python packages, fonts, native renderers, or browser server are needed
  for the portable operations. Reports are Markdown, not an adapted HTML viewer.
- Actual model evaluations need an available authorized harness; delegation and
  token metrics are optional. [Claude adapters](claude-adapters.md) are separate.

Run `python /loaded/create-skill/scripts/create_skill.py check` first. Missing
packages return exit 3. Installation is a separate user-authorized operation in a
project environment, never part of the helper or AI configuration installer.

PyYAML safe_load/YAMLError usage was checked with Context7 against
[official PyYAML documentation](https://github.com/yaml/pyyaml/blob/main/_autodocs/api-reference/top-level-functions.md).
Safe loading restricts constructed YAML types; input limits still apply.

Repository tests may select an existing PyYAML interpreter with
`SKILL_TEST_YAML_PYTHON`; it falls back to `SKILL_TEST_PYTHON` and then the test
driver. This test-only selection neither installs packages nor changes helper paths.
