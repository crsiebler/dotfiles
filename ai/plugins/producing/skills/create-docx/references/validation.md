# Validation

Creation writes to memory, reopens the ZIP and Word document, and compares ordered
paragraph text/style names, tables/cells, inline image count, section dimensions/
margins, custom font properties, and explicit page-break count. Package limits,
CRC validity, duplicate member names, and encryption are checked before inspection.
Publication refuses collisions. Failures leave source requests/images untouched.

`inspect` bounds excerpts and reports truncation. It verifies package structure,
not arbitrary Word features, tracked changes, page count, or visual appearance.
For content research use a reader workflow suited to the request.

Tests independently inspect XML and image relationships rather than relying only
on helper success. Fixtures exercise Unicode/literal XML characters, custom styles,
tables, image bytes, page settings, section breaks, missing dependencies, malformed
input, unavailable/invalid images, path/symlink/collision boundaries, truncation,
and execution from an isolated skill copy. The complete JSON recipe in authoring.md
is also executed in regression tests.

For a user-facing artifact, inspect rendered pages when a suitable authorized
renderer is available: check clipping, whitespace, heading hierarchy, table breaks,
image placement, page transitions, and glyphs. Keep a project-local render copy
and preserve the DOCX. No helper invokes conversion automatically. If rendering is
not performed, report structural checks and the unverified pagination/font/layout
limitations separately. This implementation's fixture tests establish structure
and content; no visual-pagination approval is claimed.
