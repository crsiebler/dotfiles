# Producing and document skill verification

The ten new portable bundles are create-skill, create-gif, create-docx, create-pptx,
create-xlsx, create-pdf, read-docx, read-pptx, read-xlsx and read-pdf. Each includes
its own scripts and requirements; no sibling skill supplies runtime Python imports.

`tests/document_skills_contract_test.py` checks unique discovery, required resources,
local Markdown link closure, local helper imports and Apache provenance. It copies
all ten bundles into an isolated installation, invokes helpers from a third unrelated
working directory, creates actual artifacts, reads each document back, checks missing
packages, and compares source/installed-resource hashes. Format-specific tests add
independent library/XML fixtures, malformed/boundary cases and content checks.
No test installs the skills into personal configuration as a validation step.

Use existing dependency environments; setup requires separate authorization. The
suite supports `SKILL_TEST_PYTHON` for document/GIF helpers and an optional
`SKILL_TEST_YAML_PYTHON` for create-skill's PyYAML environment. The latter falls back
to SKILL_TEST_PYTHON, then the test driver. This permits existing separate environments
without injecting packages into sys.path or weakening missing-dependency tests.

```sh
SKILL_TEST_PYTHON=/absolute/path/to/document-environment/bin/python \
SKILL_TEST_YAML_PYTHON=/absolute/path/to/yaml-environment/bin/python \
python3.11 -m unittest discover -s tests -p '*test*.py'
make validate-ai
```

Verified helper environments: Python3.12.14 with Pillow12.3.0, python-docx1.2.0,
python-pptx1.0.2, XlsxWriter3.2.9, openpyxl3.1.5, ReportLab4.4.9 and pypdf6.10.0;
Python3.11 with PyYAML6.0.3. All new helper syntax is parsed by Python3.11 in the
contract test; direct Python3.11/document-library pairing remains unverified.
Requirements pins reflect these actual tested libraries. Missing-dependency paths
run with site packages disabled; required artifact tests do not skip for absent libs.

No standalone repository typecheck or configured Python formatter exists. Source
validation, Python3.11 syntax parsing and regression tests are distinct evidence,
not a claim that an unavailable typecheck/formatter passed. Existing unrelated
conditional test skips are reported separately from required artifact verification.

Rendering is separate from package validation. PPTX's two-slide fixture and PDF's
five fixture pages were rendered and visually inspected; no general guarantee of
future content, font shaping or viewer equivalence follows. No DOCX rendering,
XLSX recalculation or live AI asset generation is claimed. Readers preserve bytes,
report bounded omissions and do not promise OCR, visual completeness, recalculation,
external refresh, or lossless Office reconstruction.
