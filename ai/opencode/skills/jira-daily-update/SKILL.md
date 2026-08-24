---
name: jira-daily-update
description: Use when posting a daily Jira update comment for a supplied Jira ticket using Jira MCP, git, and GitHub CLI evidence.
metadata:
  audience: project-managers
  workflow: jira-daily-update
---

# Daily Update

Use this skill to write and post a concise daily progress update as a Jira MCP comment on the Jira ticket supplied in the active context.

## Required Comment Format

The Jira comment must use exactly these labels and this order:

```text
Date:
What I completed:
What’s next:
Blockers:
ETA:
```

Final comments should follow this shape:

```text
Date: YYYY-MM-DD
What I completed:
- ...

What’s next:
- ...

Blockers:
- ...

ETA:
- ...
```

Do not add extra headings or sections.

## Preconditions

Before drafting or posting:

1. Identify the Jira issue key from active context.
2. If no specific Jira issue key is available, stop and ask the user for the ticket.
3. Gather evidence before writing from Jira MCP, git, and GitHub CLI.
4. Do not post if the ticket context is ambiguous, missing, or conflicts with discovered PR or commit evidence.
5. Do not expose secrets, credentials, tokens, private environment values, or sensitive customer data in the comment.

## Evidence Gathering

Use Jira MCP to retrieve the ticket details before writing.

Capture:

- Issue key, summary, description, status, and assignee.
- Acceptance criteria or stated requirements when present.
- Previous comments, especially blockers, promised next steps, prior ETA, and stakeholder requests.

Use git to determine actual local work.

Recommended commands:

```bash
git status
git branch --show-current
git log --oneline --decorate -10
git log --oneline origin/main..HEAD
git diff --stat
git diff --cached --stat
```

Use GitHub CLI to identify related pull requests and their status.

Recommended commands:

```bash
gh pr status
gh pr view --json number,title,state,isDraft,mergeStateStatus,reviewDecision,statusCheckRollup,url,mergedAt,baseRefName,headRefName
gh pr checks
```

Find PRs by current branch, relevant commits, and Jira issue key. If multiple PRs exist, include only PRs relevant to the Jira ticket.

## Section Rules

### Date

Use the current date in `YYYY-MM-DD` format.

### What I completed

Include only work supported by evidence.

Include relevant:

- Commits on the current branch or commits clearly tied to the Jira issue.
- Pull requests tied to the current branch, commits, or Jira issue key.
- Verified local work, clearly labeled if uncommitted.

Prefer concise entries:

```text
- Commit `abc1234`: Implemented scoped environment secret loading.
- PR #123: Scoped secret loading fix - open, checks pending.
```

Avoid overclaiming:

- Do not say work is complete if it is only partially implemented.
- Do not say changes are merged unless PR evidence confirms merge.
- Do not say changes are deployed unless deployment evidence exists.
- Do not claim QA completion or readiness unless explicitly verified.

If no completed work is evident, write:

```text
- No new completed engineering work found since the last update.
```

### What’s next

Analyze what remains based on:

- Jira description and acceptance criteria.
- Current Jira status.
- PR review, check, merge, and draft status.
- Previous Jira comments.
- Current local git state.

Required logic:

- If a PR is open or unmerged, state that merge and deployment still remain.
- If PR checks are failing or pending, state that they need to be resolved or completed before merge.
- If a PR is draft, state that it needs to be moved out of draft.
- If commits exist but no PR exists, state that a PR still needs to be opened.
- If local uncommitted changes exist, state that implementation needs to be finalized, tested, committed, and added to a PR.
- If acceptance criteria are not fully represented in commits or PRs, list the missing pieces conservatively.

### Blockers

Use blockers from active context first.

Also check Jira comments, commits, and PRs for blocker signals, including:

- Failed checks.
- Missing approvals.
- Unresolved review comments.
- Dependency or environment issues.
- Ambiguous requirements.
- Explicit words such as `blocked`, `blocker`, `waiting`, `depends on`, or `cannot proceed`.

Do not invent blockers. If a blocker is inferred rather than explicit, label it as potential.

If no blockers are found, write:

```text
- None identified.
```

### ETA

Estimate engineering development hours only.

Include:

- Remaining development.
- Review response work.
- Merge preparation.
- Deployment time.

Exclude:

- QA testing.
- Product acceptance testing.
- Stakeholder review delays.
- Waiting time for approvals.

Use ranges when uncertain.

Guidance:

- `0 engineering hours`: PR is merged or code is in the target branch, deployment is complete or not required, and no engineering tasks remain.
- `1-2 engineering hours`: only merge coordination and deployment remain, with green checks and no expected code changes.
- `2-4 engineering hours`: minor review fixes, pending checks, merge, and deployment remain.
- `4-8 engineering hours`: implementation exists but tests, PR creation, or moderate integration work remain.
- `6-12 engineering hours`: core implementation is incomplete, requirements are ambiguous, or significant technical blockers remain.

Always include `Excludes QA testing.` in the ETA line.

## Posting Workflow

1. Draft the comment using only evidence-backed statements.
2. Verify the issue key one final time.
3. Verify the comment has the exact required labels and no extra sections.
4. Verify the comment contains no secrets or sensitive data.
5. Use Jira MCP to add the comment to the identified Jira issue.
6. Report back with the Jira issue key and a concise summary of what was posted.

## Guardrails

- Do not post without enough ticket context.
- Do not invent commits, PRs, blockers, deployment state, or ETA.
- Do not include unrelated commits or raw command output unless concise and directly relevant.
- Do not change code, create commits, merge PRs, transition Jira status, or deploy.
- Use conservative language when evidence is incomplete.
