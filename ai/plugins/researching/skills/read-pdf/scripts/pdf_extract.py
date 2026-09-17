"""Page-located text evidence with explicit sparse/scan heuristics, without OCR."""
import io
import re
from pypdf import PdfReader
from pdf_input import ReadError


def selection(value, count):
    if value is None:
        return list(range(1, min(count,100)+1)), count > 100
    if len(value) > 1000:
        raise ReadError(2, 'input: page selection too long')
    selected = set()
    for part in value.split(','):
        if not re.fullmatch(r'[0-9]+(?:-[0-9]+)?', part):
            raise ReadError(2, 'input: expected page numbers or inclusive ranges')
        ends = [int(v) for v in part.split('-')]
        first, last = ends[0], ends[-1]
        if not 1 <= first <= last <= count or last-first >= 100:
            raise ReadError(2, 'input: page selection out of range or too large')
        selected.update(range(first,last+1))
        if len(selected) > 100:
            raise ReadError(2, 'input: select at most 100 pages')
    return sorted(selected), False


def extract(content, selected, max_chars):
    reader = PdfReader(io.BytesIO(content), strict=True)
    if reader.is_encrypted:
        raise ReadError(2, 'input: encrypted PDFs unsupported')
    if not 1 <= len(reader.pages) <= 2000:
        raise ReadError(2, 'input: PDF page count outside limits')
    numbers, truncated = selection(selected, len(reader.pages))
    remaining, total = max_chars, 0
    pages = []
    for number in numbers:
        page = reader.pages[number-1]
        stream = page.get_contents()
        size = len(stream.get_data()) if stream else 0
        total += size
        if size > 8*1024*1024 or total > 32*1024*1024:
            raise ReadError(2, 'input: selected content stream limit exceeded')
        text = page.extract_text() or ''
        excerpt = text[:remaining]
        remaining -= len(excerpt)
        page_truncated = len(excerpt) < len(text)
        truncated |= page_truncated
        sparse = len(''.join(text.split())) < 24
        pages.append(dict(page=number, location=f'page-{number}', width=float(page.mediabox.width),
                          height=float(page.mediabox.height), rotation=page.rotation,
                          text=excerpt, extracted_characters=len(text), truncated=page_truncated,
                          missing_text=not bool(text.strip()), insufficient_text=sparse, possible_scan=sparse))
    metadata = {}
    info = reader.metadata
    for key in ('title','author','subject','creator','producer','creation_date','modification_date'):
        value = getattr(info, key, None) if info else None
        if value is None:
            continue
        value = value.isoformat() if hasattr(value, 'isoformat') else str(value)
        excerpt = value[:remaining]
        remaining -= len(excerpt)
        truncated |= len(excerpt) < len(value)
        metadata[key] = excerpt
    return dict(page_count=len(reader.pages), selected_pages=numbers, pages=pages, metadata=metadata,
                truncated=bool(truncated), limitations=[
                    'Possible-scan is a sparse-text heuristic; blank/vector-only pages can trigger it.',
                    'Empty extraction does not establish an empty page; inspect visual evidence.',
                    'No OCR, table reconstruction, images, annotations, forms or layout interpretation.',
                    'Metadata excludes XMP streams; unselected pages are not inspected.',
                    'Text order may differ from visual reading order; source is never saved.'])
