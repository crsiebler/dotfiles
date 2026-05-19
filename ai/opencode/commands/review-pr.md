---
name: review-pr
description: Review a GitHub pull request with OpenCode specialist reviewers
---

# Review Pull Request

Review a GitHub pull request using the reusable PR review prompt and local
repository context. Generate a local review report only. Do not post comments or
submit a GitHub review unless a later explicit posting workflow requests and
confirms it.

OpenCode's provider/model layer handles all AI execution. Do not call OpenAI,
Anthropic, or any other model provider API directly from this command.

## Argument Handling

The optional first argument may be either a PR number or PR URL:
- `/review-pr`
- `/review-pr 123`
- `/review-pr https://github.com/owner/repo/pull/123`

Resolve the PR selector:

1. If `$1` is provided, use it exactly as the PR selector. GitHub CLI accepts a
   PR number or PR URL in `gh pr view`.
2. If `$1` is empty, detect the PR for the current branch with `gh pr view`.
3. If no PR can be detected, stop and ask the user to provide a PR number or PR
   URL. Do not guess from branch names, remotes, or recent PRs.

Current branch:
!`git rev-parse --abbrev-ref HEAD`

Detected PR URL for current branch when no argument is supplied:
!`if [ -z "$1" ]; then gh pr view --json url --jq .url 2>/dev/null || true; fi`

Selected PR argument:
!`if [ -n "$1" ]; then printf '%s\n' "$1"; fi`

Use the selected PR argument when present; otherwise use the detected PR URL.
If both are empty, ask the user for `/review-pr <number-or-url>`.

## Gather PR Context

After resolving the selector, gather this context before reviewing:

PR title, body, URL, number, base branch, head branch, author, state, commits,
and changed files:
!`selector="${1:-$(gh pr view --json url --jq .url 2>/dev/null)}"; if [ -n "$selector" ]; then gh pr view "$selector" --json title,body,url,number,baseRefName,headRefName,author,state,commits,files; fi`

Changed file summary:
!`selector="${1:-$(gh pr view --json url --jq .url 2>/dev/null)}"; if [ -n "$selector" ]; then gh pr diff "$selector" --name-only; fi`

PR diff:
!`selector="${1:-$(gh pr view --json url --jq .url 2>/dev/null)}"; if [ -n "$selector" ]; then gh pr diff "$selector" --patch; fi`

Commits on the PR branch compared with the base branch:
!`selector="${1:-$(gh pr view --json url --jq .url 2>/dev/null)}"; if [ -n "$selector" ]; then base=$(gh pr view "$selector" --json baseRefName --jq .baseRefName); head=$(gh pr view "$selector" --json headRefName --jq .headRefName); git log --oneline "origin/$base..origin/$head" 2>/dev/null || git log --oneline "$base..HEAD" 2>/dev/null || true; fi`

Reusable PR review prompt:
!`if [ -f ai/opencode/pr-review.md ]; then cat ai/opencode/pr-review.md; elif [ -f "$HOME/.config/opencode/pr-review.md" ]; then cat "$HOME/.config/opencode/pr-review.md"; else printf 'Missing reusable PR review prompt. Expected ai/opencode/pr-review.md or $HOME/.config/opencode/pr-review.md.\n'; fi`

## Specialist Subagent Workflow

Run specialist review passes against the gathered PR context before producing
the consolidated report. OpenCode's subagent system handles the specialist work;
do not call model provider APIs directly.

Always run these default specialist passes:
- `code-reviewer`: correctness, maintainability, error handling, API contracts,
  data flow, and project conventions.
- `qa-expert`: missing or weak tests, brittle assertions, fixture gaps,
  regression risk, and validation coverage.
- `security-engineer`: secure coding risks, injection, authentication and
  authorization mistakes, secret exposure, unsafe file access, network trust
  boundaries, dependency risk, logging leaks, and input validation.

