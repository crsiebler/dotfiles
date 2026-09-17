"""Bounded read-only project input for the independent PDF reader."""
from pathlib import Path


class ReadError(Exception):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def no_links(path):
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ReadError(2, 'input: symlinks are unsupported')


def load_source(root, value):
    raw = Path(value)
    raw = raw if raw.is_absolute() else root/raw
    no_links(raw)
    source = raw.resolve()
    if not source.is_relative_to(root) or not source.is_file() or source.stat().st_size > 16*1024*1024:
        raise ReadError(2, 'input: expected project PDF of at most 16 MiB')
    content = source.read_bytes()
    if not content.startswith(b'%PDF-'):
        raise ReadError(2, 'input: expected PDF header')
    return source, content
