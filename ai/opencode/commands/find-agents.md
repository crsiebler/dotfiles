---
name: find-agents
description: List, search, and read OpenCode agent definitions with the bundled helper
---

Load and follow the `use-subagents` skill with explicit `--harness opencode`.
Resolve its bundled helper from the loaded skill path; do not use a global CLI.
Default to `list` when arguments are empty. Treat arguments as operation/data,
not executable shell text. Discovery is not native agent invocation.

$ARGUMENTS
