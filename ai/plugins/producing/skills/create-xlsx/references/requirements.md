# Requirements

Python 3.11+ baseline; tested XlsxWriter 3.2.9 for production and openpyxl 3.1.5
for independent reopened validation/inspection. requirements.txt pins these versions.
Tests use existing bundled Python 3.12.14 through SKILL_TEST_PYTHON with a Python3.11
repository driver. Direct Python3.11/library pairing is unverified. Neither library
is a calculation engine. No Excel, LibreOffice, native role, creation/reading sibling,
server, or model is required. `check` reports actual versions; missing packages exit 3.
Dependency setup is separately authorized, never performed by helpers/AI installation.

Original implementation follows official XlsxWriter
[worksheet APIs](https://xlsxwriter.readthedocs.io/worksheet.html),
[workbook options](https://xlsxwriter.readthedocs.io/workbook.html), and
[formula guidance](https://xlsxwriter.readthedocs.io/working_with_formulas.html),
checked through Context7 and package fixtures. Independent inspection uses
[openpyxl loading](https://openpyxl.readthedocs.io/en/stable/tutorial.html#loading-from-a-file).
No proprietary Anthropic document sources were consulted or copied.

## Installation and availability check

Use an existing compatible project environment, or create a fresh project-local
one after dependency installation is authorized. Resolve `skill_dir` to the
advertised loaded skill; do not assume the checkout is the installed bundle.

```sh
skill_dir='/absolute/path/to/loaded/create-xlsx'
python3.11 -m venv .venv-create-xlsx
./.venv-create-xlsx/bin/python -m pip install -r "$skill_dir/requirements.txt"
./.venv-create-xlsx/bin/python "$skill_dir/scripts/create_xlsx.py" check
```

Replace the path placeholder and choose an unused environment directory.
[Python installation](https://www.python.org/downloads/) is separate if missing;
macOS with existing Homebrew can use approved `brew install python@3.11`.
Keep the bundled pins and normal transitive dependencies; do not use global pip,
overwrite an existing environment, or upgrade packages implicitly.
A successful `check` establishes availability only, not artifact/rendering quality.

## Optional recalculation and rendering

Excel or LibreOffice is conditional when actual formula recalculation or visual
inspection is requested. Approved macOS setup with existing Homebrew:
`brew install --cask libreoffice`
([cask](https://formulae.brew.sh/cask/libreoffice)); other hosts use
[LibreOffice downloads](https://www.libreoffice.org/download/download-libreoffice/).
Verify `soffice --version` or its installed executable. Microsoft Excel needs a
separately licensed installation. Use a project copy for recalculation and reopen
it to verify results. Installing Python libraries does not calculate formulas.
