# Requirements

Python 3.11+ baseline and python-pptx 1.0.2 (with its normal transitive dependencies).
Verified using existing bundled Python 3.12.14 and python-pptx 1.0.2; Python 3.11
runs repository tests with SKILL_TEST_PYTHON selecting the dependency runtime.
Direct Python 3.11/library pairing is unverified. Pillow constructs independent
test fixtures; this reader does not import it directly or inspect picture pixels.
No creation skill, native role, model, Office installation, renderer, or converter
is required. `check` reports actual versions; missing packages exit 3.

Dependency setup is a separate user-authorized operation, never automatic.
Original code follows official [notes guidance](https://python-pptx.readthedocs.io/en/latest/user/notes.html),
[shape APIs](https://python-pptx.readthedocs.io/en/latest/api/shapes.html), and
[chart APIs](https://python-pptx.readthedocs.io/en/latest/api/chart.html).
Context7 verified existing-note detection, optional notes text frames, group/text
behavior, and category-series access. No proprietary document skill code consulted.
