# Validation

Check literal text, font availability/glyph coverage, page frame, table shape and
image size before build. Build entirely in memory, reopen using pypdf, verify page
count bounds, geometry, page-number text and requested text after whitespace
normalization. Missing text or layout failure prevents publication. Paragraph
wrapping normalizes whitespace; this is not byte-identical text layout or tagged
semantic structure. Sources and existing outputs remain unchanged.

Tests independently inspect PDF page geometry, text, embedded TrueType resources,
image count, explicit page breaks, flowing tables with repeated headers, and page
numbers. They cover literal XML characters, accented glyphs, missing font/glyphs,
oversized unsplittable rows/images, invalid page geometry, collisions, path/symlink
restrictions, missing packages, and exact documentation recipe in an isolated bundle.

Reopened extraction and font cmap checks do not prove shaping, visual glyph quality,
clipping, or page aesthetics. Render and inspect every page when tools are available:

```sh
pdftoppm -scale-to 1200 -png /project/report.pdf /project/render/page
```

Use an existing project-local render directory. Verify actual output images, then
inspect text hierarchy, page/footer separation, table breaks/repeated headers,
image aspect, whitespace, clipping and glyphs. Keep source PDF intact. No helper
starts conversion or rendering automatically. Report unavailable/failed rendering
separately from content/geometry checks; never claim universal viewer equivalence.
