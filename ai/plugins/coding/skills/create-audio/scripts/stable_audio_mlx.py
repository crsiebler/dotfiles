"""Stable Audio MLX adapter. Framework imports run only in its subprocess."""

from dataclasses import dataclass
import math
import os
from pathlib import Path
import subprocess
import sys
from typing import Callable, Mapping, cast

from audio_domain import ArtifactPaths, AudioRequest
from stable_audio_runtime import MODEL, REVISION, WEIGHT_REVISION, check_runtime, runtime_path


FLOAT_WAV_LAUNCHER = '''
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "scripts"))
import soundfile
import sa3_mlx
def save_float_wav(path, audio, sample_rate=sa3_mlx.SAMPLE_RATE):
    if not sa3_mlx.np.isfinite(audio).all():
        raise RuntimeError("non-finite model output")
    soundfile.write(path, audio.T, sample_rate, subtype="FLOAT", format="WAV")
sa3_mlx.save_wav = save_float_wav
sa3_mlx.main()
'''.strip()


@dataclass(frozen=True)
class StableAudioOptions:
    negative_prompt: str
    seconds: float
    steps: int
    seed: int
    cfg: float
    apg: float

    @classmethod
    def from_request(cls, request: AudioRequest) -> 'StableAudioOptions':
        options = request.options
        if set(options) != {'negative_prompt', 'seconds', 'steps', 'seed', 'cfg', 'apg'}:
            raise ValueError('Stable Audio requires exactly negative_prompt, seconds, steps, seed, cfg, apg')
        negative = options['negative_prompt']
        if not isinstance(negative, str) or '\x00' in negative:
            raise ValueError('negative_prompt must be a string without NUL characters')
        for field, minimum, maximum, integer in (
            ('seconds', 0.5, 120, False), ('steps', 1, 1000, True),
            ('seed', 0, 4294967295, True), ('cfg', -100, 100, False),
            ('apg', 0, 1, False),
        ):
            value = options[field]
            # Bounds first: converting arbitrary-size integers to float can overflow.
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f'{field} must be numeric')
            if ((integer and not isinstance(value, int)) or not minimum <= value <= maximum
                    or (isinstance(value, float) and not math.isfinite(value))):
                raise ValueError(f'{field} must be {minimum}..{maximum}' +
                                 (' (integer)' if integer else ''))
        return cls(negative, cast(float, options['seconds']), cast(int, options['steps']),
                   cast(int, options['seed']), cast(float, options['cfg']), cast(float, options['apg']))


class StableAudioBackend:
    def __init__(self, root: Path, *, run: Callable[..., object] = subprocess.run,
                 inspect: Callable[[Path], dict[str, object]] = check_runtime,
                 environment: Mapping[str, str] | None = None) -> None:
        self.root = root.resolve()
        self.protected_paths = (self.root,)
        self.run = run
        self.inspect = inspect
        self.environment = dict(os.environ if environment is None else environment)

    def normalize(self, payload: Mapping[str, object]) -> AudioRequest:
        request = AudioRequest.from_dict(payload)
        if request.model != MODEL:
            raise ValueError('unsupported Stable Audio model')
        StableAudioOptions.from_request(request)
        if Path(request.output).suffix.lower() != '.wav':
            raise ValueError('raw output must be a WAV file')
        return request

    def command(self, request: AudioRequest, paths: ArtifactPaths) -> list[str]:
        options = StableAudioOptions.from_request(request)
        command = [str(runtime_path(self.root) / '.venv/bin/python'), '-c',
                   FLOAT_WAV_LAUNCHER, '--dit', 'sm-sfx', '--decoder', 'same-s',
                   '--prompt=' + request.prompt, '--negative-prompt=' + options.negative_prompt]
        for field in ('seconds', 'steps', 'seed', 'cfg', 'apg'):
            command.extend(['--' + field, str(getattr(options, field))])
        return command + ['--out', str(paths.output)]

    def preview(self, request: AudioRequest, paths: ArtifactPaths) -> dict[str, object]:
        return {'backend': 'stable-audio-mlx', 'command': self.command(request, paths),
                'cwd': str(runtime_path(self.root)), 'source_revision': REVISION,
                'weight_revision': WEIGHT_REVISION, 'output_encoding': '32-bit IEEE float WAV',
                'output_validation': 'encoding specified by launcher; no independent waveform QC'}

    def status(self) -> dict[str, object]:
        return self.inspect(self.root)

    def generate(self, request: AudioRequest, paths: ArtifactPaths) -> None:
        env = dict(self.environment, PYTHONDONTWRITEBYTECODE='1', HF_HUB_OFFLINE='1',
                   TRANSFORMERS_OFFLINE='1', TOKENIZERS_PARALLELISM='false')
        directories = {
            'HF_HOME': paths.cache / 'huggingface', 'UV_CACHE_DIR': paths.cache / 'uv',
            'XDG_CACHE_HOME': paths.cache / 'xdg', 'TMPDIR': paths.cache / 'tmp',
        }
        for directory in directories.values():
            resolved = directory.resolve()
            if not resolved.is_relative_to(paths.cache):
                raise ValueError('cache children must remain inside the project cache')
        for key, directory in directories.items():
            directory.mkdir(parents=True, exist_ok=True)
            env[key] = str(directory)
        self.run(self.command(request, paths), cwd=runtime_path(self.root), env=env,
                 check=True, stdout=sys.stderr, stderr=sys.stderr)
