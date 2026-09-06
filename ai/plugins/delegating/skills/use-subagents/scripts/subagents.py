"""Read static native definitions, not runtime-loaded agent state. Python 3.11+.

TOML uses tomllib. Markdown metadata supports only top-level single-line
name/description/tools scalars; complex YAML metadata is omitted, not guessed.
Fetch always returns the complete original file bytes.
"""
import argparse
import os
from pathlib import Path
import re
import sys
import tomllib


def metadata(path):
    text = path.read_text()
    if path.suffix == '.toml':
        return tomllib.loads(text)
    # Deliberately only top-level, single-line scalar frontmatter. No YAML claims.
    result = {}
    lines = text.splitlines()
    if lines and lines[0] == '---':
        for line in lines[1:]:
            if line == '---':
                break
            match = re.fullmatch(r'(name|description|tools):\s*(.*)', line)
            if match:
                value = match[2]
                if value not in ('|', '>', '|-', '>-'):
                    result[match[1]] = value.strip('\"\'')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--harness', choices=['opencode', 'codex'])
    parser.add_argument('--scope', choices=['global', 'project'])
    parser.add_argument('--project', type=Path, help='Project root (default: nearest Git root or cwd)')
    parser.add_argument('command', choices=['list', 'search', 'fetch', 'help'])
    parser.add_argument('query', nargs='?')
    args = parser.parse_args()
    if (args.command in ('search', 'fetch')) != bool(args.query):
        parser.error('search/fetch require exactly one nonempty argument; list/help take none')
    if args.command == 'fetch' and not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_.-]*', args.query):
        parser.error('fetch requires an exact agent name, not a path')
    if args.command == 'help':
        parser.print_help()
        return
    project = args.project.resolve() if args.project else Path.cwd()
    if not args.project:
        project = next((p for p in [project, *project.parents] if (p / '.git').exists()), project)
    harness = args.harness
    if not harness:
        candidates = [h for h in ('codex', 'opencode') if (project / ('.' + h)).is_dir()]
        if len(candidates) == 1:
            harness = candidates[0]
        else:
            parser.error('specify --harness codex|opencode; harness cannot be determined safely')
    home = Path.home()
    global_root = (Path(os.environ.get('CODEX_HOME', home / '.codex')) if harness == 'codex'
                   else Path(os.environ.get('XDG_CONFIG_HOME', home / '.config')) / 'opencode')
    roots = [('global', global_root), ('project', project / ('.' + harness))]
    records = []
    for scope, root in roots:
        if args.scope and args.scope != scope:
            continue
        folders = ['agents'] if harness == 'codex' else ['agents', 'agent']
        for folder in folders:
            for path in sorted((root / folder).rglob('*.toml' if harness == 'codex' else '*.md')):
                meta = metadata(path)
                records.append((scope, path, str(meta.get('name', path.stem)), str(meta.get('description', '')), str(meta.get('tools', ''))))
    if args.command == 'fetch':
        matches = [r for r in records if args.query in (r[1].stem, r[2])]
        if len(matches) != 1:
            parser.exit(1, 'subagents: ' + ('duplicate definitions; select --scope or --project\n' if matches else 'not found; use list or search\n'))
        sys.stdout.buffer.write(matches[0][1].read_bytes())
        return
    print(f'{harness}: static definitions (not runtime-loaded state)')
    for scope, path, name, description, tools in records:
        if args.command == 'search' and args.query.casefold() not in f'{name} {path.stem} {description} {tools}'.casefold():
            continue
        print(f'{name}\t{scope}\t{description}\t{path}')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError):
        print('subagents: cannot read/parse a native definition; check file syntax and permissions.', file=sys.stderr)
        sys.exit(1)
