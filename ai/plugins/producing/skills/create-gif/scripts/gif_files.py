"""Project-owned GIF input and publication boundaries."""
from pathlib import Path

RESOURCE = Path(__file__).resolve().parents[1]


class GifError(Exception):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def no_links(path):
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise GifError(2, 'input: symlinks are not supported')


def project_path(root, value, *, output=False):
    if not isinstance(value, str):
        raise GifError(2, 'input: path must be text')
    raw = Path(value)
    raw = raw if raw.is_absolute() else root / raw
    no_links(raw)
    path = raw.resolve()
    if not path.is_relative_to(root):
        raise GifError(2, 'input: path escapes project')
    if output:
        if path.is_relative_to(RESOURCE) or path.exists() or not path.parent.is_dir():
            raise GifError(2, 'input: output must be fresh, project-owned, with existing parent')
    elif not path.is_file() or path.stat().st_size > 10 * 1024 * 1024:
        raise GifError(2, 'input: expected a regular file of at most 10 MiB')
    return path


def publish(path, content):
    created = False
    try:
        with path.open('xb') as stream:
            created = True
            stream.write(content)
    except FileExistsError:
        raise GifError(2, 'input: output already exists') from None
    except OSError:
        if created:
            path.unlink(missing_ok=True)
        raise GifError(4, 'generation: cannot publish GIF') from None
