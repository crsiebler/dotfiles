# Requirements

## Required and conditional dependencies

The bundled discovery launcher uses a POSIX shell and Python 3.11+ (`tomllib`
is standard library). No pip package or global `subagents` binary is required.
Resolve `scripts/subagents` from the advertised loaded skill. Catalog inspection
works without a native delegation tool; actual delegation additionally needs
exposed native agent capabilities, authorization, and the applicable budget.

## Installation and checks

If Python is missing, separately approved setup on macOS with existing Homebrew
can use `brew install python@3.11`
([formula](https://formulae.brew.sh/formula/python@3.11)).
Other platforms: [Python installation](https://www.python.org/downloads/).
Verify the chosen interpreter and use the installed skill path:

```sh
python3.11 --version
skill_dir='/absolute/path/to/loaded/use-subagents'
PYTHON=python3.11 "$skill_dir/scripts/subagents" --help
```

Replace the path placeholder. `PYTHON` may select an existing executable; the
launcher checks for `tomllib`. Do not install the helper globally or modify user
agent collections to test discovery. Inspecting a role file does not prove a
native delegated invocation or its runtime restrictions.
