"""Validate typed workbook input before calling the writer."""
from datetime import date
import re
from xlsx_support import DocumentError, fields, number, text


def seq(value, low, high):
    if not isinstance(value, list) or not low <= len(value) <= high:
        raise DocumentError(2, 'input: invalid list size')
    return value


def integer(value, low, high):
    if type(value) is not int or not low <= value <= high:
        raise DocumentError(2, 'input: invalid index')
    return value


def validate(request):
    fields(request, ('formats', 'sheets'))
    formats = request.get('formats', {})
    if not isinstance(formats, dict) or len(formats) > 100:
        raise DocumentError(2, 'input: invalid formats')
    for name, spec in formats.items():
        text(name, 100)
        fields(spec, ('num_format', 'bold', 'font_color', 'bg_color', 'text_wrap'))
        for key, value in spec.items():
            if key in ('bold', 'text_wrap'):
                if type(value) is not bool:
                    raise DocumentError(2, 'input: format flag must be boolean')
            elif key.endswith('color'):
                if not isinstance(value, str) or not re.fullmatch('#[0-9a-fA-F]{6}', value):
                    raise DocumentError(2, 'input: invalid format color')
            else:
                text(value, 200)
    names, count = set(), 0
    for sheet in seq(request.get('sheets'), 1, 20):
        fields(sheet, ('name', 'rows', 'widths', 'freeze', 'table', 'filter', 'charts'))
        name = text(sheet.get('name'), 31)
        if (not name or re.search(r'[\[\]:*?/\\]', name) or name.startswith("'")
                or name.endswith("'") or name.lower() in names or name.lower() == 'history'):
            raise DocumentError(2, 'input: invalid or duplicate worksheet name')
        names.add(name.lower())
        rows = seq(sheet.get('rows'), 1, 1000)
        width = len(seq(rows[0], 1, 100))
        count += len(rows) * width
        if count > 20000:
            raise DocumentError(2, 'input: workbook exceeds 20000 cells')
        for row in rows:
            for cell in seq(row, width, width):
                validate_cell(cell, formats)
        if 'widths' in sheet:
            for value in seq(sheet['widths'], width, width):
                number(value, 1, 100)
        if 'freeze' in sheet:
            split = seq(sheet['freeze'], 2, 2)
            integer(split[0], 0, 1048575); integer(split[1], 0, 16383)
        for flag in ('table', 'filter'):
            if type(sheet.get(flag, False)) is not bool:
                raise DocumentError(2, 'input: table/filter must be boolean')
        if sheet.get('table') and sheet.get('filter'):
            raise DocumentError(2, 'input: table and standalone filter conflict')
        if sheet.get('table'):
            headers = [cell.get('value') for cell in rows[0]]
            if (len(rows) < 2 or any(c['type'] != 'string' for c in rows[0])
                    or any(not h or len(h) > 255 for h in headers)
                    or len({h.lower() for h in headers}) != width):
                raise DocumentError(2, 'input: tables need unique string headers and a data row')
        for chart in seq(sheet.get('charts', []), 0, 10):
            fields(chart, ('at', 'category_column', 'value_columns', 'title'))
            anchor = seq(chart.get('at'), 2, 2)
            integer(anchor[0], 0, 1048575); integer(anchor[1], 0, 16383)
            category = integer(chart.get('category_column'), 0, width - 1)
            columns = seq(chart.get('value_columns'), 1, 10)
            if len(rows) < 2:
                raise DocumentError(2, 'input: chart requires data rows')
            for column in columns:
                integer(column, 0, width - 1)
                if rows[0][column]['type'] != 'string' or any(r[column]['type'] not in ('number', 'formula') for r in rows[1:]):
                    raise DocumentError(2, 'input: chart values need string heading and numeric/formula cells')
            if any(r[category]['type'] not in ('string', 'number') for r in rows[1:]):
                raise DocumentError(2, 'input: chart categories must be strings/numbers')
            text(chart.get('title', ''), 200)
    return request


def validate_cell(cell, formats):
    fields(cell, ('type', 'value', 'format', 'cached'))
    kind = cell.get('type')
    fmt = cell.get('format')
    if fmt is not None and (not isinstance(fmt, str) or fmt not in formats):
        raise DocumentError(2, 'input: unknown format')
    if 'cached' in cell and kind != 'formula':
        raise DocumentError(2, 'input: only formulas have caches')
    value = cell.get('value')
    if kind == 'string':
        text(value, 32767)
    elif kind == 'number':
        number(value, -1e300, 1e300)
    elif kind == 'boolean':
        if type(value) is not bool:
            raise DocumentError(2, 'input: boolean cell requires boolean')
    elif kind == 'date':
        try:
            if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value) or date.fromisoformat(value) < date(1900, 1, 1):
                raise ValueError('invalid')
        except ValueError:
            raise DocumentError(2, 'input: date requires ISO date from 1900 onward') from None
    elif kind == 'formula':
        value = text(value, 8192)
        if not value.startswith('=') or len(value) < 2:
            raise DocumentError(2, 'input: formula requires leading equals and expression')
        number(cell.get('cached', 0), -1e300, 1e300)
    elif kind == 'blank':
        if 'value' in cell:
            raise DocumentError(2, 'input: blank cells have no value')
    else:
        raise DocumentError(2, 'input: unsupported cell type')
