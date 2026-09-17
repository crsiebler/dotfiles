---
name: create-pdf
description: Create paginated PDFs with explicit embedded fonts, literal text, headings, tables, images, and page numbers, then independently validate content and inspect rendered pages.
---

# Create PDF

Use for a new fixed-layout document. Establish audience, content, page format,
image sources and licensed font choice. Prefer an adequate native reader for
simple existing PDF reads. This skill does not edit arbitrary PDFs, fill forms,
perform OCR or promise accessible tagged PDF output.

Read [authoring](references/authoring.md), [requirements](references/requirements.md),
and [validation](references/validation.md). Resolve scripts/create_pdf.py from
this installed skill; keep requests, licensed fonts, images, outputs and render
artifacts in the project. Installed resources remain read-only.

```sh
python /loaded/create-pdf/scripts/create_pdf.py check
python /loaded/create-pdf/scripts/create_pdf.py --project /project create request.json report.pdf
python /loaded/create-pdf/scripts/create_pdf.py --project /project inspect report.pdf
```

Use readable hierarchy, deliberate margins, restrained density and tables for
actual tabular content. All text is escaped, not interpreted as input markup.
Missing glyphs and oversized unsplittable content stop publication. A glyph map
is not proof of correct shaping or typography.

Reopen and inspect content/geometry, then render every page when a suitable tool
is available. Check table/page transitions, clipping, glyphs, whitespace and image
placement. Report exactly which checks ran and any layout/font gaps; structural
validity alone is not visual approval. Deliver the project-local PDF path.
