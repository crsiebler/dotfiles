"""Generation orchestration, independent of model frameworks and subprocesses."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Mapping, cast

from audio_domain import ArtifactPaths, ArtifactStore, AudioBackend, AudioRequest


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class AudioService:
    def __init__(self, backends: Mapping[str, AudioBackend], files: ArtifactStore,
                 now: Callable[[], str] = utc_now) -> None:
        self.backends = dict(backends)
        self.files = files
        self.now = now

    def _prepare(self, project: Path, request_path: Path) -> tuple[
            AudioBackend, AudioRequest, ArtifactPaths, dict[str, object]]:
        payload = self.files.read_request(project, request_path)
        model = payload.get('model')
        if not isinstance(model, str) or model not in self.backends:
            raise ValueError('unsupported audio model; available: ' + ', '.join(self.backends))
        backend = self.backends[model]
        request = backend.normalize(payload)
        paths = self.files.resolve(project, request, backend.protected_paths)
        batch = dict(backend.preview(request, paths), request=request.to_dict(),
                     output=str(paths.output), cache=str(paths.cache),
                     project_root=str(paths.project_root), model=request.model)
        return backend, request, paths, batch

    def plan(self, project: Path, request_path: Path) -> dict[str, object]:
        return self._prepare(project, request_path)[3]

    def generate(self, project: Path, request_path: Path) -> dict[str, object]:
        backend, request, paths, batch = self._prepare(project, request_path)
        self.files.ensure_available(paths)
        state = backend.status()
        if not state['ready']:
            raise ValueError('; '.join(cast(list[str], state['problems'])))
        initial = dict(batch, status='running', started_at=self.now())
        with self.files.reserve(paths) as artifacts:
            artifacts.record(initial)
            try:
                artifacts.reserve_output()
                backend.generate(request, paths)
                result = dict(initial, status='generated', completed_at=self.now(),
                              output_sha256=artifacts.fingerprint(),
                              approval='not asserted; follow project review requirements')
                artifacts.record(result)
                return result
            except BaseException:
                # Preserve model identity and settings without persisting an
                # exception message that could contain provider credentials.
                artifacts.record(dict(initial, status='failed', completed_at=self.now()))
                raise
