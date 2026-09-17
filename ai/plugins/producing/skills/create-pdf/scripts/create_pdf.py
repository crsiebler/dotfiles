#!/usr/bin/env python3
"""Create paginated PDF artifacts with explicit fonts and independent validation."""
import argparse
import json
import logging
from pathlib import Path
import sys
sys.dont_write_bytecode = True
from pdf_support import DocumentError, no_links, project_path, publish


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
            import reportlab
            import pypdf
            import PIL
        except ImportError:
            raise DocumentError(3, 'dependency: ReportLab, pypdf and Pillow required; see references/requirements.md') from None
        if sys.version_info < (3,11):
            raise DocumentError(3, 'dependency: Python 3.11+ required')
        if args.action == 'check':
            print(json.dumps({'python':sys.version.split()[0], 'ReportLab':reportlab.Version,
                              'pypdf':pypdf.__version__, 'Pillow':PIL.__version__}))
            return 0
        if args.project is None:
            raise DocumentError(2, 'input: --project required')
        no_links(args.project.absolute())
        root = args.project.resolve()
        if not root.is_dir():
            raise DocumentError(2, 'input: project directory must exist')
        from pdf_inspect import read_pages, verify, inspect
        # Library diagnostics can include input content; return our sanitized errors.
        logging.getLogger('pypdf').setLevel(logging.CRITICAL)
        if args.action == 'inspect':
            result = inspect(read_pages(project_path(root,args.input).read_bytes()))
        else:
            output = project_path(root,args.output,output=True)
            try:
                request = json.loads(project_path(root,args.request).read_text())
            except (ValueError,UnicodeError):
                raise DocumentError(2, 'input: invalid request JSON') from None
            from pdf_build import build
            content, expected, dimensions = build(request,root)
            pages = read_pages(content)
            verify(pages,expected,dimensions)
            publish(output,content)
            result = dict(output=output.relative_to(root).as_posix(),page_count=len(pages),
                          structural_validation='passed',rendered=False)
        print(json.dumps(result,ensure_ascii=False,allow_nan=False))
        return 0
    except DocumentError as error:
        print(str(error),file=sys.stderr)
        return error.code
    except Exception:
        print('generation: unable to process PDF; check font, content size, layout and file access',file=sys.stderr)
        return 4


if __name__ == '__main__':
    sys.exit(main())
