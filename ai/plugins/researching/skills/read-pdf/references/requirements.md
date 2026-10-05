# Requirements

Python3.11+ baseline; pypdf6.10.0 pinned in requirements.txt. Verified with existing
bundled Python3.12.14/pypdf6.10.0; Python3.11 drives repository tests with
SKILL_TEST_PYTHON selecting the dependency runtime. Direct Python3.11 pairing is
unverified. ReportLab/Pillow create independent test fixtures only; the shipped
reader requires neither. No creation skill, model, renderer, Office application,
OCR engine or native role is required. pdfplumber remains out of scope.

`check` reports versions; missing dependencies exit3. Setup requires separate user
authorization and is never performed automatically or by AI configuration install.
Original implementation follows official pypdf
[text extraction](https://pypdf.readthedocs.io/en/stable/user/extract-text.html) and
[metadata](https://pypdf.readthedocs.io/en/stable/user/metadata.html) guidance, checked
through Context7 and independent fixtures. No proprietary document skill code read.
Content-stream decompression still consumes memory before decoded-size rejection;
limits bound supported inputs and output, not an operating-system resource sandbox.

## Installation and availability check

Use an existing compatible project environment, or create a fresh project-local
one after dependency installation is authorized. Resolve `skill_dir` to the
advertised loaded skill; do not assume the checkout is the installed bundle.

```sh
skill_dir='/absolute/path/to/loaded/read-pdf'
python3.11 -m venv .venv-read-pdf
./.venv-read-pdf/bin/python -m pip install -r "$skill_dir/requirements.txt"
./.venv-read-pdf/bin/python "$skill_dir/scripts/read_pdf.py" check
```

Replace the path placeholder and choose an unused environment directory.
[Python installation](https://www.python.org/downloads/) is separate if missing;
macOS with existing Homebrew can use approved `brew install python@3.11`.
Keep the bundled pins and normal transitive dependencies; do not use global pip,
overwrite an existing environment, or upgrade packages implicitly.
A successful `check` establishes availability only, not artifact/rendering quality.
