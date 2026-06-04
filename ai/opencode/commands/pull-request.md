---
name: pull-request
description: Create a pull request for the current branch with formatted description including Jira ticket
---

Create a pull request for the current branch. This command may write to
GitHub, so it must preview the exact PR details and receive explicit
confirmation before running `gh pr create`.

Determine the base branch handling:
- If $1 is provided, include `--base $1` in the `gh pr create` command
- If $1 is empty, omit `--base` so GitHub CLI uses the repository default branch

Safety checks before previewing:
- Stop if the current branch is `main` or `master`.
- Stop if there are uncommitted changes unless the user explicitly says to ignore them.
- Stop if there are no commits or file changes between the base branch and `HEAD`.

Gather required information:

Current branch: !`git rev-parse --abbrev-ref HEAD`

Last commit title: !`git log -1 --pretty=%s`

Worktree name: !`git worktree list | grep $(pwd) | awk '{print $1}' | xargs basename`

Jira ticket (optional, only if matches PROJ-123 format): !`git worktree list | grep $(pwd) | awk '{print $1}' | xargs basename | grep -oE '[A-Z]+-[0-9]+' || echo ""`

Changes since branching from base branch:
!`git diff --name-status ${1:-$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name)}..HEAD`

Based on the above information, construct the GitHub CLI command to create the PR.

**PR Title:** Use the last commit title directly

**PR Description:** Create a detailed breakdown of changes following this format:
- Modified [File] to [brief description of what changed]
- [Additional bullet points as needed]
- [More detailed explanations if needed]

[If Jira ticket is present, include it on a new line at the end]

Before creating the PR, show a preview containing:
- Current branch
- Base branch or repository default branch behavior
- PR title
- Full PR description
- Exact `gh pr create` command

Use a workspace-local body file for the generated description instead of an
inline `--body` value. Example command shape:

```sh
gh pr create ${1:+--base $1} --head "$(git rev-parse --abbrev-ref HEAD)" --title "$(git log -1 --pretty=%s)" --body-file "./.pr-body.md"
```

After showing the preview, ask the user to confirm before running `gh pr
create`. Accepted confirmation values are exactly:

- `yes`
- `y`
- `confirm`
- `create it`
- `go ahead`

Treat all other responses as cancellation. On cancellation, do not run any
GitHub write command.

Confirm the PR was created successfully and provide the PR URL.
