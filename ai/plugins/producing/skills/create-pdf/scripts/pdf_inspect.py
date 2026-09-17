"""Independent pypdf geometry/content verification with bounded inspection."""
import io
import math
import re
from pypdf import PdfReader
from pdf_support import DocumentError, MAX_FILE


def read_pages(content):
    if len(content) > MAX_FILE or not content.startswith(b'%PDF-'):
        raise DocumentError(2, 'input: expected PDF of at most 16 MiB')
    reader = PdfReader(io.BytesIO(content), strict=True)
    if reader.is_encrypted or not 1 <= len(reader.pages) <= 100:
        raise DocumentError(2, 'input: encrypted PDF or page limit exceeded')
    pages, total = [], 0
    for index, page in enumerate(reader.pages, 1):
        stream = page.get_contents()
        size = len(stream.get_data()) if stream else 0
        total += size
        if size > 8*1024*1024 or total > 32*1024*1024:
            raise DocumentError(2, 'input: PDF content stream limit exceeded')
        pages.append(dict(page=index, width=float(page.mediabox.width), height=float(page.mediabox.height),
                          text=page.extract_text() or ''))
    return pages


def verify(pages, expected, dimensions):
    for page in pages:
        if not all(math.isclose(page[key], value, abs_tol=.01) for key,value in zip(('width','height'),dimensions)):
            raise DocumentError(5, 'validation: page geometry differs')
        if f"Page {page['page']}" not in page['text']:
            raise DocumentError(5, 'validation: page number missing')
    # Remove only the known first line footer emitted by our page callback.
    text = '\n'.join(re.sub(r'^Page \d+\s*\n', '', p['text'], count=1) for p in pages)
    normalized = ''.join(text.split())
    for value in expected:
        if ''.join(value.split()) not in normalized:
            raise DocumentError(5, 'validation: expected text missing from extraction')


def inspect(pages):
    remaining, truncated = 50000, False
    result = []
    for page in pages:
        excerpt = page['text'][:remaining]
        remaining -= len(excerpt)
        truncated |= len(excerpt) < len(page['text'])
        result.append(dict(page, text=excerpt))
    return dict(page_count=len(pages), pages=result, truncated=truncated, rendered=False)
