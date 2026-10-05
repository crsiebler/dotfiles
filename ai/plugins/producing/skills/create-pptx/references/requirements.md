# Requirements and evidence

Python 3.11+ baseline. requirements.txt pins tested python-pptx 1.0.2 and Pillow
12.3.0; Pillow validates PNG/JPEG dimensions/format before placement. python-pptx
also uses its normal lxml and XlsxWriter dependencies. Tested with existing bundled
Python 3.12.14; repository tests use Python 3.11 as driver and SKILL_TEST_PYTHON to
select the dependency runtime. The direct Python 3.11/library pairing is unverified.

`check` reports actual versions. Missing packages exit 3; no command installs
anything. Dependency setup is separate from AI installation and requires user
authorization. No sibling skill, native role, model, server, or Office installation
is needed for creation and structural inspection.

Original implementation follows official [slides](https://python-pptx.readthedocs.io/en/latest/api/slides.html),
[placeholders](https://python-pptx.readthedocs.io/en/latest/user/placeholders-using.html),
[shapes](https://python-pptx.readthedocs.io/en/latest/api/shapes.html), and
[charts](https://python-pptx.readthedocs.io/en/latest/user/charts.html) APIs checked
through Context7 and independent artifact tests. No proprietary Anthropic document
sources were consulted or copied. No fonts are bundled/downloaded; recipient font
availability and licensing remain separate from naming a font in the presentation.

## Installation and availability check

Use an existing compatible project environment, or create a fresh project-local
one after dependency installation is authorized. Resolve `skill_dir` to the
advertised loaded skill; do not assume the checkout is the installed bundle.

```sh
skill_dir='/absolute/path/to/loaded/create-pptx'
python3.11 -m venv .venv-create-pptx
./.venv-create-pptx/bin/python -m pip install -r "$skill_dir/requirements.txt"
./.venv-create-pptx/bin/python "$skill_dir/scripts/create_pptx.py" check
```

Replace the path placeholder and choose an unused environment directory.
[Python installation](https://www.python.org/downloads/) is separate if missing;
macOS with existing Homebrew can use approved `brew install python@3.11`.
Keep the bundled pins and normal transitive dependencies; do not use global pip,
overwrite an existing environment, or upgrade packages implicitly.
A successful `check` establishes availability only, not artifact/rendering quality.

## Optional rendering and fonts

PowerPoint or LibreOffice is conditional for actual visual inspection. Approved
macOS setup with existing Homebrew: `brew install --cask libreoffice`
([cask](https://formulae.brew.sh/cask/libreoffice)); other hosts use
[LibreOffice downloads](https://www.libreoffice.org/download/download-libreoffice/).
Verify `soffice --version` or its installed absolute executable. PDF-to-image
previews can additionally use approved `brew install poppler`
([formula](https://formulae.brew.sh/formula/poppler)); verify `pdftoppm -v`.
Use a project copy and output paths for conversion. Recipient fonts are separate
licensed inputs; structural inspection does not prove font/rendering fidelity.
