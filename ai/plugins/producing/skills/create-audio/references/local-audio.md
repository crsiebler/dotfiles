# Audio workflow and Stable Audio backend

## Invocation

Agents load `create-audio` and resolve `<skill>` to its installed directory.
The neutral CLI exposes:

```sh
python3.11 <skill>/scripts/create_audio.py status
python3.11 <skill>/scripts/create_audio.py generate --request assets/audio/requests/latch.json --dry-run
python3.11 <skill>/scripts/create_audio.py generate --request assets/audio/requests/latch.json
```

The current directory is the project root unless `--project-root` is supplied.
Relative request paths are resolved from that root, even when invoked elsewhere.
Use the same skill-relative entry point in each harness. There is no shell alias
and no dependency on OpenCode's specific installation path.

OpenCode's `/create-audio <request or brief>` asks the current assistant to load
the skill. Its chat model orchestrates the local audio generator. Stable Audio
is not an OpenAI-compatible chat server and is not a `/models` entry. The JSON
request's `model` field selects the audio backend; currently the supported value
is `stable-audio-3-small-sfx`.

## Project request

This example is illustrative, not a global generation preset. For the Stable Audio backend, every field is
required; unknown fields fail rather than silently doing something unexpected.
Store the request and artistic source material in the active project.

```json
{
  "model": "stable-audio-3-small-sfx",
  "prompt": "A small metal latch clicks open in a quiet room",
  "negative_prompt": "speech, music, long reverb",
  "seconds": 2.5,
  "steps": 8,
  "seed": 42,
  "cfg": 3.0,
  "apg": 1.0,
  "output": "assets/audio/generated/latch.raw.wav",
  "cache": ".cache/local-audio"
}
```

`output` and `cache` must be separate, project-relative locations that resolve
inside the project. Existing output or provenance is never overwritten. The
Stable Audio adapter supports 0.5–120 seconds, integer steps 1–1000, unsigned 32-bit seeds,
CFG −100–100, and APG 0–1. These are validation bounds, not recommended quality
settings or promises that the host can handle every combination. The project's
qualified resource budget should narrow them. No unrequested retries occur.

The pinned backend uses the Small-SFX DiT and SAME-Small decoder. Raw output
uses 32-bit float WAV to preserve decoder amplitude. Master sample rate,
channel layout, loudness, trimming, loops, and runtime exports belong to project
processing instructions; the generator does not silently apply them. Prompting
for a loop does not prove a seamless loop.

Generation records the request, command, revisions, timestamps, output encoding,
and SHA-256 in `<output>.provenance.json`. A failed invocation reserves its paths
and records failure; inspect any partial source and choose a new name to retry.
Generation runs offline with project-local Hugging Face, XDG, uv, and temporary
directories. Setup caches are separate and live beside the shared runtime.

## Setup

Setup is an explicit one-time dependency installation, separate from dotfiles
AI installation. It requires Apple Silicon macOS, Git, and `uv` already on PATH.
It creates a Python 3.11 environment in a new models root. Existing roots are
never replaced, repaired, or relocated automatically.

Preview the exact commands without writing or downloading:

```sh
python3.11 <skill>/scripts/create_audio.py setup --dry-run
```

After reviewing the model's Stable Audio Community License and required Gemma
terms, run setup explicitly:

```sh
python3.11 <skill>/scripts/create_audio.py setup --accept-model-terms
```

Model access may require separately configured Hugging Face authentication.
The runner never reads credential stores or accepts licenses on your behalf.
The flag records your decision for this invocation; project commercial-use
evidence and qualification remain project responsibilities.

To reuse existing downloaded weights, supply the directory containing the four
pinned NPZ files (not the old virtual environment):

```sh
python3.11 <skill>/scripts/create_audio.py setup --weights-from /absolute/path/to/existing/MLX --dry-run
python3.11 <skill>/scripts/create_audio.py setup --weights-from /absolute/path/to/existing/MLX --accept-model-terms
```

The setup checks SHA-256 before installing, copies those files, and builds a
fresh environment under `~/Models/local-audio/`. It leaves the original runtime
and weights intact. Source cloning and dependency installation still need network
access. This avoids relocating virtual environments with embedded absolute paths.
An interrupted setup leaves its files for inspection; retry into a new explicit
`--models-root` rather than deleting an existing installation implicitly.

Source and weight revisions and hashes are pinned in `scripts/stable_audio_runtime.py`.
Python dependencies follow that source revision's requirements; they are not a
fully locked transitive environment. `status` verifies source HEAD, runtime
file presence, and weight hashes, not a pristine checkout or successful inference.
Qualify actual generation on the target host before production use.

## Architecture and extensions

- `audio_domain.py`: request and artifact data, backend/store protocols; no I/O.
- `audio_service.py`: generation lifecycle, injected backend and artifact store.
- `audio_files.py`: project path resolution, exclusive files, hashes, evidence.
- `stable_audio_mlx.py`: MLX options, commands, environment, subprocess execution.
- `stable_audio_runtime.py`: local model checks and explicit provisioning.
- `create_audio.py`: CLI and dependency construction.

The flat request format is unchanged. Common fields are `model`, `prompt`,
`output`, and `cache`; each adapter validates its remaining options. MLX-specific
fields such as CFG and APG are not requirements of the shared domain.

A new backend implements the small backend protocol and is wired in the CLI's
composition function. It does not need to inherit MLX settings, subprocesses,
local directories, or installation requirements. The filesystem adapter remains
responsible for project-contained artifacts. No hosted backend or automatic
local-to-hosted fallback is currently implemented. Its connection configuration
and authorization must be designed when a concrete provider is selected.

The service writes an initial provenance record and records ordinary failures,
including output reservation and hashing failures, without provider exception
text. This is not crash-atomic storage. The Stable Audio adapter declares float
WAV output; the shared service checks nonempty output and hashes it, not waveform
validity or listening approval.

## Earlier skill copies

The bundled CLI was renamed from `local_audio.py` to `create_audio.py`, and
`audio_runtime.py` to `stable_audio_runtime.py`. If an earlier copy was installed,
the OpenCode installer can refuse obsolete files to protect local modifications.
Inspect and preserve the exact old files before approved cleanup; do not delete
an entire skill directory or plugin cache. Source changes do not update already
installed copies or loaded shell functions automatically.
