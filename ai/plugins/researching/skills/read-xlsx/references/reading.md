# XLSX reading contract

```sh
python /loaded/read-xlsx/scripts/read_xlsx.py check
python /loaded/read-xlsx/scripts/read_xlsx.py --project /project read book.xlsx --sheet Sales --range A1:D20 --max-cells 2000 --max-chars 50000
```

`--sheet` may repeat, selecting exact worksheet names in workbook order. Default:
first 20 worksheets, including hidden sheets; additional worksheets set truncation.
Explicit selection permits at most 20 names; unknown names fail. `--range` is one
finite A1 cell/range (no entire rows/columns, sheet prefixes, or reversed endpoints),
applied to each selected sheet. Default: A1 through actual stored cell bounds,
capped to first 2000 rows/100 columns with truncation reported. Inspect stored XML
cell coordinates instead of trusting possibly incorrect worksheet dimension hints.

Global max-cells 1–20000 and max-chars 1–200000 span all sheets (defaults above).
Blank positions count toward the cell budget; ranges stop at the budget and report
truncation. Character limits apply to extracted strings, including formulas and
format codes. Date/time values use ISO strings, numbers remain numbers. Source path
and SHA-256, selected sheet names, requested/effective ranges, sheet state, and cell
coordinates/types accompany values. Each cell reports row_hidden and column_hidden
(including grouped column spans). Hidden data remains included and clearly marked.

Formula cells have formula text, cached value/type, cache_status `present` or
`missing`, and cache_source `unknown`. A present cache may be stale or a writer
placeholder; missing values never become zero. No save, recalculation, data refresh,
macro execution, automatic conversion or external link resolution. Read-only
openpyxl views supply formula and cached values; project-local source bytes remain
unchanged. The reader is independent of creation skills.

Nonsymlink project-local regular inputs only; project and ancestors must exist
without symlinks. Limits: 16 MiB file, 2000 ZIP members, 64 MiB expanded, 100,000
stored cells and 100,000 row/column definitions across inspected worksheets.
Hidden row/column metadata comes from bounded package XML, as read-only openpyxl
does not expose those dimensions. Other content (charts, images, comments, rich
formatting, macros, external links and merged-cell layout) is not reconstructed;
output always reports these limitations. Empty/truncated cells do not establish
an empty workbook. Chart sheets are outside worksheet selection and reported omitted.

Exit codes: 0 bounded extraction, 2 invalid inputs/limits/package, 3 dependency
missing, 4 parse/I/O failure. Errors omit workbook contents. No output-file option.
