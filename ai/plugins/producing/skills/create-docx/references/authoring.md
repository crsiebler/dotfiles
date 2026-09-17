# DOCX creation contract

Invoke the loaded skill's `scripts/create_docx.py` with Python 3.11+:

- `check`: dependency/version report, no writes.
- `--project ROOT create REQUEST.json OUTPUT.docx`: create a fresh document.
- `--project ROOT inspect INPUT.docx`: bounded structure/content inspection.

Relative paths resolve under the existing project ROOT. Reject symlinks, escaped
paths, installed resource outputs, collisions, and missing output parents. No
implicit overwrite, template editing, package installation, or conversion. The
request is at most 1 MiB; DOCX/images at most 16 MiB; DOCX packages at most 1,000
members and 64 MiB expanded. Exit 2 input, 3 dependency, 4 generation/I/O, 5 validation.

The request is a format-specific object with `blocks` (1–1000 ordered entries),
optional `page`, and optional `styles` (up to 50 custom paragraph styles). Unknown
fields fail. Text is literal Unicode, at most 20,000 characters per value and
500,000 characters total. XML-forbidden control characters fail without publication.
No HTML or markup interpretation.

`page`: width_inches, height_inches, and top_margin_inches, bottom_margin_inches,
left_margin_inches, right_margin_inches. Defaults: US Letter, 1-inch margins.
Dimensions must be finite positive numbers, at most 22 inches; margins nonnegative
and leave a positive content area. Word may round to twentieths of a point.

`styles`: map from custom style name to an object containing optional font_name,
size_pt (1–200), bold, italic, and base (existing paragraph style, default Normal).
Names must not shadow built-in styles. Define custom styles before referencing them.

Blocks:

- `{"type":"heading","text":"Title","level":1}`: level 0–9.
- `{"type":"paragraph","text":"Text","style":"Normal"}`: paragraph style optional.
- `{"type":"table","rows":[["A","B"],["1","2"]],"style":"Table Grid"}`:
  nonempty rectangular string rows, up to 100 columns/1000 rows/10000 cells total.
- `{"type":"image","path":"assets/chart.png","width_inches":4}`: inline PNG/JPEG
  from the project, width must fit the current section; aspect ratio preserved.
- `{"type":"page_break"}`: explicit break paragraph.
- `{"type":"section","page":{"width_inches":11,"height_inches":8.5}}`:
  start a new page section; unspecified settings inherit from the previous section.

For example, combine a heading, paragraph using a custom Body style, a table,
image, explicit page break, and landscape section. Choose deliberate typography
and page dimensions from the audience's needs; do not assume package validity
means the content fits or the chosen fonts exist on the recipient's computer.

Creation saves to memory, reopens the package, verifies section/style/table/image
structure and expected text from the construction record, then publishes exclusively.
`inspect` returns section dimensions/margins, paragraph text/styles (up to 100),
tables (up to 20, each 20x20 cells), inline image count, page-break count, custom
style properties, and explicit truncation. It does not render pages or inspect all
arbitrary DOCX features. Use a reader workflow for broader document research.

## Complete tested recipe

```json
{
  "page": {"left_margin_inches": 1.25},
  "styles": {"Body": {"font_name": "Arial", "size_pt": 11}},
  "blocks": [
    {"type": "heading", "text": "Project report", "level": 1},
    {"type": "paragraph", "text": "A concise Unicode résumé.", "style": "Body"},
    {"type": "table", "rows": [["Item", "Status"], ["Draft", "Ready"]]},
    {"type": "page_break"},
    {"type": "paragraph", "text": "Supporting notes"},
    {"type": "section", "page": {"width_inches": 11, "height_inches": 8.5}},
    {"type": "paragraph", "text": "Landscape appendix"}
  ]
}
```

Add the image block described above only with an existing project PNG/JPEG and
an explicit width that fits its section. The integration fixture verifies image
content and relationships; this portable JSON recipe requires no external assets.
