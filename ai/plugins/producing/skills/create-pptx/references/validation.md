# Validation

Creation saves to memory, validates ZIP structure, reopens with python-pptx, and
compares supported text, tables, chart categories/series, images and shape/slide
geometry. Publication requires a fresh project-local path. Inspection bounds text
and cell/chart values and reports truncation. These checks do not validate arbitrary
PowerPoint features, animation, macros, accessibility, or rendering fidelity.

Regression tests independently inspect package XML, embedded chart workbook
presence, exact chart data, text, slide count/dimensions and proportional image
geometry. They exercise layout inventory, placeholder selection, invalid geometry,
chart/table inputs, collisions, dependency absence, isolated installed resources,
path/symlink boundaries, and the exact authoring JSON recipe.

Text wrap does not guarantee text fits its box; the helper does not measure font
metrics or automatically shrink text. Table rows, chart legends/labels and template
placeholders can overflow or overlap. Inherited placeholder geometry comes from
the blank template and is not automatically redesigned for a different slide size.

When a renderer is available, render a project-local copy and inspect every slide
for clipping, overlap, readability, glyphs, image aspect ratio, chart labels and
consistent hierarchy. Use a project-local application profile and output directory;
never modify global settings. For example, with already available LibreOffice:

```sh
soffice -env:UserInstallation=file:///project/render-profile --headless --convert-to pdf --outdir /project/render /project/deck.pptx
pdftoppm -scale-to 1200 -png /project/render/deck.pdf /project/render/slide
```

Create the project directories first. Rendering is a separate explicit verification
step; no helper starts conversion. Inspect its exit status and actual files. A
successful renderer exit alone is not visual approval. If unavailable or unsuccessful,
report the exact gap and structural evidence instead. LibreOffice and PowerPoint
may differ in font substitution and layout, so one renderer does not certify all.
