# Requirements

Python 3.11+ and Pillow are required. The helper suite has been tested with Pillow
12.3.0 under the existing bundled Python 3.12.14 runtime; Python 3.11 drives the
repository tests, with SKILL_TEST_PYTHON selecting that subprocess runtime. Direct
Python 3.11 + Pillow compatibility remains unverified until dependency setup is
approved. requirements.txt deliberately pins the actually tested Pillow version.

No ImageIO or NumPy is retained: Pillow provides frame composition, resampling,
quantization, GIF encoding, and decoded inspection. No fonts, native renderer,
conversion tools, provider, or harness-specific image tool is needed for supplied
frames or the procedural circle. No model packages are installed.

`check` reports the Python/Pillow versions. Missing Pillow exits 3 with a dependency
message. Dependency installation is a separate authorized operation; helpers never
install it. Pixel/time/input bounds and unsupported features are in authoring.md.

Pillow GIF save/sequence behavior was checked via Context7 against the
[official file-format documentation](https://github.com/python-pillow/pillow/blob/main/docs/handbook/image-file-formats.rst)
and verified by reopening fixture outputs. GIF's encoded time uses 10 ms units;
viewers may impose different playback minimums.
