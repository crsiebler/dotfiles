"""Pinned Stable Audio MLX infrastructure; no project generation preferences."""

import os
from pathlib import Path
import platform
import shutil
import subprocess
from typing import cast

from audio_files import sha256


MODEL = 'stable-audio-3-small-sfx'
REPOSITORY = 'https://github.com/Stability-AI/stable-audio-3.git'
REVISION = '5919e8720ab0586f10b1e7c4c597ac19facba407'
WEIGHT_REPOSITORY = 'stabilityai/stable-audio-3-optimized'
WEIGHT_REVISION = '197c684e6ba5370da7a9c710f655a41cb5d68119'
WEIGHTS = {
    'dit_sm-sfx_f16.npz': '7e702d2640699a57fe436ca975fda16832040ba568c1e092c2ae826987558118',
    'same_s_decoder_f32.npz': '909928a8e6937c1ebe6ac4b729f0462bd3773704a11ea18278e42671dc69bfe4',
    'same_s_encoder_f32.npz': 'a48f80d81c30d74c45e2a3047082c4891f715e24c44645adb9c1f4f07afdaf0c',
    't5gemma_f16.npz': '8deb20489f36d9aec539f26c9c67321f99bc5fe300d470435ed6e76be4f16bbd',
}


def models_root(value: str | Path | None = None) -> Path:
    root = Path(value or os.environ.get('LOCAL_AUDIO_MODELS_ROOT') or
                Path.home() / 'Models' / 'local-audio').expanduser()
    if not root.is_absolute():
        raise ValueError('models root must be absolute')
    return root.resolve()


def runtime_path(root: Path) -> Path:
    return Path(root) / 'sources/stable-audio-3/optimized/mlx'


def check_runtime(root: Path) -> dict[str, object]:
    runtime = runtime_path(root)
    source = runtime.parents[1]
    problems = []
    if platform.system() != 'Darwin' or platform.machine() != 'arm64':
        problems.append('Apple Silicon macOS is required')
    revision = None
    if (source / '.git').exists():
        result = subprocess.run(['git', '-C', str(source), 'rev-parse', 'HEAD'],
                                capture_output=True, text=True, check=False)
        revision = result.stdout.strip() if result.returncode == 0 else None
    if revision != REVISION:
        problems.append('pinned source revision is missing or mismatched')
    for relative in ('.venv/bin/python', 'scripts/sa3_mlx.py'):
        if not (runtime / relative).is_file():
            problems.append(f'missing runtime file: {relative}')
    for name, expected in WEIGHTS.items():
        path = runtime / 'models/mlx' / name
        if not path.is_file() or sha256(path) != expected:
            problems.append(f'missing or mismatched weight: {name}')
    return {'ready': not problems, 'model': MODEL, 'runtime': str(runtime),
            'source_revision': revision, 'weight_revision': WEIGHT_REVISION,
            'problems': problems,
            'validation': 'source revision, runtime file presence, weight SHA-256; no inference'}


def setup_plan(root: Path, weights_from: str | Path | None = None) -> dict[str, object]:
    runtime = runtime_path(root)
    source = runtime.parents[1]
    python = runtime / '.venv/bin/python'
    commands = [
        ['git', 'clone', '--no-checkout', REPOSITORY, str(source)],
        ['git', '-C', str(source), 'checkout', '--detach', REVISION],
        ['uv', 'venv', '--python', '3.11', str(runtime / '.venv')],
        ['uv', 'pip', 'install', '--python', str(python), '-r',
         str(runtime / 'requirements.txt'), 'soundfile', 'huggingface-hub'],
    ]
    weights = Path(root) / 'weights' / WEIGHT_REVISION
    if not weights_from:
        commands.append([str(runtime / '.venv/bin/hf'), 'download',
                         WEIGHT_REPOSITORY, '--revision', WEIGHT_REVISION,
                         '--local-dir', str(weights), '--include',
                         *['MLX/' + name for name in WEIGHTS]])
    return {'models_root': str(root), 'model': MODEL, 'commands': commands,
            'weights_from': str(weights_from) if weights_from else None,
            'weight_sha256': WEIGHTS,
            'effects': 'Create a new runtime, install dependencies, copy or download weights, and link verified weights.'}


def setup(root: Path, weights_from: str | Path | None = None,
          accept_model_terms: bool = False) -> dict[str, object]:
    if not accept_model_terms:
        raise ValueError('setup requires --accept-model-terms after reviewing model and Gemma terms')
    if platform.system() != 'Darwin' or platform.machine() != 'arm64':
        raise ValueError('setup requires Apple Silicon macOS')
    for tool in ('git', 'uv'):
        if not shutil.which(tool):
            raise ValueError(f'{tool} is required; install it separately')
    if Path(root).exists():
        raise ValueError('setup requires a new models root; existing installations are never replaced')
    if weights_from:
        weights_from = Path(weights_from).expanduser().resolve(strict=True)
        for name, expected in WEIGHTS.items():
            if sha256(weights_from / name) != expected:
                raise ValueError(f'weight checksum mismatch: {name}')
    plan = setup_plan(root, weights_from)
    Path(root).mkdir(parents=True)
    env = dict(os.environ, UV_CACHE_DIR=str(Path(root) / 'setup-cache/uv'),
               HF_HOME=str(Path(root) / 'setup-cache/huggingface'),
               PYTHONDONTWRITEBYTECODE='1')
    runtime_path(root).parents[2].mkdir(parents=True, exist_ok=True)
    for command in cast(list[list[str]], plan['commands']):
        subprocess.run(command, check=True, env=env)
    weights = Path(root) / 'weights' / WEIGHT_REVISION / 'MLX'
    if weights_from:
        weights.mkdir(parents=True)
        for name in WEIGHTS:
            shutil.copy2(weights_from / name, weights / name)
    destination = runtime_path(root) / 'models/mlx'
    destination.mkdir(parents=True, exist_ok=True)
    for name, expected in WEIGHTS.items():
        if sha256(weights / name) != expected:
            raise ValueError(f'downloaded weight checksum mismatch: {name}')
        (destination / name).symlink_to(weights / name)
    return check_runtime(root)
