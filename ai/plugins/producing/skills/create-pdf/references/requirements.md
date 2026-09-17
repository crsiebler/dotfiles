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
