"""Pure request data and the boundaries used by the audio application."""

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import ContextManager, Mapping, Protocol, cast


@dataclass(frozen=True)
class AudioRequest:
    model: str
    prompt: str
    output: str
    cache: str
    options: Mapping[str, object]

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> 'AudioRequest':
        common = {'model', 'prompt', 'output', 'cache'}
        for field in common:
            value = payload.get(field)
            if not isinstance(value, str) or not value.strip() or '\x00' in value:
                raise ValueError(f'{field} must be a nonempty string without NUL characters')
        return cls(
            model=cast(str, payload['model']), prompt=cast(str, payload['prompt']),
            output=cast(str, payload['output']), cache=cast(str, payload['cache']),
            options=MappingProxyType({key: value for key, value in payload.items()
                                      if key not in common}),
        )

    def to_dict(self) -> dict[str, object]:
        return dict(self.options, model=self.model, prompt=self.prompt,
                    output=self.output, cache=self.cache)


@dataclass(frozen=True)
class ArtifactPaths:
    project_root: Path
    output: Path
    cache: Path


class AudioBackend(Protocol):
    """Backend previews must contain only provenance-safe, JSON-compatible data."""

    protected_paths: tuple[Path, ...]

    def normalize(self, payload: Mapping[str, object]) -> AudioRequest: ...
    def preview(self, request: AudioRequest, paths: ArtifactPaths) -> dict[str, object]: ...
    def status(self) -> dict[str, object]: ...
    def generate(self, request: AudioRequest, paths: ArtifactPaths) -> None: ...


class Artifacts(Protocol):
    def reserve_output(self) -> None: ...
    def fingerprint(self) -> str: ...
    def record(self, value: Mapping[str, object]) -> None: ...


class ArtifactStore(Protocol):
    def read_request(self, project: Path, request: Path) -> dict[str, object]: ...
    def resolve(self, project: Path, request: AudioRequest,
                protected_paths: tuple[Path, ...]) -> ArtifactPaths: ...
    def ensure_available(self, paths: ArtifactPaths) -> None: ...
    def reserve(self, paths: ArtifactPaths) -> ContextManager[Artifacts]: ...
