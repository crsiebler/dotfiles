# DOCX extraction contract

`python /loaded/read-docx/scripts/read_docx.py check` reports prerequisites.
`python /loaded/read-docx/scripts/read_docx.py --project ROOT read INPUT.docx
--max-records 500 --max-chars 50000 --max-cells 1000` emits one bounded JSON object
to stdout. The read operation has no output-file option and never saves the input.
All paths must be existing nonsymlink files inside ROOT; relative paths resolve
from ROOT, independently of the working directory. ROOT must exist without symlink
ancestors. Input limit: 16 MiB; expanded ZIP: 64 MiB and 1000 members.

Output includes source-relative path and SHA-256, ordered `records`, header/footer
`contexts`, `unsupported` counts, `truncated`, and limitations. Supported body blocks
are visited in their paragraph/table document order via iter_inner_content. Locations
such as `body/block-2` use a one-based supported-block ordinal, not rendered pages.
Paragraph records carry text, paragraph style, and inherited heading level where
recognizable. Tables carry row/cell coordinates and text; merged grid positions may
repeat the same cell. Column numbers include omitted leading grid positions;
missing positions have no invented cell or text. Nested tables are omitted and counted, never silently flattened.

Header/footer contexts distinguish section number, default/first/even variant,
enabled status, linked-to-previous status, and the section defining inherited content.
Disabled but defined variants are included as stored content, clearly marked. Absent
inherited definitions stay absent; reading does not create or unlink definitions.
At most 100 sections are inspected, with truncation reported if more exist.

Global limits apply across body and header/footer records. max-records: 1–2000;
max-chars: 1–200000 (text/style excerpts); max-cells: 1–10000. Exhaustion reports
truncation; an incomplete extraction cannot establish that omitted content is absent.
Unsupported counts include tracked revisions, text boxes, nested tables, content
controls, foot/endnote references, comments, drawings, embedded objects, fields,
hyperlink targets, and unknown top-level body blocks. Their content is not accepted,
executed, rendered, or reconstructed. Counts describe stored structures, not pages.

Examples:

```sh
python /loaded/read-docx/scripts/read_docx.py --project /project read report.docx
python /loaded/read-docx/scripts/read_docx.py --project /project read report.docx --max-records 20 --max-chars 4000
```

Exit codes: 0 successful bounded extraction, 2 invalid input/path/package/limits,
3 missing dependency, 4 other parse/I/O failure. Errors omit document contents.
No model, native role, creation-skill import, renderer, converter, OCR, or automatic
package installation is used. Native readers remain appropriate for simple reads.
