# Presentation authoring contract

Resolve scripts/create_pptx.py from this installed skill. Commands:

```sh
python /loaded/create-pptx/scripts/create_pptx.py check
python /loaded/create-pptx/scripts/create_pptx.py layouts
python /loaded/create-pptx/scripts/create_pptx.py --project /project create request.json deck.pptx
python /loaded/create-pptx/scripts/create_pptx.py --project /project inspect deck.pptx
```

`layouts` inventories the library's blank presentation: layout names and placeholder
idx, name, type, and geometry. Select an exact unique name from that inventory;
indices are never assumed. Arbitrary templates/editing are outside this helper.
Each slide can populate text placeholders by inspected idx and add explicit
editable shapes. Inherited placeholders retain template geometry. Avoid populating
an inherited placeholder and adding another shape on top of it.

Request JSON: `width` and `height` in inches (1–56), and 1–100 `slides`.
Each slide has `layout` (exact name), optional `placeholders` (list of `{idx,text}`),
and `shapes` (up to 100). Shapes have `kind`, `x`, `y`, `width`, `height` (inches,
entire box within the slide). Supported kinds:

- `text`: `text`, optional `font` (default Arial), `size` (8–96 points),
  `bold` (boolean), `color` (six hex digits). Text remains editable; wrap enabled.
- `image`: project-relative `path` to PNG/JPEG. Fit proportionally centered inside
  the supplied box, without cropping or stretching.
- `table`: rectangular nonempty `rows` of strings, at most 50 rows by 20 columns,
  optional `size` (8–48 points). No automatic pagination or cell-fit guarantee.
- `chart`: `categories` (1–100 strings), `series` (1–10 objects with `name` and
  same-length finite numeric `values`). Native editable clustered column chart;
  embedded workbook supplied by python-pptx. No unsupported chart-type fallback.

Text fields are at most 20,000 characters. Unknown keys, invalid geometry, duplicate
placeholder indices, unavailable text placeholders, and nonfinite values fail.
Requests/images/input PPTX are regular nonsymlink project files <=16 MiB; ZIP inputs
are limited to 2000 members/64 MiB expanded. Fresh output with existing parent must
be inside project and outside installed skill resources. No automatic directories,
replacement, installations, conversion, or execution of document content.

```json
{
  "width": 10,
  "height": 5.625,
  "slides": [{
    "layout": "Blank",
    "shapes": [
      {"kind":"text","x":0.6,"y":0.3,"width":8.8,"height":0.7,"text":"Quarterly results","size":28,"bold":true},
      {"kind":"chart","x":0.8,"y":1.3,"width":8.4,"height":3.7,"categories":["Q1","Q2"],"series":[{"name":"Units","values":[12,18]}]}
    ]
  }]
}
```

The example selects `Blank` after verifying that name in `layouts`.
`inspect` reports dimensions, slide count, up to 100 slides/100 shapes each, text
excerpts, table cells, native chart categories/series, shape geometry, and truncation.
Global limits are 50,000 excerpt characters and 10,000 table/chart values; it is
structural inspection, not a general research reader. Creation reopens the output
and compares supported content/geometry before exclusive publication. Exit codes:
0 success, 2 invalid input/collision, 3 missing dependencies, 4 generation/I/O,
5 failed validation. Diagnostics omit request/document contents.
