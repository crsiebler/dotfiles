---
name: format-code
description: Formats and lints changed Python or JavaScript/TypeScript files.
---

# Format Code

Inspect repository instructions, scripts, formatter configuration, and changed
files. Use [Python](references/python.md) or
[JavaScript/TypeScript](references/javascript-typescript.md); read both for a
mixed change. Repository commands and installed versions are authoritative.

Scope writes to intended files. Start with checks when change scope is unclear;
review auto-fix diffs and rerun checks. Do not install missing tools, alter
dependencies/configuration, bypass hooks, or apply unsafe fixes implicitly.
Report commands, files affected, failures, and checks not run. Formatting is not
a substitute for tests or typecheck and does not authorize a commit.
