# Requirements

Python 3.11+ baseline and python-pptx 1.0.2 (with its normal transitive dependencies).
Verified using existing bundled Python 3.12.14 and python-pptx 1.0.2; Python 3.11
runs repository tests with SKILL_TEST_PYTHON selecting the dependency runtime.
Direct Python 3.11/library pairing is unverified. Pillow constructs independent
test fixtures; this reader does not import it directly or inspect picture pixels.
No creation skill, native role, model, Office installation, renderer, or converter
is required. `check` reports actual versions; missing packages exit 3.

Dependency setup is a separate user-authorized operation, never automatic.
Original code follows official [notes guidance](https://python-pptx.readthedocs.io/en/latest/user/notes.html),
[shape APIs](https://python-pptx.readthedocs.io/en/latest/api/shapes.html), and
[chart APIs](https://python-pptx.readthedocs.io/en/latest/api/chart.html).
Context7 verified existing-note detection, optional notes text frames, group/text
behavior, and category-series access. No proprietary document skill code consulted.

## Installation and availability check

Use an existing compatible project environment, or create a fresh project-local
one after dependency installation is authorized. Resolve `skill_dir` to the
advertised loaded skill; do not assume the checkout is the installed bundle.

```sh
skill_dir='/absolute/path/to/loaded/read-pptx'
python3.11 -m venv .venv-read-pptx
./.venv-read-pptx/bin/python -m pip install -r "$skill_dir/requirements.txt"
./.venv-read-pptx/bin/python "$skill_dir/scripts/read_pptx.py" check
```

Replace the path placeholder and choose an unused environment directory.
[Python installation](https://www.python.org/downloads/) is separate if missing;
macOS with existing Homebrew can use approved `brew install python@3.11`.
Keep the bundled pins and normal transitive dependencies; do not use global pip,
overwrite an existing environment, or upgrade packages implicitly.
A successful `check` establishes availability only, not artifact/rendering quality.
