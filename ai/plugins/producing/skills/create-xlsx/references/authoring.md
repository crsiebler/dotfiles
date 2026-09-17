# XLSX authoring contract

```sh
python /loaded/create-xlsx/scripts/create_xlsx.py check
python /loaded/create-xlsx/scripts/create_xlsx.py --project /project create request.json report.xlsx
python /loaded/create-xlsx/scripts/create_xlsx.py --project /project inspect report.xlsx
```

Request JSON has optional `formats` (named objects with `num_format`, `bold`,
`font_color`, `bg_color`, `text_wrap`) and `sheets` (1–20). Each sheet has a unique
case-insensitive valid Excel `name`, rectangular nonempty `rows` (up to 1000 rows,
100 columns; at most 20,000 cells across workbook), optional `widths` (one width
per column, 1–100 character units), `freeze` ([row,column] zero-based split),
`table` (boolean, entire data range with existing first row as unique string headers),
`filter` (boolean, entire data range; mutually exclusive with table), and `charts`
(up to 10). Each column chart has `at` ([row,column] anchor), `category_column`
(zero-based), `value_columns` (1–10 zero-based columns), and optional `title`.
Charts use row 1 onward as data and row 0 as headings; headings must be strings,
category data strings/numbers, value data numbers or explicit formulas.

Every cell is an object with `type`, optional `format` name, and `value` except
`blank`. Types: `string`, `number` (finite), `boolean`, `date` (ISO YYYY-MM-DD,
1900-01-01 onward), `formula` (explicit nonempty leading `=`), `blank`.
Formula cells may specify finite numeric `cached`; omission writes the library's
zero placeholder. These are supplied caches or placeholders, never recalculation.
Creation reports each formula's cache provenance; standalone inspection cannot
infer provenance from an arbitrary workbook and labels it unknown.

Strings remain literal, including leading zeros, formula-like text and URLs. No
implicit number/formula/hyperlink conversion. Strings <=32,767 characters; reject
oversize and all nonzero writer return codes instead of accepting truncation.
Dates use an explicit date format by default; named formats can override display.
Numeric precision follows Excel's floating-point format; use strings for exact IDs.

All paths are nonsymlink project-local regular inputs <=16 MiB, existing project
root/parent, and fresh output outside installed resources. No replacement, external
links, macros, template editing, dependency installation or recalculation is performed.
Invalid requests and writer errors leave source files and existing outputs untouched.
Writer warnings become failures; construct workbook entirely in memory before publish.

```json
{
  "formats": {"money": {"num_format": "$#,##0.00"}},
  "sheets": [{"name": "Sales", "table": true, "freeze": [1,0], "widths": [18,18],
    "rows": [
      [{"type":"string","value":"Region"},{"type":"string","value":"Amount"}],
      [{"type":"string","value":"001"},{"type":"number","value":12.5,"format":"money"}],
      [{"type":"string","value":"West"},{"type":"formula","value":"=B2*2","cached":25,"format":"money"}]
    ],
    "charts": [{"at":[5,0],"category_column":0,"value_columns":[1],"title":"Sales"}]
  }]
}
```

`inspect` returns sheet names, bounded cell coordinates/types/values/formulas/caches,
calculation settings and truncation; defaults up to 2000 cells/50,000 characters,
across up to 20 sheets and the first 100 columns/2000 rows per sheet. No calculation engine is started. Creation independently
reopens with openpyxl to compare cell values/types/formulas/caches and formats before
publication. Package input limits: 2000 members/64 MiB expanded. Exit codes: 0 success,
2 invalid input/collision, 3 missing dependency, 4 writer/I/O failure, 5 validation.
