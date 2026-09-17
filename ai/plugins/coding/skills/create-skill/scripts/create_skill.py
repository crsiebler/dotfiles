#!/usr/bin/env python3
"""Portable, project-owned skill validation, packaging, and evaluation CLI."""
import argparse
import importlib.metadata
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True

from aggregate_benchmark import generate_benchmark
from generate_report import generate_markdown
from package_skill import package_skill
from quick_validate import require_yaml, validate_skill
from skill_io import MAX_FILE, SkillError, no_links, project_path, publish, read_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path)
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('check')
    for action in ('validate', 'package', 'benchmark', 'report'):
        command = sub.add_parser(action)
        command.add_argument('source')
        if action != 'validate':
            command.add_argument('output')
    args = parser.parse_args()
    try:
        if sys.version_info < (3, 11):
            raise SkillError(3, 'dependency: Python 3.11 or newer required')
        if args.action == 'check':
            require_yaml()
            print(json.dumps({'python': sys.version.split()[0],
                              'PyYAML': importlib.metadata.version('PyYAML')}))
            return 0
        if args.project is None:
            raise SkillError(2, 'input: --project is required')
        no_links(args.project.absolute())
        root = args.project.resolve()
        if not root.is_dir():
            raise SkillError(2, 'input: project must be an existing directory')
        source = project_path(root, args.source)
        if args.action == 'validate':
            validate_skill(source)
            print('Validated skill frontmatter and bounded file tree.')
            return 0
        output = project_path(root, args.output, output=True)
        if source.is_dir() and output.is_relative_to(source):
            raise SkillError(2, 'input: output must not be inside source directory')
        if args.action == 'package':
            content = package_skill(source)
        elif args.action == 'benchmark':
            data = generate_benchmark(source)
            content = json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False).encode()
            if len(content) > MAX_FILE:
                raise SkillError(4, 'generation: benchmark exceeds readable 2 MiB limit')
            generate_markdown(json.loads(content))  # independent report-contract inspection
        else:
            content = generate_markdown(read_json(source)).encode('utf-8')
        publish(output, content)
        print(json.dumps({'operation': args.action, 'bytes': len(content)}))
        return 0
    except SkillError as error:
        print(str(error), file=sys.stderr)
        return error.code
    except (OSError, ValueError, TypeError, OverflowError, RecursionError):
        print('generation: operation failed; check input structure and filesystem access', file=sys.stderr)
        return 4


if __name__ == '__main__':
    sys.exit(main())
