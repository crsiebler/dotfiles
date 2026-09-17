#!/usr/bin/env python3
"""Create a fresh structured Word document or inspect bounded package content."""
import argparse
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
from docx_support import DocumentError, no_links, project_path, publish


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',type=Path)
    commands=parser.add_subparsers(dest='action',required=True)
    commands.add_parser('check')
    commands.add_parser('inspect').add_argument('input')
    create=commands.add_parser('create')
    create.add_argument('input')
    create.add_argument('output')
    args=parser.parse_args()
    try:
        try:
            import docx
        except ImportError:
            raise DocumentError(3,'dependency: python-docx required; see references/requirements.md') from None
        if sys.version_info < (3,11):
            raise DocumentError(3,'dependency: Python 3.11+ required')
        if args.action=='check':
            print(json.dumps({'python':sys.version.split()[0],'python-docx':docx.__version__}))
            return 0
        if args.project is None:
            raise DocumentError(2,'input: --project is required')
        no_links(args.project.absolute())
        root=args.project.resolve()
        if not root.is_dir():
            raise DocumentError(2,'input: project must be an existing directory')
        source=project_path(root,args.input)
        if args.action=='inspect':
            from docx_inspect import inspect_document
            result=inspect_document(source.read_bytes())
        else:
            output=project_path(root,args.output,output=True)
            if source.stat().st_size > 1024*1024:
                raise DocumentError(2,'input: request exceeds 1 MiB')
            try:
                spec=json.loads(source.read_text(encoding='utf-8'))
            except (ValueError,UnicodeError,RecursionError):
                raise DocumentError(2,'input: invalid UTF-8 JSON request') from None
            from docx_build import create_document
            content,result=create_document(root,spec)
            publish(output,content)
        print(json.dumps(result,ensure_ascii=False,allow_nan=False))
        return 0
    except DocumentError as error:
        print(str(error),file=sys.stderr)
        return error.code
    except Exception:
        # Third-party parse/image failures must not echo document content or tracebacks.
        print('generation: invalid document data or unavailable file; no input was modified',file=sys.stderr)
        return 4


if __name__=='__main__':
    sys.exit(main())
