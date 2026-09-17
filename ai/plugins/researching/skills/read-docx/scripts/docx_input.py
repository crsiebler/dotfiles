"""Read-only, bounded project input for the independent DOCX reader."""
import io
from pathlib import Path
import zipfile


class ReadError(Exception):
    def __init__(self, code, message):
        self.code=code
        super().__init__(message)


def no_links(path):
    if any(p.is_symlink() for p in (path,*path.parents)):
        raise ReadError(2,'input: symlinks are unsupported')


def load_source(root,value):
    raw=Path(value)
    raw=raw if raw.is_absolute() else root/raw
    no_links(raw)
    source=raw.resolve()
    if not source.is_relative_to(root) or not source.is_file():
        raise ReadError(2,'input: source must be a project-local file')
    if source.stat().st_size > 16*1024*1024:
        raise ReadError(2,'input: DOCX exceeds 16 MiB')
    content=source.read_bytes()
    try:
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            members=archive.infolist()
            if len(members)>1000 or sum(m.file_size for m in members)>64*1024*1024:
                raise ReadError(2,'input: expanded DOCX limits exceeded')
            if len({m.filename for m in members})!=len(members):
                raise ReadError(2,'input: duplicate ZIP members')
            if any(m.flag_bits & 1 for m in members) or archive.testzip() is not None:
                raise ReadError(2,'input: encrypted or invalid ZIP package')
            if 'word/document.xml' not in archive.namelist():
                raise ReadError(2,'input: expected DOCX package')
    except zipfile.BadZipFile:
        raise ReadError(2,'input: invalid DOCX ZIP package') from None
    return source,content
