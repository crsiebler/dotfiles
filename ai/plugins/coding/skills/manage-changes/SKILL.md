---
name: manage-changes
description: Ship scoped changes through Git commits, branch pushes and GitHub pull requests with explicit write approval.
---

# Manage Changes

Read [requirements](references/requirements.md) before selecting external tools or
running helpers. Dependency setup is separately authorized.

Use for shipping changes, preparing commits, pushing a feature branch, or opening
a pull request. Identify the requested endpoint and repository/remote provider.
GitHub is the implemented adapter; other hosts need a verified adapter before
external operations. Do not claim support from a matching URL alone.

Read [Git and GitHub workflow](references/git-github.md). Inspect repository
instructions, current branch, worktree state, diff, tracking, and recent history.
Preserve unrelated work and follow repository naming conventions rather than
imposing Git Flow.

For commit drafting or validation, read [commit messages](references/commit-messages.md).
For requested changelog work, read [git-cliff](references/git-cliff.md); it is
optional and is not run on every commit by default.

An explicit request to implement an approved plan includes its initial and
subsequent scoped local commits. Honor that existing grant without asking again;
explicit no-commit or planning-only instructions take precedence. Scope expansion
and external writes still need their applicable authority.
Create branches or commits only within actual scope. Run required tests, lint, and
typecheck before a commit; stage intended paths only. Do not amend, rebase shared
history, force-push, bypass hooks, or merge implicitly.

For actions whose authority is missing, prepare the complete shipping sequence
before asking for its write approval:
validation, intended file/commit scope if needed, exact push remote/ref, and PR
head/base/title/body/payload. One explicit approval may cover that bounded
sequence; carry it forward without repeated requests. If its target or material
content changes, preview the changed scope and obtain approval for it. A request
to prepare shipping alone grants no push/PR write authority.

Use the final base-to-head behavior and purpose for the PR description, with
actual validation and limitations. After automatic run archival, include the
authorized closeout commit and verify that active artifacts were archived and
the intended branch is ready. Do not archive or remove state as a shipping side
effect. Verify actual commit IDs, remote branch and PR URL before reporting
success. Stop after the requested endpoint; no implicit merge, release or deploy.
