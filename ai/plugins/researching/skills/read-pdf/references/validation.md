# Validation and interpretation

Check source hash and selected page numbers. Cite page-N locations; text order is
not guaranteed visual order. Compare page extracted_characters, excerpt length,
truncated and missing_text to distinguish sparse input from exhausted output budget.
Metadata excerpts share the remaining character budget after page text.

Fixtures independently generate four pages: text, image-only, more text, and blank.
Tests verify exact selection, source/metadata/geometry, missing-text and possible-scan
flags for image-only and blank pages, preserved bytes, truncation, malformed PDF
sanitized errors, invalid selections, missing dependencies, project/symlink controls,
and unchanged isolated resources. They do not invoke the creation skill.

possible_scan is true for fewer than24 nonwhitespace characters, which includes
blank and sparse/vector-only pages. It requests further relevant inspection and is
not a diagnosis. No OCR, table reconstruction, XMP metadata recovery, annotation/
form/attachment interpretation or rendering is performed. A page without extracted
text may still convey substantial information. Encrypted PDFs are rejected without
password handling. Source bytes are never written, including when parsing fails.
