#!/usr/bin/env python3
"""Remove recognized dotfiles installer backups, never active configuration."""
import os
from pathlib import Path
import re
import shutil
import sys


STAMP = r'\d{8}_\d{6}(?:_\d{6})?'
BACKUP = re.compile(r'(.+)\.backup\.' + STAMP)


def checked_root(value, label):
    path = Path(value)
    if not value or not path.is_absolute() or path.resolve() == Path('/'):
        raise ValueError(f'{label} must be an absolute directory other than /.')
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError(f'{label} must not use symlinks.')
    if path.exists() and not path.is_dir():
        raise ValueError(f'{label} must be a directory.')
    return path


def files_under(path):
    if path.is_symlink():
        return
    for directory, folders, files in os.walk(path, followlinks=False):
        folders[:] = [name for name in folders
                      if not (Path(directory) / name).is_symlink()]
        for name in files:
            file = Path(directory) / name
            if not file.is_symlink() and file.is_file():
                yield file


def candidates(home, roots):
    found = set()
    for path in home.glob('.zshrc.backup.*'):
        if BACKUP.fullmatch(path.name) and path.is_file() and not path.is_symlink():
            found.add(path)
    for root, names, suffix in roots:
        for name in names:
            for path in root.glob(name + '.backup.*'):
                if BACKUP.fullmatch(path.name) and path.is_file() and not path.is_symlink():
                    found.add(path)
        for folder in ('agents', 'commands'):
            for path in files_under(root / folder):
                match = BACKUP.fullmatch(path.name)
                if match and match[1].endswith(suffix if folder == 'agents' else '.md'):
                    found.add(path)
        archives = root / '.install-ai-backups'
        if archives.is_symlink():
            continue
        if archives.is_dir():
            for path in archives.iterdir():
                if re.fullmatch(STAMP, path.name) and path.is_dir() and not path.is_symlink():
                    found.add(path)
            snapshots = archives / 'plugin-sources'
            if snapshots.is_dir() and not snapshots.is_symlink():
                for plugin in snapshots.iterdir():
                    if not plugin.is_dir() or plugin.is_symlink():
                        continue
                    for path in plugin.iterdir():
                        if (re.fullmatch(r'[0-9a-f]{64}', path.name)
                                and path.is_dir() and not path.is_symlink()):
                            found.add(path)
    return sorted(found)


def main():
    home = checked_root(os.environ.get('HOME', ''), 'HOME')
    codex = checked_root(os.environ.get('CODEX_HOME', str(home / '.codex')), 'CODEX_HOME')
    xdg = checked_root(os.environ.get('XDG_CONFIG_HOME', str(home / '.config')), 'XDG_CONFIG_HOME')
    opencode = checked_root(str(xdg / 'opencode'), 'OpenCode configuration')
    roots = ((codex, ('config.toml', 'astra.config.toml', 'AGENTS.md'), '.toml'),
             (opencode, ('opencode.json', 'tui.json', 'astra.json', 'sol.json',
                         'opencode-notifier.json', 'AGENTS.md'), '.md'))
    paths = candidates(home, roots)
    for path in paths:
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    print(f'Removed {len(paths)} installer backup files or archives. Active files and inventories were preserved.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as error:
        print(f'clean-install-backups: {error}', file=sys.stderr)
        sys.exit(1)
