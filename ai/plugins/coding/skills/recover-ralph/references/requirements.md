# Requirements

## Required and conditional dependencies

Diagnosis uses the matching installed `ralph` CLI and its read-only
`ralph --status` interface. The runner needs Python 3.11+, Git, and a POSIX host
with process groups/flock. Its Python runtime is standard library only.
OpenCode and native `ralph-reviewer` are needed for an approved resumed run,
not for merely reading runner state. jq/Ruby are test-fixture dependencies only.

Read the actual native ralph and ralph-reviewer definitions through discovery.
The existing use-subagents helper may fetch them with explicit opencode harness
and project root; resolve it from its advertised skill. Missing or duplicate
definitions block dependent diagnosis. Do not guess cache paths, substitute a
reviewer or infer native invocation from fetched text.

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
Its shell launcher searches supported interpreter names and validates Python
3.11+, including a newer interpreter exposed only as `python3`. An active Conda
interpreter is supported; no new environment or package setup is needed.

Read-only diagnosis grants no installation, service operation, ledger edit,
stop-file removal, or resume permission. Setup cannot repair a persisted blocker.

Contract loading does not start an execution or planning workflow. Ralph remains
serial under its own native adapter and runner.
