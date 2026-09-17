"""Read stored bounds and hidden spans without depending on dimension hints."""
import io
import posixpath
import re
import zipfile
from xml.etree import ElementTree as ET
from openpyxl.utils.cell import range_boundaries
from xlsx_input import ReadError

NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
REL = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'


def bounds(value):
    if not isinstance(value, str) or not re.fullmatch(r'\$?[A-Za-z]{1,3}\$?[1-9][0-9]*(?::\$?[A-Za-z]{1,3}\$?[1-9][0-9]*)?', value):
        raise ReadError(2, 'input: expected a finite A1 cell range')
    left, top, right, bottom = range_boundaries(value.upper())
    if not 1 <= left <= right <= 16384 or not 1 <= top <= bottom <= 1048576:
        raise ReadError(2, 'input: range exceeds worksheet bounds or is reversed')
    return left, top, right, bottom


def metadata(content, names):
    result, count, definitions = {}, 0, 0
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        workbook = ET.fromstring(archive.read('xl/workbook.xml'))
        relationships = ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))
        targets = {r.get('Id'): r for r in relationships}
        for sheet in workbook.findall('s:sheets/s:sheet', NS):
            name = sheet.get('name')
            if name not in names:
                continue
            relation = targets[sheet.get(REL)]
            if relation.get('TargetMode') == 'External':
                raise ReadError(2, 'input: external worksheet targets unsupported')
            target = relation.get('Target')
            path = posixpath.normpath(target.lstrip('/') if target.startswith('/') else 'xl/' + target)
            if not path.startswith('xl/'):
                raise ReadError(2, 'input: worksheet target outside package namespace')
            xml = ET.fromstring(archive.read(path))
            hidden_rows, hidden_columns = set(), []
            max_row, max_column = 1, 1
            for row in xml.findall('s:sheetData/s:row', NS):
                definitions += 1
                if definitions > 100000:
                    raise ReadError(2, 'input: worksheet metadata limit exceeded')
                if row.get('hidden') in ('1', 'true'):
                    hidden_rows.add(int(row.get('r')))
                for cell in row.findall('s:c', NS):
                    count += 1
                    if count > 100000:
                        raise ReadError(2, 'input: stored cell limit exceeded')
                    left, top, right, bottom = bounds(cell.get('r'))
                    max_row, max_column = max(max_row, bottom), max(max_column, right)
            for column in xml.findall('s:cols/s:col', NS):
                definitions += 1
                if definitions > 100000:
                    raise ReadError(2, 'input: worksheet metadata limit exceeded')
                if column.get('hidden') in ('1', 'true'):
                    hidden_columns.append((int(column.get('min')), int(column.get('max'))))
            result[name] = dict(max_row=max_row, max_column=max_column,
                                hidden_rows=hidden_rows, hidden_columns=hidden_columns)
    return result
