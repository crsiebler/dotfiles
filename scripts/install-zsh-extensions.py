#!/usr/bin/env python3
"""Install missing Oh My Zsh extensions; never update existing checkouts."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


EXTENSIONS = [
    ('plugins/opencode', 'https://github.com/crsiebler/omz-plugin-opencode.git',
     'opencode.plugin.zsh'),
    ('plugins/gh', 'https://github.com/crsiebler/omz-plugin-gh.git', 'gh.plugin.zsh'),
    ('plugins/bun', 'https://github.com/ntnyq/omz-plugin-bun.git', 'bun.plugin.zsh'),
    ('plugins/you-should-use', 'https://github.com/MichaelAquilina/zsh-you-should-use.git',
     'you-should-use.plugin.zsh'),
    ('plugins/zsh-autosuggestions', 'https://github.com/zsh-users/zsh-autosuggestions.git',
     'zsh-autosuggestions.plugin.zsh'),
    ('plugins/zsh-syntax-highlighting',
     'https://github.com/zsh-users/zsh-syntax-highlighting.git',
     'zsh-syntax-highlighting.plugin.zsh'),
    ('themes/powerlevel10k', 'https://github.com/romkatv/powerlevel10k.git',
     'powerlevel10k.zsh-theme'),
]


def main():
    home = Path(os.environ.get('HOME', ''))
    zsh = Path(os.environ.get('ZSH') or home / '.oh-my-zsh')
    custom = Path(os.environ.get('ZSH_CUSTOM') or zsh / 'custom')
    for label, path in (('HOME', home), ('ZSH', zsh), ('ZSH_CUSTOM', custom)):
        if not path.is_absolute() or path == Path('/'):
            raise ValueError(f'{label} must be an absolute directory other than /')
    if not (zsh / 'oh-my-zsh.sh').is_file():
        raise ValueError(f'Oh My Zsh is required at {zsh}; install it separately first')
    if not shutil.which('git'):
        raise ValueError('git is required on PATH; install it separately first')

    # Check all existing destinations before downloading anything. Existing
    # custom or non-Git installations are valid if their entry point is readable.
    for relative, _, entry in EXTENSIONS:
        destination = custom / relative
        if any(path.is_symlink() for path in (destination, *destination.parents)):
            raise ValueError(f'symlink at or above {destination}; reconcile manually')
        if destination.exists() and not (
                (destination / entry).is_file() and os.access(destination / entry, os.R_OK)):
            raise ValueError(f'existing {destination} lacks readable {entry}; preserve and reconcile manually')

    installed = preserved = 0
    for relative, url, entry in EXTENSIONS:
        destination = custom / relative
        if destination.exists():
            print(f'Keeping existing {relative} (no updates).', flush=True)
            preserved += 1
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        print(f'Installing {relative} from {url}...', flush=True)
        # Clone to our own temporary directory so failed downloads do not leave
        # an apparently installed plugin. Do not execute downloaded code here.
        with tempfile.TemporaryDirectory(prefix='.install-zsh-', dir=destination.parent) as staging:
            checkout = Path(staging) / 'checkout'
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', '--', url, str(checkout)],
                env=dict(os.environ, GIT_TERMINAL_PROMPT='0'),
                capture_output=True, text=True,
            )
            if result.returncode:
                raise ValueError(f'clone failed for {relative} (exit {result.returncode}); '
                                 'check network access and repository availability, then retry')
            if not (checkout / entry).is_file() or not os.access(checkout / entry, os.R_OK):
                raise ValueError(f'missing readable entry point {entry} for {relative}; not installed')
            if destination.exists() or destination.is_symlink():
                raise ValueError(f'destination appeared during installation: {relative}; retry after inspection')
            checkout.rename(destination)
        installed += 1
        print(f'Installed {relative}.', flush=True)
    print(f'Zsh extensions ready: {installed} installed, {preserved} preserved.', flush=True)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as error:
        message = str(error) if isinstance(error, ValueError) else (
            f'filesystem/process error (errno {error.errno}); check target paths and permissions')
        print(f'install-zsh-extensions: {message}', file=sys.stderr)
        print('Installation stopped. Earlier completed extensions are retained; retry is safe.',
              file=sys.stderr)
        sys.exit(1)
