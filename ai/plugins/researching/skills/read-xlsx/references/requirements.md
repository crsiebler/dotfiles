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
