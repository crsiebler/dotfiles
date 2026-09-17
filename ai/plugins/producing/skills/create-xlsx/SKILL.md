---
name: create-xlsx
description: Create typed and formatted Excel workbooks with sheets, tables, filters, freeze panes, charts, and explicit formulas while preserving literal strings and reporting formula cache provenance.
---

# Create XLSX

Use for a new workbook. Establish the data meaning, exact identifiers, formats,
formulas, expected results and intended spreadsheet application. Prefer an adequate
native reader for simple reads; this skill does not edit or round-trip existing
workbooks. Read [authoring](references/authoring.md),
[requirements](references/requirements.md), and [validation](references/validation.md).
Resolve scripts/create_xlsx.py from this installed skill.

```sh
python /loaded/create-xlsx/scripts/create_xlsx.py check
python /loaded/create-xlsx/scripts/create_xlsx.py --project /project create request.json report.xlsx
python /loaded/create-xlsx/scripts/create_xlsx.py --project /project inspect report.xlsx
```

Select every cell type explicitly. Keep IDs and untrusted formula-like strings
as strings; request formulas explicitly and obtain trustworthy supplied caches
when offline display matters. Neither a supplied cache nor the writer's default
zero means a formula was calculated. A recalculation flag requests future work by
a spreadsheet application; it is not evidence that calculation has occurred.

Keep requests and artifacts inside the project and installed resources read-only.
Use readable widths and formats, descriptive sheets, simple charts, filters and
frozen headings. Check outputs independently and report actual validation, formula
cache provenance, and any unverified calculation/rendering limitations. No implicit
package setup, conversion, external data refresh, or application launch.
