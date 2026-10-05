# Requirements

## Required and conditional dependencies

The outer bundled CLI needs Python 3.11+; its imports are standard library.
Local generation uses the supported Stable Audio MLX backend: Apple Silicon
macOS, Git, uv, a Python 3.11 backend environment, the pinned source revision,
and four verified model NPZ files. Backend setup installs that revision's Python
requirements plus soundfile and huggingface-hub; dependencies are not fully
transitively locked. Source/weight revisions and hashes are owned by
`scripts/stable_audio_runtime.py`, not a guessed latest pip package.

Model access and license acceptance are separate user decisions. Hugging Face
authentication may be required; never inspect credential stores. FFmpeg, Conda,
ElevenLabs, and an audio chat provider are not required for the shipped generator.
Project-specific post-processing may introduce its own selected utilities.

## Installation and checks

For missing prerequisites on macOS with existing Homebrew, after setup approval:

```sh
brew install python@3.11 git uv
python3.11 --version
git --version
uv --version
```

See official [uv installation](https://docs.astral.sh/uv/getting-started/installation/)
and the [Python formula](https://formulae.brew.sh/formula/python@3.11).
Use the loaded skill path to preview provisioning before any download:

```sh
skill_dir='/absolute/path/to/loaded/create-audio'
python3.11 "$skill_dir/scripts/create_audio.py" setup --dry-run
```

Replace the path. Follow [backend setup](local-audio.md) for model terms,
`--models-root`, and optional verified `--weights-from`.
Only after explicit model-directory/dependency setup authorization and the user's
acceptance of the applicable model terms:

```sh
python3.11 "$skill_dir/scripts/create_audio.py" setup --accept-model-terms
python3.11 "$skill_dir/scripts/create_audio.py" status
```

The default root is `~/Models/local-audio/`, outside the active project. That
requires separate filesystem/global setup authority; project generation approval
does not grant it. Existing roots are preserved. AI configuration installation
does not provision models. `status` checks presence/revisions/hashes, not
successful inference; qualify generation on the actual host.
