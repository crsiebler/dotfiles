# Requirements

Python 3.11+ and Pillow are required. The helper suite has been tested with Pillow
12.3.0 under the existing bundled Python 3.12.14 runtime; Python 3.11 drives the
repository tests, with SKILL_TEST_PYTHON selecting that subprocess runtime. Direct
Python 3.11 + Pillow compatibility remains unverified until dependency setup is
approved. requirements.txt deliberately pins the actually tested Pillow version.

No ImageIO or NumPy is retained: Pillow provides frame composition, resampling,
quantization, GIF encoding, and decoded inspection. No fonts, native renderer,
conversion tools, provider, or harness-specific image tool is needed for supplied
frames or the procedural circle. No model packages are installed.

`check` reports the Python/Pillow versions. Missing Pillow exits 3 with a dependency
message. Dependency installation is a separate authorized operation; helpers never
install it. Pixel/time/input bounds and unsupported features are in authoring.md.

Pillow GIF save/sequence behavior was checked via Context7 against the
[official file-format documentation](https://github.com/python-pillow/pillow/blob/main/docs/handbook/image-file-formats.rst)
and verified by reopening fixture outputs. GIF's encoded time uses 10 ms units;
viewers may impose different playback minimums.

## Installation and availability check

Use an existing compatible project environment, or create a fresh project-local
one after dependency installation is authorized. Resolve `skill_dir` to the
advertised loaded skill; do not assume the checkout is the installed bundle.

```sh
skill_dir='/absolute/path/to/loaded/create-gif'
python3.11 -m venv .venv-create-gif
./.venv-create-gif/bin/python -m pip install -r "$skill_dir/requirements.txt"
./.venv-create-gif/bin/python "$skill_dir/scripts/create_gif.py" check
```

Replace the path placeholder and choose an unused environment directory.
[Python installation](https://www.python.org/downloads/) is separate if missing;
macOS with existing Homebrew can use approved `brew install python@3.11`.
Keep the bundled pins and normal transitive dependencies; do not use global pip,
overwrite an existing environment, or upgrade packages implicitly.
A successful `check` establishes availability only, not artifact/rendering quality.

## Optional generated frames

An image-generation provider is conditional only when new AI-created frames are
requested. Discover the applicable advertised skill and exposed provider before
use; follow that skill's requirements and spending approval. Supplied-frame GIF
assembly does not require a provider or extra model packages.
