# PDF authoring contract

```sh
python /loaded/create-pdf/scripts/create_pdf.py check
python /loaded/create-pdf/scripts/create_pdf.py --project /project create request.json report.pdf
python /loaded/create-pdf/scripts/create_pdf.py --project /project inspect report.pdf
```

Request: `font` is a project-relative licensed TrueType font file, `page` optionally
sets `width`, `height`, `margin` in inches (default Letter 8.5×11, margin 0.75;
dimensions 3–30, margin 0.3–3 with positive content area), and `blocks` is 1–500
objects. All text is literal, escaped before ReportLab paragraph markup; no raw
HTML/XML or external resource URLs. Explicit font is embedded; missing glyphs fail
before publication rather than silently substituting. Shaping/RTL support is not
promised by glyph coverage.

Blocks:

- `heading`: `text`, optional `level` 1–3, semantic visual hierarchy (not PDF tags).
- `paragraph`: `text`, optional `size` 8–24 points; wrapping and paragraph spacing.
- `table`: rectangular nonempty `rows` (1–100 rows, 1–12 columns) of strings,
  optional `widths` in inches (one per column, sum within content width); header row
  repeats across pages, cells wrap, rows split only at row boundaries.
- `image`: `path` PNG/JPEG and `width` in inches, preserving source aspect ratio;
  reject images too tall/wide for the content frame instead of clipping.
- `page_break`: no additional fields. Every page has a `Page N` footer.

Strings <=20,000 characters, total text <=200,000; reject unknown keys, invalid
font/images, missing glyphs, unusable page geometry and oversized unsplittable
content. Outputs <=16 MiB and <=100 pages. Input files <=16 MiB. Files/ancestors
must be nonsymlink project-local paths; output must be fresh with existing parent
outside installed resources. Requests and input assets remain unchanged. Build in
memory, independently check with pypdf, then publish exclusively.

```json
{
  "font": "Vera.ttf",
  "page": {"width":8.5,"height":11,"margin":0.75},
  "blocks": [
    {"kind":"heading","text":"Résumé & results","level":1},
    {"kind":"paragraph","text":"Literal <tag> & characters stay visible."},
    {"kind":"table","rows":[["Region","Units"],["East","12"],["West","18"]]},
    {"kind":"page_break"},
    {"kind":"paragraph","text":"Second page evidence."}
  ]
}
```

The recipe requires a project font; tests copy ReportLab's unmodified licensed
Vera.ttf with its license into the fixture. No helper bundles/downloads fonts.
`inspect` reports up to100 pages with geometry and text excerpts, global50,000
character limit and explicit truncation. Page streams >8 MiB or total >32 MiB
are refused before text extraction (decompression itself still needs memory).
Exit codes: 0 success, 2 input/collision, 3 dependency, 4 generation/I/O/layout,
5 failed content validation. Diagnostics omit input contents. No conversion or
native renderer is automatically invoked; rendered inspection is separate.
