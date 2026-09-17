# PDF extraction contract

```sh
python /loaded/read-pdf/scripts/read_pdf.py check
python /loaded/read-pdf/scripts/read_pdf.py --project /project read report.pdf --pages 1,3-5 --max-chars 50000
```

Emit JSON to stdout; no output-file option, save, OCR, conversion or creation-skill
import. `--pages` accepts one-based numbers/inclusive ranges, collapses duplicates,
and visits document order. Reject malformed, reversed, out-of-range or >100-page
selections. Default first100 pages with truncation when more exist. Source PDF may
contain up to2000 pages. File <=16 MiB; page content streams <=8 MiB and selected
streams total <=32 MiB before extraction. Decompression itself still requires memory.

Global max-chars1–200000 (default50000) bounds text/metadata excerpts. Page text gets
priority; metadata follows. Reports source-relative path/SHA-256, total and selected
page numbers, page-N locations, page geometry/rotation, extracted text, full extracted
character count, page truncation, missing_text and insufficient_text. Fewer than24
nonwhitespace characters triggers insufficient_text and possible_scan: a heuristic
which can also flag blank/sparse/vector-only pages, never proof of a scan. No text
is not proof of no information. Pages whose excerpts hit limits remain distinguished
from pages with no extractable text at all.

Metadata includes bounded title/author/subject/creator/producer/creation/modification
date values from the document information dictionary, not arbitrary XMP streams.
Extraction cannot reconstruct table semantics, visual reading order, images,
annotations, forms, attachments, signatures or layout. No pdfplumber dependency or
OCR/table-reconstruction promise. Consult visual evidence when extraction is insufficient.

All paths must be nonsymlink project-local regular files with existing project root;
source bytes and installed resources are unchanged. Encrypted PDFs are rejected;
no password collection or decryption. Exit0 bounded extraction,2 invalid input/path/
limits/encryption,3 missing dependency,4 parse/I/O failure. Diagnostics omit content.
