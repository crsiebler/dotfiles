---
name: create-pptx
description: Create editable PowerPoint presentations with inspected layouts, explicit geometry, text, images, tables, and native charts, then validate their package content and rendered slides.
---

# Create PPTX

Use to produce a new presentation. Establish audience, narrative, content, brand
constraints, and slide format. Prefer an adequate native reader for simple existing
file reads; this workflow does not edit or round-trip arbitrary Office templates.

Read the [authoring contract](references/authoring.md) and
[requirements](references/requirements.md). Resolve scripts/create_pptx.py from
this installed skill. Run `check`, then `layouts` before selecting named layouts
and text placeholder indices. Keep requests, assets, output, and render artifacts
inside the active project; installed resources remain read-only.

Choose a coherent hierarchy, restrained text density, readable chart labels,
consistent spacing, and deliberate image crops (this helper uses proportional fit).
Editable elements do not guarantee text fit. Use explicit text boxes when the
blank template's inherited placeholder geometry does not suit the chosen format.

Run [validation](references/validation.md) after creation. Reopening verifies
supported content and geometry; inspect rendered slides when a suitable renderer
is available. Report actual checks, font substitution and layout limitations,
and the final project-local PPTX path. Never call package checks visual approval.
