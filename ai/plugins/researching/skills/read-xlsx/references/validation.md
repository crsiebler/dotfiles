# Validation and reporting

Use source hash and worksheet/cell coordinates to tie claims to input bytes.
Review selected ranges, last emitted coordinates and truncation before conclusions.
Hidden sheets remain selected by default; hidden rows/column spans remain included
with explicit flags. Formula cache status reports presence only, never freshness.
Non-string formula objects (such as specialized array/data-table representations)
are explicitly marked formula_supported=false with a placeholder instead of a
misleading textual expression; inspect those separately when relevant.

Fixtures independently create literal IDs, formula-like strings, URLs, supplied
caches, a zero placeholder, hidden sheets/rows/grouped columns, then remove one
cache and falsify a worksheet dimension hint through ZIP/XML. Tests verify exact
coordinates, missing versus zero caches, hidden flags, bounds, partial rows,
invalid ranges/selections/packages, path/symlink controls, missing dependencies,
and unchanged sources/isolated installed resources. No creation-skill imports.

Metadata parsing checks actual stored cell coordinates. Formula/cache streams use
explicit bounds so incorrect dimension hints cannot silently hide in-range data.
No save, recalculation, external refresh, macro execution or renderer is involved.
Third-party parsing warnings fail with a sanitized diagnostic rather than leaking
workbook contents. Unsupported structures and visual omissions stay explicit.
