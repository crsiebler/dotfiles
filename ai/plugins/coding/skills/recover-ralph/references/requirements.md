# Requirements

## Required and conditional dependencies

Diagnosis uses the matching installed `ralph` CLI and its read-only
`ralph --status` interface. The runner needs Python 3.11+, Git, and a POSIX host
with process groups/flock. Its Python runtime is standard library only.
OpenCode and native `ralph-reviewer` are needed for an approved resumed run,
not for merely reading runner state. jq/Ruby are test-fixture dependencies only.

Load the advertised `prepare-implementation` skill's recovery/execution
references through discovery. Do not substitute a hardcoded sibling or cache path,
a different reviewer, or an unverified runner version.

## Installation and checks

Missing Python/Git on macOS with existing Homebrew can be provisioned separately:

```sh
brew install python@3.11 git
python3.11 --version
git --version
```

Use [Python](https://www.python.org/downloads/) and
[Git](https://git-scm.com/downloads) platform instructions for other supported
POSIX hosts. OpenCode setup follows [official installation](https://opencode.ai/docs/).
For Ralph, use the owning dotfiles checkout's reviewed `bin/ralph` installation
procedure; do not run a broad dotfiles install to diagnose a stopped run.
Confirm `ralph --help` exposes the expected status/recovery interfaces.
Its `/usr/bin/env python3` launcher also needs that executable to resolve to
Python 3.11+; installing `python3.11` alone does not prove launcher resolution.

Read-only diagnosis grants no installation, service operation, ledger edit,
stop-file removal, or resume permission. Setup cannot repair a persisted blocker.
