#!/usr/bin/env python3
"""Create typed workbooks with explicit formula caches and independent verification."""
import argparse
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
from xlsx_support import DocumentError, inspect_package, no_links, project_path, publish


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path)
    commands = parser.add_subparsers(dest='action', required=True)
    commands.add_parser('check')
    create = commands.add_parser('create')
    create.add_argument('request'); create.add_argument('output')
    commands.add_parser('inspect').add_argument('input')
    args = parser.parse_args()
    try:
        try:
            import xlsxwriter
            import openpyxl
        except ImportError:
            raise DocumentError(3, 'dependency: XlsxWriter and openpyxl required; see references/requirements.md') from None
        if sys.version_info < (3, 11):
            raise DocumentError(3, 'dependency: Python 3.11+ required')
        if args.action == 'check':
            print(json.dumps({'python': sys.version.split()[0], 'XlsxWriter': xlsxwriter.__version__, 'openpyxl': openpyxl.__version__}))
            return 0
        if args.project is None:
            raise DocumentError(2, 'input: --project required')
        no_links(args.project.absolute())
        root = args.project.resolve()
        if not root.is_dir():
            raise DocumentError(2, 'input: project directory must exist')
        from xlsx_inspect import inspect, verify
        if args.action == 'inspect':
            content = project_path(root, args.input).read_bytes()
            inspect_package(content)
            result = inspect(content)
        else:
            output = project_path(root, args.output, output=True)
            try:
                request = json.loads(project_path(root, args.request).read_text())
            except (ValueError, UnicodeError):
                raise DocumentError(2, 'input: invalid request JSON') from None
            from xlsx_contract import validate
            from xlsx_build import build
            validate(request)
            content, formulas = build(request)
            inspect_package(content)
            verify(content, request)
            publish(output, content)
            result = dict(output=output.relative_to(root).as_posix(), formulas=formulas,
                          recalculated=False, structural_validation='passed')
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return 0
    except DocumentError as error:
        print(str(error), file=sys.stderr)
        return error.code
    except Exception:
        print('writer: unable to process workbook; check request, package and file access', file=sys.stderr)
        return 4


if __name__ == '__main__':
    sys.exit(main())
