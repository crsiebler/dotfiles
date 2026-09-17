#!/usr/bin/env python3
"""Extract bounded workbook evidence without saving or calculating formulas."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import warnings
sys.dont_write_bytecode = True
from xlsx_input import ReadError, load_source, no_links


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path)
    commands = parser.add_subparsers(dest='action', required=True)
    commands.add_parser('check')
    read = commands.add_parser('read')
    read.add_argument('input')
    read.add_argument('--sheet', action='append')
    read.add_argument('--range', dest='region')
    read.add_argument('--max-cells', type=int, default=2000)
    read.add_argument('--max-chars', type=int, default=50000)
    args = parser.parse_args()
    try:
        try:
            import openpyxl
        except ImportError:
            raise ReadError(3, 'dependency: openpyxl required; see references/requirements.md') from None
        if sys.version_info < (3, 11):
            raise ReadError(3, 'dependency: Python 3.11+ required')
        if args.action == 'check':
            print(json.dumps({'python': sys.version.split()[0], 'openpyxl': openpyxl.__version__}))
            return 0
        if args.project is None or not 1 <= args.max_cells <= 20000 or not 1 <= args.max_chars <= 200000:
            raise ReadError(2, 'input: project required and extraction limits must be valid')
        no_links(args.project.absolute())
        root = args.project.resolve()
        if not root.is_dir():
            raise ReadError(2, 'input: project directory must exist')
        source, content = load_source(root, args.input)
        from xlsx_extract import extract
        with warnings.catch_warnings():
            # Third-party warnings can contain document data; fail with sanitized error.
            warnings.simplefilter('error')
            result = extract(content, args.sheet, args.region, args.max_cells, args.max_chars)
        result.update(source=source.relative_to(root).as_posix(), sha256=hashlib.sha256(content).hexdigest())
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return 0
    except ReadError as error:
        print(str(error), file=sys.stderr)
        return error.code
    except Exception:
        print('parse: unable to read workbook; check package structure and file access', file=sys.stderr)
        return 4


if __name__ == '__main__':
    sys.exit(main())
