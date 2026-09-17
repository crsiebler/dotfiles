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
