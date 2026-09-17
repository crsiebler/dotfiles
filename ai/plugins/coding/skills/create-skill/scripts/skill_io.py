"""Project-bounded I/O for portable skill tooling (Python 3.11+)."""
import json
from pathlib import Path

RESOURCE = Path(__file__).resolve().parents[1]
MAX_FILE = 2 * 1024 * 1024
MAX_TOTAL = 16 * 1024 * 1024


class SkillError(Exception):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def no_links(path):
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise SkillError(2, 'input: symlinks are not supported')


def project_path(root, value, *, output=False):
    raw = Path(value)
    raw = raw if raw.is_absolute() else root / raw
    no_links(raw)
    path = raw.resolve()
    if not path.is_relative_to(root):
        raise SkillError(2, 'input: path escapes project')
    if output:
        if path.is_relative_to(RESOURCE):
            raise SkillError(2, 'input: installed resources are read-only')
        if path.exists() or not path.parent.is_dir():
            raise SkillError(2, 'input: output exists or parent directory is missing')
    elif not path.exists():
        raise SkillError(2, 'input: path does not exist')
    return path


def tree_files(path):
    no_links(path)
    if not path.is_dir():
        raise SkillError(2, 'input: expected a directory')
    files, size = [], 0
    for count, item in enumerate(path.rglob('*'), 1):
        if count > 1000:
            raise SkillError(2, 'input: tree exceeds 1000 entries')
        no_links(item)
        if item.is_dir():
            continue
        if not item.is_file():
            raise SkillError(2, 'input: expected regular files')
        length = item.stat().st_size
        size += length
        if length > MAX_FILE or size > MAX_TOTAL:
            raise SkillError(2, 'input: file or tree size limit exceeded')
        files.append(item)
    return sorted(files)


def read_text(path):
    no_links(path)
    if not path.is_file() or path.stat().st_size > MAX_FILE:
        raise SkillError(2, 'input: expected a regular file of at most 2 MiB')
    try:
        return path.read_text(encoding='utf-8')
    except UnicodeError:
        raise SkillError(2, 'input: expected UTF-8 text') from None


def read_json(path):
    try:
        return json.loads(read_text(path))
    except (ValueError, RecursionError):
        raise SkillError(2, 'input: invalid JSON') from None


def publish(path, content):
    if len(content) > MAX_TOTAL:
        raise SkillError(4, 'generation: output exceeds 16 MiB')
    created = False
    try:
        with path.open('xb') as output:
            created = True
            output.write(content)
    except FileExistsError:
        raise SkillError(2, 'input: output already exists') from None
    except OSError:
        # Remove only the partial artifact created by this operation.
        if created:
            path.unlink(missing_ok=True)
        raise SkillError(4, 'generation: unable to write output') from None
