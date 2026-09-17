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
