# Requirements

Python 3.11+ baseline, openpyxl 3.1.5 pinned in requirements.txt. Verified extraction
uses existing bundled Python3.12.14/openpyxl3.1.5 with Python3.11 repository test
driver and SKILL_TEST_PYTHON selecting that runtime. Direct Python3.11/library
pairing is unverified. XlsxWriter is used only to construct independent fixtures;
the reader does not import it. No creation skill, Excel, LibreOffice, model, native
role, renderer or calculation engine is required.

`check` reports actual versions and missing packages exit 3. Dependency setup is a
separate authorized operation, never performed by helpers or AI configuration install.
Original implementation follows official openpyxl
[loading guidance](https://openpyxl.readthedocs.io/en/stable/tutorial.html#loading-from-a-file),
[optimized reading](https://openpyxl.readthedocs.io/en/stable/optimized.html), and
[cell utilities](https://openpyxl.readthedocs.io/en/stable/api/openpyxl.utils.cell.html).
Context7 verified data_only/keep_links/read_only, dimension-hint limitations and
range iteration. No proprietary document skill implementations were consulted.

## Installation and availability check

Use an existing compatible project environment, or create a fresh project-local
one after dependency installation is authorized. Resolve `skill_dir` to the
advertised loaded skill; do not assume the checkout is the installed bundle.

```sh
skill_dir='/absolute/path/to/loaded/read-xlsx'
python3.11 -m venv .venv-read-xlsx
./.venv-read-xlsx/bin/python -m pip install -r "$skill_dir/requirements.txt"
./.venv-read-xlsx/bin/python "$skill_dir/scripts/read_xlsx.py" check
```

Replace the path placeholder and choose an unused environment directory.
[Python installation](https://www.python.org/downloads/) is separate if missing;
macOS with existing Homebrew can use approved `brew install python@3.11`.
Keep the bundled pins and normal transitive dependencies; do not use global pip,
overwrite an existing environment, or upgrade packages implicitly.
A successful `check` establishes availability only, not artifact/rendering quality.