Conditionally add these specialist passes when the changed file list or diff
content indicates their domain is relevant:
- `security-auditor`: include when files or diff content touch authentication,
  authorization, secrets, dependencies, inputs, networking, file access,
  logging, or trust boundaries.
- `documentation-engineer`: include when files or diff content touch
  user-facing behavior, commands, APIs, environment variables, configuration,
  installation, or operational behavior.
- `compliance-auditor`: include when files or diff content touch PII, PHI,
  financial data, retention, consent, audit trails, licensing, accessibility,
  or regulated workflows.

For each specialist pass, provide the PR metadata, changed file summary, diff,
commits, repository instructions, and reusable PR review prompt. Require every
specialist to return findings using the shared finding schema from the reusable
prompt. If a specialist has no actionable findings, it should explicitly return
an empty findings list and note residual risks or checks not run.

Merge specialist results before writing the final report:
- Deduplicate findings that describe the same root cause, even when different
  specialists report them with different wording or adjacent line references.
- Keep the highest severity among duplicates and preserve the clearest body.
- Combine useful remediation details from duplicate findings without repeating
  the same issue in multiple report entries.
- Preserve the `source` field for the primary specialist finding, or list
  multiple sources in the body when that context is important.
- Discard generic, praise-only, speculative, or unchanged-code findings that do
  not satisfy the reusable prompt's noise-reduction rules.

## Inline Comment Mapping

Before deciding whether findings are inline comments or summary-only findings,
parse the PR diff and build a map of commentable lines for each changed file:

- For every `diff --git` file section, track the relative path from the `+++`
  and `---` headers. Use `+++ b/<path>` for added or modified lines and
  `--- a/<path>` for deleted lines. Treat `/dev/null` as absent.
- For every hunk header, track old and new line numbers from the
  `@@ -old_start,old_count +new_start,new_count @@` ranges.
- Lines beginning with `+` but not `+++` are commentable on side `RIGHT` at the
  current new-file line number.
- Lines beginning with `-` but not `---` are commentable on side `LEFT` at the
  current old-file line number.
- Context lines advance both old and new counters but are not valid inline
  comment targets unless GitHub marks them as changed in the PR diff.
- Record each valid target as `{ path, line, side }` and use only those records
  when preparing inline comments.

When converting merged findings into inline comments:

- Inline findings must include `path`, `line`, `side`, and `body` fields that
  are compatible with GitHub's pull request review API.
- Use `side: "RIGHT"` for added or modified lines from the new side of the diff.
- Use `side: "LEFT"` for deleted lines from the old side of the diff.
- Include `start_line`, `start_side`, `line`, and `side` for multiline comments
  only when every referenced line maps to a valid diff-visible line in the same
  file and on the intended side.
- If a finding lacks a valid `{ path, line, side }` mapping, or if any multiline
  range endpoint is invalid, move it to the consolidated summary instead of the
  inline comments list.
- Do not invent line numbers, target unchanged context, or post comments for
  files and lines that are not visible in the diff.

Preview the local inline review payload before any posting workflow is used.
Include the PR URL, intended review event, consolidated review body, inline
comment count, and a JSON-compatible comments array with the exact fields that
would be sent to GitHub. If any proposed inline comment is malformed or
unmappable, remove it from the inline payload and include the finding in the
summary preview instead.

## Review Instructions

Use the reusable prompt as the source of truth for review objectives, severity
levels, finding schema, noise-reduction rules, summary versus inline comment
rules, posting safety requirements, and specialist reviewer guidance.

Produce a consolidated local review report containing:
- PR metadata: title, URL, base branch, and head branch.
- Specialist passes used and why.
- Findings ordered by severity, with file and line references when they map to
  valid diff-visible lines.
- Inline comment payload preview with only valid GitHub review comment fields.
- Summary-only findings for issues that cannot be safely mapped inline.
- Residual risks and checks not run.

Do not post the review to GitHub from this command.
