# Requirements and tested environment

- Python 3.11+ syntax baseline; python-docx 1.2.0 is pinned in requirements.txt.
- Verified artifact operations under existing bundled Python 3.12.14 and
  python-docx 1.2.0, including its installed lxml dependency. The repository test
  driver is Python 3.11 with SKILL_TEST_PYTHON selecting the dependency runtime.
  The direct Python 3.11 + python-docx combination has not been provisioned/tested.
- Pillow is used only to construct test image fixtures; the shipped helper uses
  python-docx's PNG/JPEG reader and does not import Pillow.
- Font names in styles reference recipient-installed fonts; no fonts are bundled
  or downloaded, and naming a font does not verify glyph coverage or licensing.
- Word or LibreOffice rendering is optional and separate. No native renderer,
  conversion utility, model, or harness-specific tool is required for creation or
  structural inspection. The helper never starts a renderer or converts formats.

`check` reports actual Python/library versions; missing dependencies exit 3.
Dependency setup is a separate user-authorized operation, never a side effect of
this helper or the AI configuration installer.

Original implementation uses the public
[python-docx document API](https://python-docx.readthedocs.io/en/latest/api/document.html),
[section API](https://python-docx.readthedocs.io/en/latest/api/section.html), and
[style guidance](https://python-docx.readthedocs.io/en/latest/user/styles-using.html).
These APIs were checked through Context7 and local artifact tests. No proprietary
Anthropic document skill sources were consulted or copied.
