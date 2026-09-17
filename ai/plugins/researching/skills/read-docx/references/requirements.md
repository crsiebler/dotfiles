# Requirements

Python 3.11+ syntax baseline; python-docx 1.2.0 is pinned in requirements.txt.
Extraction was tested with existing bundled Python 3.12.14, python-docx 1.2.0,
and its installed lxml dependency. Python 3.11 drives repository tests with
SKILL_TEST_PYTHON selecting that runtime; the direct Python 3.11/library pairing
has not been provisioned or verified. No creation skill, model, converter, Word,
LibreOffice, OCR, or native agent is required.

Run `check` to report actual versions. Dependency setup requires separate user
authorization and is never automatic. Errors report missing packages without
printing source content. Resources resolve relative to this installed skill.

Original implementation uses the public [document API](https://python-docx.readthedocs.io/en/latest/api/document.html),
[table API](https://python-docx.readthedocs.io/en/latest/api/table.html), and
[header/footer guidance](https://python-docx.readthedocs.io/en/latest/user/hdrftr.html).
Context7 research verified ordered iter_inner_content and header/footer inheritance;
local fixtures verified the extraction behavior. No proprietary document skill
sources were consulted or copied.
