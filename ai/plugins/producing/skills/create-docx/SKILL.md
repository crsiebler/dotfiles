---
name: create-docx
description: Create structured Word DOCX documents with explicit styles, tables, inline images, and page settings, then inspect their generated content and package structure.
---

# Create DOCX

Use for producing a new Word artifact. Establish audience, required content,
typography, image sources, and page layout from the request. For a simple existing
document read, use an adequate native reader; this skill does not provide general
Office editing or lossless round trips.

Read [authoring and CLI contract](references/authoring.md), then check
[requirements](references/requirements.md). Resolve `scripts/create_docx.py` from
this installed skill. Keep request files, images, outputs, and optional render
artifacts inside the active project; installed resources remain read-only.

```sh
python /loaded/create-docx/scripts/create_docx.py check
python /loaded/create-docx/scripts/create_docx.py --project /project create request.json report.docx
python /loaded/create-docx/scripts/create_docx.py --project /project inspect report.docx
```

Choose semantic heading levels and paragraph styles. Use real tables for tabular
content, explicit margins/page dimensions, aspect-preserving inline images, and
page/section breaks for deliberate structure. The helper uses the library's default
blank template; it does not edit or preserve an arbitrary supplied template.

Follow [validation](references/validation.md): reopen structure and content, then
render/inspect separately when needed and available. Font substitution, table flow,
and pagination depend on the recipient's renderer. Report exactly which checks
ran, and never call package validity visual approval. Deliver the project DOCX
path with any outstanding layout or font limitations.
