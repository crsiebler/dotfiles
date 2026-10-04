# Requirements and font fixture

Python 3.11+ baseline; ReportLab4.4.9 generates PDFs, pypdf6.10.0 independently
inspects them, Pillow12.3.0 validates image inputs. Versions in requirements.txt
were verified under existing bundled Python3.12.14; repository tests use Python3.11
with SKILL_TEST_PYTHON selecting that runtime. Direct Python3.11 pairing unverified.
No sibling skill, renderer, model or native role is required by the helper.
Dependency setup is separate and authorized, never implicit or part of AI install.

Tests select ReportLab's unmodified `fonts/Vera.ttf` and copy its adjacent
`bitstream-vera-license.txt` unchanged into project fixtures. The inspected license
permits use/copy/redistribution with notices and forbids standalone font resale;
no font binary is vendored by this skill. This licensed fixture covers the tested
Latin/accents and does not claim universal Unicode coverage. Users must supply an
appropriate licensed TrueType font for their content. No font downloads occur.

Original implementation uses official ReportLab
[Platypus](https://docs.reportlab.com/reportlab/userguide/ch5_platypus),
[tables](https://docs.reportlab.com/reportlab/userguide/ch7_tables), and
[fonts](https://docs.reportlab.com/reportlab/userguide/ch3_fonts), plus pypdf
[text extraction](https://pypdf.readthedocs.io/en/stable/user/extract-text.html).
Context7 research and local artifact tests informed this original code; no proprietary
Anthropic document skill sources were consulted. Font glyph-map inspection is tied
to the pinned ReportLab version and tested missing-glyph behavior.

## Installation and availability check

Use an existing compatible project environment, or create a fresh project-local
one after dependency installation is authorized. Resolve `skill_dir` to the
advertised loaded skill; do not assume the checkout is the installed bundle.

```sh
skill_dir='/absolute/path/to/loaded/create-pdf'
python3.11 -m venv .venv-create-pdf
./.venv-create-pdf/bin/python -m pip install -r "$skill_dir/requirements.txt"
./.venv-create-pdf/bin/python "$skill_dir/scripts/create_pdf.py" check
```

Replace the path placeholder and choose an unused environment directory.
[Python installation](https://www.python.org/downloads/) is separate if missing;
macOS with existing Homebrew can use approved `brew install python@3.11`.
Keep the bundled pins and normal transitive dependencies; do not use global pip,
overwrite an existing environment, or upgrade packages implicitly.
A successful `check` establishes availability only, not artifact/rendering quality.

## Optional rendering and required font input

For requested raster preview, Poppler's `pdftoppm` is optional. Approved macOS
setup with existing Homebrew: `brew install poppler`
([formula](https://formulae.brew.sh/formula/poppler)); verify `pdftoppm -v`.
For other hosts, use [Poppler distributions](https://poppler.freedesktop.org/).
Write previews inside the project. Rendering is separate from helper `check`.

The creation request needs a licensed TrueType font file with verified glyph
coverage. Obtain it from the user or an approved font source and retain required
license notices; a system font name is not a supplied file. No automatic font
download or installation is included.
