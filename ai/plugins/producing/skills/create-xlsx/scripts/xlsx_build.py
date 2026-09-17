"""Explicit typed writers; never infer a formula, number, or URL from a string."""
from datetime import date
import io
import warnings
import xlsxwriter
from xlsx_support import DocumentError


def checked(result):
    if result not in (None, 0):
        raise DocumentError(4, 'writer: operation failed or truncated content')


def build(request):
    stream = io.BytesIO()
    formulas = []
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        workbook = xlsxwriter.Workbook(stream, {'in_memory': True, 'strings_to_formulas': False,
                                               'strings_to_urls': False, 'strings_to_numbers': False})
        formats = {name: workbook.add_format(value) for name, value in request.get('formats', {}).items()}
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
        workbook.set_calc_mode('auto')
        for sheet in request['sheets']:
            page = workbook.add_worksheet(sheet['name'])
            rows = sheet['rows']
            if sheet.get('table'):
                checked(page.add_table(0, 0, len(rows)-1, len(rows[0])-1,
                                       {'columns': [{'header': c['value']} for c in rows[0]]}))
            for r, row in enumerate(rows):
                for c, cell in enumerate(row):
                    kind, value = cell['type'], cell.get('value')
                    fmt = formats.get(cell.get('format'))
                    if kind == 'string':
                        result = page.write_string(r, c, value, fmt)
                    elif kind == 'number':
                        result = page.write_number(r, c, value, fmt)
                    elif kind == 'boolean':
                        result = page.write_boolean(r, c, value, fmt)
                    elif kind == 'date':
                        result = page.write_datetime(r, c, date.fromisoformat(value), fmt or date_format)
                    elif kind == 'blank':
                        result = page.write_blank(r, c, None, fmt)
                    else:
                        result = page.write_formula(r, c, value, fmt, cell.get('cached', 0))
                        formulas.append(dict(sheet=sheet['name'], row=r+1, column=c+1,
                                             cache_source='supplied' if 'cached' in cell else 'writer_placeholder'))
                    checked(result)
            for column, width in enumerate(sheet.get('widths', [])):
                checked(page.set_column(column, column, width))
            if 'freeze' in sheet:
                page.freeze_panes(*sheet['freeze'])
            if sheet.get('filter'):
                checked(page.autofilter(0, 0, len(rows)-1, len(rows[0])-1))
            for spec in sheet.get('charts', []):
                chart = workbook.add_chart({'type': 'column'})
                for column in spec['value_columns']:
                    chart.add_series({'name': [sheet['name'], 0, column],
                                      'categories': [sheet['name'], 1, spec['category_column'], len(rows)-1, spec['category_column']],
                                      'values': [sheet['name'], 1, column, len(rows)-1, column]})
                if spec.get('title'):
                    chart.set_title({'name': spec['title']})
                checked(page.insert_chart(*spec['at'], chart))
        workbook.close()
    return stream.getvalue(), formulas
