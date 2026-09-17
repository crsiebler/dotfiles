"""Bounded file and value handling for this independently packaged PDF helper."""
import math
from pathlib import Path

RESOURCE = Path(__file__).resolve().parents[1]
MAX_FILE = 16 * 1024 * 1024


class DocumentError(Exception):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def no_links(path):
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise DocumentError(2, 'input: symlinks are unsupported')


def project_path(root, value, *, output=False):
    if not isinstance(value, str):
        raise DocumentError(2, 'input: path must be text')
    raw = Path(value)
    raw = raw if raw.is_absolute() else root / raw
    no_links(raw)
    path = raw.resolve()
    if not path.is_relative_to(root):
        raise DocumentError(2, 'input: path escapes project')
    if output:
        if path.is_relative_to(RESOURCE) or path.exists() or not path.parent.is_dir():
            raise DocumentError(2, 'input: output must be fresh with an existing project parent')
    elif not path.is_file() or path.stat().st_size > MAX_FILE:
        raise DocumentError(2, 'input: expected a regular file of at most 16 MiB')
    return path


def fields(value, allowed):
    if not isinstance(value, dict) or set(value) - set(allowed):
        raise DocumentError(2, 'input: unexpected object fields')


def text(value, limit=20000):
    if (not isinstance(value, str) or len(value) > limit
            or any(ord(c) < 32 and c not in '\n\r\t' for c in value)):
        raise DocumentError(2, 'input: invalid or oversized text')
    return value


def number(value, low, high):
    if type(value) not in (int, float) or not math.isfinite(value) or not low <= value <= high:
        raise DocumentError(2, 'input: invalid numeric range')
    return value


def publish(path, content):
    created = False
    try:
        with path.open('xb') as stream:
            created = True
            stream.write(content)
    except FileExistsError:
        raise DocumentError(2, 'input: output already exists') from None
    except OSError:
        if created:
            path.unlink(missing_ok=True)
        raise DocumentError(4, 'generation: cannot publish document') from None
