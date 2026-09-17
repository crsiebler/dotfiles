#!/usr/bin/env python3
"""Read bounded slide-located PPTX evidence without modifying the source."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
from pptx_input import ReadError, load_source, no_links


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path)
    commands = parser.add_subparsers(dest='action', required=True)
    commands.add_parser('check')
    read = commands.add_parser('read')
    read.add_argument('input')
    read.add_argument('--slides')
    read.add_argument('--max-records', type=int, default=500)
    read.add_argument('--max-chars', type=int, default=50000)
    read.add_argument('--max-values', type=int, default=10000)
    args = parser.parse_args()
    try:
        try:
            import pptx
        except ImportError:
            raise ReadError(3, 'dependency: python-pptx required; see references/requirements.md') from None
        if sys.version_info < (3, 11):
            raise ReadError(3, 'dependency: Python 3.11+ required')
        if args.action == 'check':
            print(json.dumps({'python': sys.version.split()[0], 'python-pptx': pptx.__version__}))
            return 0
        if args.project is None:
            raise ReadError(2, 'input: --project required')
        for value, maximum in ((args.max_records, 2000), (args.max_chars, 200000), (args.max_values, 20000)):
            if not 1 <= value <= maximum:
                raise ReadError(2, 'input: extraction limit out of range')
        no_links(args.project.absolute())
        root = args.project.resolve()
        if not root.is_dir():
            raise ReadError(2, 'input: project directory must exist')
        source, content = load_source(root, args.input)
        from pptx_extract import extract
        result = extract(content, args.slides, args.max_records, args.max_chars, args.max_values)
        result.update(source=source.relative_to(root).as_posix(), sha256=hashlib.sha256(content).hexdigest())
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return 0
    except ReadError as error:
        print(str(error), file=sys.stderr)
        return error.code
    except Exception:
        print('parse: unable to extract presentation; check package structure and file access', file=sys.stderr)
        return 4


if __name__ == '__main__':
    sys.exit(main())
