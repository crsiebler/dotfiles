---
name: pull-request
description: Create a pull request for the current branch with formatted description including Jira ticket
---

Create a pull request for the current branch.

Determine the base branch handling:
- If $1 is provided, include --base $1 in the gh command
- If $1 is empty, omit --base flag (gh will automatically use the repository's default branch)

Gather required information:

Current branch: !`git rev-parse --abbrev-ref HEAD`

Last commit title: !`git log -1 --pretty=%s`

Worktree name: !`git worktree list | grep $(pwd) | awk '{print $1}' | xargs basename`

Jira ticket (optional, only if matches PROJ-123 format): !`git worktree list | grep $(pwd) | awk '{print $1}' | xargs basename | grep -oE '[A-Z]+-[0-9]+' || echo ""`

Changes since branching from base branch:
!`git diff --name-status ${1:-$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name)}..HEAD`

Based on the above information, construct and execute the GitHub CLI command to create the PR:

**PR Title:** Use the last commit title directly

**PR Description:** Create a detailed breakdown of changes following this format:
- Modified [File] to [brief description of what changed]
- [Additional bullet points as needed]
- [More detailed explanations if needed]

[If Jira ticket is present, include it on a new line at the end]

Execute this command:
!`gh pr create ${1:+--base $1} --head $(git rev-parse --abbrev-ref HEAD) --title "$(git log -1 --pretty=%s)" --body "[generated description]"`

Confirm the PR was created successfully and provide the PR URL.