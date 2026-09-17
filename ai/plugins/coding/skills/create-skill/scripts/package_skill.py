"""Adapted from Anthropic skill-creator, Apache-2.0; see ../LICENSE.txt.
Modified 2026-09-17: in-memory packaging, bounded input, no overwrite, reopened
archive inspection, and project-owned publication through create_skill.py.
"""
import fnmatch
import io
import zipfile
from skill_io import SkillError, tree_files
from quick_validate import validate_skill

EXCLUDE_DIRS = {'__pycache__', 'node_modules'}
EXCLUDE_GLOBS = {'*.pyc'}
EXCLUDE_FILES = {'.DS_Store'}
ROOT_EXCLUDE_DIRS = {'evals'}


def should_exclude(rel_path):
    parts = rel_path.parts
    return (any(part in EXCLUDE_DIRS for part in parts)
            or len(parts) > 1 and parts[1] in ROOT_EXCLUDE_DIRS
            or rel_path.name in EXCLUDE_FILES
            or any(fnmatch.fnmatch(rel_path.name, pattern) for pattern in EXCLUDE_GLOBS))


def package_skill(path):
    validate_skill(path)
    buffer = io.BytesIO()
    expected = {}
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
        for file in tree_files(path):
            relative = file.relative_to(path.parent)
            if should_exclude(relative):
                continue
            content = file.read_bytes()
            expected[relative.as_posix()] = content
            archive.writestr(relative.as_posix(), content)
    with zipfile.ZipFile(buffer) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != set(expected):
            raise SkillError(5, 'validation: package inventory mismatch')
        if any(archive.read(name) != value for name, value in expected.items()):
            raise SkillError(5, 'validation: package content mismatch')
    return buffer.getvalue()
