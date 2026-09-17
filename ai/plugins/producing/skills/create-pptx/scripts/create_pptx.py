#!/usr/bin/env python3
"""Create and structurally inspect bounded editable PPTX presentations."""
import argparse
import io
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
from pptx_support import DocumentError, inspect_package, no_links, project_path, publish


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path)
    commands = parser.add_subparsers(dest='action', required=True)
    commands.add_parser('check')
    commands.add_parser('layouts')
    create = commands.add_parser('create')
    create.add_argument('request')
    create.add_argument('output')
    commands.add_parser('inspect').add_argument('input')
    args = parser.parse_args()
    try:
        try:
            import pptx
            import PIL
        except ImportError:
            raise DocumentError(3, 'dependency: python-pptx and Pillow required; see references/requirements.md') from None
        if sys.version_info < (3, 11):
            raise DocumentError(3, 'dependency: Python 3.11+ required')
        from pptx_inspect import inspect, layouts
        if args.action == 'check':
            print(json.dumps({'python': sys.version.split()[0], 'python-pptx': pptx.__version__, 'Pillow': PIL.__version__}))
            return 0
        if args.action == 'layouts':
            print(json.dumps(layouts()))
            return 0
        if args.project is None:
            raise DocumentError(2, 'input: --project required')
        no_links(args.project.absolute())
        root = args.project.resolve()
        if not root.is_dir():
            raise DocumentError(2, 'input: project directory must exist')
        if args.action == 'inspect':
            content = project_path(root, args.input).read_bytes()
            inspect_package(content)
            result = inspect(pptx.Presentation(io.BytesIO(content)))
        else:
            output = project_path(root, args.output, output=True)
            try:
                request = json.loads(project_path(root, args.request).read_text())
            except (ValueError, UnicodeError):
                raise DocumentError(2, 'input: invalid request JSON') from None
            from pptx_build import build
            presentation = build(request, root)
            expected = inspect(presentation)
            if expected['truncated']:
                raise DocumentError(2, 'input: generated content exceeds inspection budget')
            stream = io.BytesIO()
            presentation.save(stream)
            content = stream.getvalue()
            inspect_package(content)
            result = inspect(pptx.Presentation(io.BytesIO(content)))
            if result != expected:
                raise DocumentError(5, 'validation: reopened presentation differs')
            publish(output, content)
            result = {'output': output.relative_to(root).as_posix(), 'slide_count': result['slide_count'],
                      'structural_validation': 'passed', 'rendered': False}
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return 0
    except DocumentError as error:
        print(str(error), file=sys.stderr)
        return error.code
    except Exception:
        print('generation: cannot process presentation; check package, inputs, and file access', file=sys.stderr)
        return 4


if __name__ == '__main__':
    sys.exit(main())
