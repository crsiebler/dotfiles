# PPTX extraction contract

```sh
python /loaded/read-pptx/scripts/read_pptx.py check
python /loaded/read-pptx/scripts/read_pptx.py --project /project read deck.pptx --slides 1,3-5 --max-records 500 --max-chars 50000 --max-values 10000
```

The reader emits JSON to stdout, never saves or converts the source, and has no
creation-skill dependency. Paths must be regular nonsymlink project files; project
and ancestors cannot be symlinks. Input <=16 MiB, ZIP <=2000 members/64 MiB expanded.
Exit codes: 0 extraction, 2 invalid input, 3 missing dependency, 4 parse/I/O failure.
Diagnostics omit document contents.

`--slides` is a comma-separated list of one-based slide numbers or inclusive ranges,
selected in document order with duplicates collapsed. Reject malformed/out-of-range
selection and more than 100 selected slides. Without selection, inspect the first
100 slides and mark truncation when more exist. No selected slide implies anything
about unselected slides. Source-relative path, SHA-256, slide count and selected
slide numbers accompany every result.

Records carry `kind`, `slide`, and `location`, such as `slide-2/shape-3` or
`slide-2/shape-3/group/shape-1`. Shape indices follow stored shape order, not visual
reading order. Text frames carry text; tables carry row/column coordinates (merged
positions retain library grid semantics); supported native category charts carry
categories and named numeric series; notes carry speaker-note text at `slide-N/notes`.
Notes are accessed only when already present. Group shapes recurse to depth 10;
missing/unsupported content is reported, never reconstructed.

Supported charts are single-plot, flat category charts with numeric series.
Scatter/bubble, multi-plot and hierarchical-category charts are reported unsupported.
Values are stored chart caches, not a recalculation or external-data refresh.
Tables/caches/notes/text are extracted without executing embedded content.

Global limits: max-records 1–2000, max-chars 1–200000 (all extracted strings),
max-values 1–20000 (table cells, categories, series and numeric values). Defaults
shown above. Limits span all selected slides and notes; exhaustion sets `truncated`.
A bounded `unsupported` list identifies selected-slide pictures/visual-only shapes,
groups beyond depth, unsupported charts, notes without a text placeholder and
nontext shapes. Layout/master content, comments, formatting, animations, hyperlink
targets and visual reading order are not reconstructed; these limitations are always
reported. Empty text cannot establish empty visual content. No OCR is provided.
