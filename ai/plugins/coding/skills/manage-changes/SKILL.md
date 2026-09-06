---
name: manage-changes
description: Prepares scoped Git commits and pull requests with explicit write approval.
---

# Manage Changes

Read [Git and GitHub workflow](references/git-github.md). Inspect repository
instructions, current branch, worktree state, diff, tracking, and recent history.
Preserve unrelated work and follow repository naming conventions rather than
imposing Git Flow.

Create branches or commits only when requested. Run required tests, lint, and
typecheck before a commit; stage intended paths only. Do not amend, rebase shared
history, force-push, bypass hooks, or merge implicitly.

For every external write, including pushes and PR creation, preview the exact
target and command/payload and require explicit approval. If the content changes,
preview again. Report successful commit IDs/PR URLs only from actual results.
