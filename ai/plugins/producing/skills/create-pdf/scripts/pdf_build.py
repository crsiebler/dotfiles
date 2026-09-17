"""Original literal-text paginated PDF production with explicit embedded font."""
import hashlib
import io
from xml.sax.saxutils import escape
from PIL import Image as RasterImage
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from pdf_support import DocumentError, fields, number, project_path, text


def sequence(value, low, high):
    if not isinstance(value, list) or not low <= len(value) <= high:
        raise DocumentError(2, 'input: invalid list size')
    return value


def build(request, root):
    fields(request, ('font', 'page', 'blocks'))
    page = request.get('page', {})
    fields(page, ('width', 'height', 'margin'))
    width = number(page.get('width', 8.5), 3, 30) * 72
    height = number(page.get('height', 11), 3, 30) * 72
    margin = number(page.get('margin', .75), .3, 3) * 72
    # Platypus frames include 6pt padding on each edge.
    usable_width, usable_height = width - 2*margin - 12, height - 2*margin - 12
    if min(usable_width, usable_height) < 36:
        raise DocumentError(2, 'input: unusable content frame')
    font_bytes = project_path(root, request.get('font')).read_bytes()
    name = 'ProjectFont' + hashlib.sha256(font_bytes).hexdigest()[:16]
    try:
        font = TTFont(name, io.BytesIO(font_bytes))
        pdfmetrics.registerFont(font)
    except Exception:
        raise DocumentError(2, 'input: expected usable TrueType font') from None
    required = 'Page 0123456789'
    if any(ord(c) not in font.face.charToGlyph for c in required):
        raise DocumentError(2, 'input: font lacks footer glyphs')
    expected, total = [], 0

    def paragraph(value, size=11, heading=False):
        nonlocal total
        value = text(value)
        total += len(value)
        if total > 200000:
            raise DocumentError(2, 'input: total text limit exceeded')
        if any(ord(c) not in font.face.charToGlyph for c in value if c not in '\n\r\t'):
            raise DocumentError(2, 'input: selected font lacks required glyphs')
        expected.append(value)
        style = ParagraphStyle('Project', fontName=name, fontSize=size, leading=size*1.35,
                               spaceAfter=8, keepWithNext=heading)
        literal = escape(value).replace('\r\n', '\n').replace('\r', '\n').replace('\n', '<br/>')
        return Paragraph(literal, style)

    story = []
    for block in sequence(request.get('blocks'), 1, 500):
        if not isinstance(block, dict):
            raise DocumentError(2, 'input: expected block object')
        kind = block.get('kind')
        if kind in ('heading', 'paragraph'):
            fields(block, ('kind', 'text', 'level') if kind == 'heading' else ('kind', 'text', 'size'))
            if kind == 'heading':
                level = block.get('level', 1)
                if type(level) is not int or not 1 <= level <= 3:
                    raise DocumentError(2, 'input: invalid heading level')
                size = {1:22, 2:17, 3:14}[level]
            else:
                size = number(block.get('size', 11), 8, 24)
            story.append(paragraph(block.get('text'), size, kind == 'heading'))
        elif kind == 'table':
            fields(block, ('kind', 'rows', 'widths'))
            rows = sequence(block.get('rows'), 1, 100)
            columns = len(sequence(rows[0], 1, 12))
            widths = block.get('widths')
            if widths is None:
                widths = [usable_width / columns] * columns
            else:
                widths = [number(v, .25, 30)*72 for v in sequence(widths, columns, columns)]
                if sum(widths) > usable_width:
                    raise DocumentError(2, 'input: table exceeds frame width')
            data = [[paragraph(value, 10) for value in sequence(row, columns, columns)] for row in rows]
            table = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E8EEF4')),
                                       ('GRID',(0,0),(-1,-1),.5,colors.HexColor('#8996A3')),
                                       ('VALIGN',(0,0),(-1,-1),'TOP')]))
            story.extend((table, Spacer(1, 10)))
        elif kind == 'image':
            fields(block, ('kind', 'path', 'width'))
            content = project_path(root, block.get('path')).read_bytes()
            try:
                with RasterImage.open(io.BytesIO(content)) as image:
                    if image.format not in ('PNG', 'JPEG') or image.width*image.height > 25000000:
                        raise ValueError('unsupported image')
                    iw, ih = image.size
                    image.verify()
            except Exception:
                raise DocumentError(2, 'input: expected valid bounded PNG/JPEG image') from None
            image_width = number(block.get('width'), .1, 30)*72
            image_height = image_width*ih/iw
            if image_width > usable_width or image_height > usable_height:
                raise DocumentError(2, 'input: image exceeds content frame')
            story.extend((Image(io.BytesIO(content), width=image_width, height=image_height), Spacer(1,10)))
        elif kind == 'page_break':
            fields(block, ('kind',))
            story.append(PageBreak())
        else:
            raise DocumentError(2, 'input: unsupported block kind')
    stream = io.BytesIO()
    document = SimpleDocTemplate(stream, pagesize=(width, height), leftMargin=margin,
                                 rightMargin=margin, topMargin=margin, bottomMargin=margin)
    def footer(canvas, document):
        if document.page > 100:
            raise DocumentError(4, 'generation: page limit exceeded')
        canvas.saveState()
        canvas.setFont(name, 9)
        canvas.drawCentredString(width/2, margin/2, f'Page {document.page}')
        canvas.restoreState()
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    return stream.getvalue(), expected, (width, height)
