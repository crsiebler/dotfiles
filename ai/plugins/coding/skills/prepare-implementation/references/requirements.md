# Requirements

## Required and conditional dependencies

Planning needs no external package or installed runner. Resolve harness identity
from trusted runtime context or the invoking entry point; installed executables
do not determine the active harness.

Execution handoff is conditional: Git and the exact prepared branch/commit;
Codex Goal with its native `story-reviewer`, or OpenCode/Ralph with native
`ralph-reviewer`. Those are separate execution contracts, not prerequisites
for writing a plan. Ralph requires Python 3.11+, Git, POSIX process groups/flock,
OpenCode, and matching runner guidance. Ruby and jq are repository test fixtures,
not Ralph runtime dependencies.

The bundled archive helper needs Python 3.11+, Git, and POSIX filesystem/locking
support. Its Python imports are standard library; no pip package is required.
Archival/removal and closeout commits need their own applicable authorization.

## Installation and checks

For missing Python/Git on macOS with existing Homebrew and setup approval:

```sh
brew install python@3.11 git
python3.11 --version
git --version
```

Use [Python downloads](https://www.python.org/downloads/) and
[Git downloads](https://git-scm.com/downloads) for other supported hosts.
Obtain OpenCode through its [official installation guide](https://opencode.ai/docs/).
Codex/native reviewer setup belongs to the selected harness's reviewed
configuration; discovering a TOML/Markdown role file does not prove invocation.

Ralph is delivered by the owning dotfiles checkout's `bin/ralph`. Review that
checkout's installation guide rather than using a broad shell/dotfiles install
as dependency bootstrap. An installed `ralph --help` and `opencode --version`
check availability; they do not prove a prepared execution or recovery is safe.
No setup or execution occurs while drafting requirements/plans.
