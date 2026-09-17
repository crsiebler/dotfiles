"""Adapted from Anthropic skill-creator, Apache-2.0; see ../LICENSE.txt.
Modified 2026-09-17: bounded reads, lazy dependency check, directory/name agreement,
nonempty values, sanitized errors, and reusable validation without implicit CLI I/O.
"""
import re
from skill_io import SkillError, read_text, tree_files


def require_yaml():
    try:
        import yaml
    except ImportError:
        raise SkillError(3, 'dependency: PyYAML is required; see references/requirements.md') from None
    return yaml


def validate_skill(path):
    yaml = require_yaml()
    tree_files(path)
    content = read_text(path / 'SKILL.md')
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', content, re.DOTALL)
    if not match:
        raise SkillError(5, 'validation: missing YAML frontmatter')
    try:
        header = yaml.safe_load(match[1])
    except yaml.YAMLError:
        raise SkillError(5, 'validation: invalid YAML frontmatter') from None
    if not isinstance(header, dict):
        raise SkillError(5, 'validation: frontmatter must be a mapping')
    allowed = {'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility'}
    if set(header) - allowed:
        raise SkillError(5, 'validation: unsupported frontmatter keys')
    name = header.get('name')
    if (not isinstance(name, str) or len(name) > 64
            or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name)
            or name != path.name):
        raise SkillError(5, 'validation: name must match the action-oriented directory name')
    description = header.get('description')
    if (not isinstance(description, str) or not description.strip()
            or len(description) > 1024 or '<' in description or '>' in description):
        raise SkillError(5, 'validation: description must be nonempty text, at most 1024 characters')
    compatibility = header.get('compatibility', '')
    if not isinstance(compatibility, str) or len(compatibility) > 500:
        raise SkillError(5, 'validation: invalid compatibility text')
    return header
