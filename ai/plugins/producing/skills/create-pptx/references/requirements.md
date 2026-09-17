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
