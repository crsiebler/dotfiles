---
name: format-code
description: Format and lint intended changed files using the repository's configured tools across languages; inspect automatic changes and report unavailable checks.
---

# Format Code

Inspect repository instructions, scripts, formatter configuration, and changed
files. Select the repository-native tools and commands for the actual languages.
Read [Python](references/python.md) or
[JavaScript/TypeScript](references/javascript-typescript.md) only for applicable
files; other languages use their verified project configuration without forcing
these adapters. Repository commands and installed versions are authoritative.
Resolve bundled references relative to this loaded skill, not a sibling skill.

Read-only review and planning do not authorize formatting or lint execution.
This helper stays within the caller's scope; it does not create execution state,
start implementation/orchestration, or replace required review gates. If no tool
is configured or available, report the limitation rather than choose/install one.

Scope writes to intended files. Start with checks when change scope is unclear;
review auto-fix diffs and rerun checks. Do not install missing tools, alter
dependencies/configuration, bypass hooks, or apply unsafe fixes implicitly.
Report commands, files affected, failures, and checks not run. Formatting is not
a substitute for tests or typecheck and does not authorize a commit.
