"""Filesystem adapter for project requests and generated artifact evidence."""

from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
from typing import Generator, Mapping, TextIO

from audio_domain import ArtifactPaths, AudioRequest


def sha256(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def overlap(left: Path, right: Path) -> bool:
    return left.is_relative_to(right) or right.is_relative_to(left)


def project_path(project: Path, value: str) -> Path:
    if not value or Path(value).is_absolute():
        raise ValueError('output and cache must be project-relative paths')
    path = (project / value).resolve()
    if not path.is_relative_to(project) or path == project:
        raise ValueError('path must remain inside the project')
    return path


class FileArtifacts:
    def __init__(self, output: Path, stream: TextIO) -> None:
        self.output = output
        self.stream = stream

    def reserve_output(self) -> None:
        with self.output.open('xb'):
            pass

    def fingerprint(self) -> str:
        if self.output.stat().st_size == 0:
            raise ValueError('model produced no audio')
        return sha256(self.output)

    def record(self, value: Mapping[str, object]) -> None:
        serialized = json.dumps(dict(value), indent=2) + '\n'
        self.stream.seek(0)
        self.stream.write(serialized)
        self.stream.truncate()
        self.stream.flush()


class ProjectFiles:
    def read_request(self, project: Path, request: Path) -> dict[str, object]:
        project = project.resolve(strict=True)
        path = (request if request.is_absolute() else project / request).resolve(strict=True)
        if not path.is_relative_to(project):
            raise ValueError('request must be inside the project')
        payload = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(payload, dict):
            raise ValueError('request must be a JSON object')
        return payload

    def resolve(self, project: Path, request: AudioRequest,
                protected_paths: tuple[Path, ...]) -> ArtifactPaths:
        project = project.resolve(strict=True)
        output = project_path(project, request.output)
        cache = project_path(project, request.cache)
        if overlap(output, cache):
            raise ValueError('raw output and mutable cache must be separate')
        for protected in protected_paths:
            if overlap(output, protected.resolve()) or overlap(cache, protected.resolve()):
                raise ValueError('output and cache must not overlap model infrastructure')
        return ArtifactPaths(project, output, cache)

    def ensure_available(self, paths: ArtifactPaths) -> None:
        evidence = paths.output.with_suffix(paths.output.suffix + '.provenance.json')
        if any(path.exists() or path.is_symlink() for path in (paths.output, evidence)):
            raise FileExistsError('output or provenance already exists; choose a new output name')

    @contextmanager
    def reserve(self, paths: ArtifactPaths) -> Generator[FileArtifacts, None, None]:
        self.ensure_available(paths)
        paths.output.parent.mkdir(parents=True, exist_ok=True)
        evidence = paths.output.with_suffix(paths.output.suffix + '.provenance.json')
        with evidence.open('x', encoding='utf-8') as stream:
            yield FileArtifacts(paths.output, stream)
