---
name: ship
description: Prepare and create a pull request after preview and explicit approval
---

Load and follow `manage-changes`, including its GitHub reference, for PR creation.
Treat `$1` as an optional base branch value, not shell code. If absent, discover
the repository default base for comparison and omit `--base` when creating.
Use the last commit title and a file-by-file change summary; append a Jira key
only when reliably identified. Inspect all included commits and the base diff.

Stop on `main`/`master`, no relevant changes, or uncommitted work unless the user
explicitly approves ignoring it. Use a unique project-local body file. Preview
head/base, title, full body, and exact `gh pr create` command; require explicit
confirmation (`yes`, `y`, `confirm`, `create it`, or `go ahead`) afterward.
All other responses cancel. Do not push implicitly; a push needs its own preview
and approval. Return the verified PR URL only after successful creation.

$ARGUMENTS
