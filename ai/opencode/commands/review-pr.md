---
name: review-pr
description: Review a GitHub pull request with OpenCode specialist reviewers
---

# Review Pull Request

Review a GitHub pull request using the reusable PR review prompt and local
repository context. By default, generate a local review report only. Do not post
comments or submit a GitHub review unless the user passes `--post` and then
explicitly confirms the exact payload.

OpenCode's provider/model layer handles all AI execution. Do not call OpenAI,
Anthropic, or any other model provider API directly from this command.

## Argument Handling

The optional argument string may include `--post` and may include a PR number or
PR URL:
- `/review-pr`
- `/review-pr 123`
- `/review-pr https://github.com/owner/repo/pull/123`
- `/review-pr --post`
- `/review-pr --post 123`
- `/review-pr --post https://github.com/owner/repo/pull/123`

Resolve the PR selector:

1. Treat the literal token `--post` as a posting request, not as a PR selector.
2. If the remaining argument text is provided, use it exactly as the PR
   selector. GitHub CLI accepts a PR number or PR URL in `gh pr view`.
3. If no selector remains, detect the PR for the current branch with
   `gh pr view`.
4. If no PR can be detected, stop and ask the user to provide a PR number or PR
   URL. Do not guess from branch names, remotes, or recent PRs.

Current branch:
!`git rev-parse --abbrev-ref HEAD`

Detected PR URL for current branch when no argument is supplied:
!`selector=""; for arg in $1; do [ "$arg" = "--post" ] && continue; selector="${selector:+$selector }$arg"; done; if [ -z "$selector" ]; then gh pr view --json url --jq .url 2>/dev/null || true; fi`

Selected PR argument:
!`selector=""; for arg in $1; do [ "$arg" = "--post" ] && continue; selector="${selector:+$selector }$arg"; done; if [ -n "$selector" ]; then printf '%s\n' "$selector"; fi`

Posting requested:
!`case " $1 " in *" --post "*) printf 'yes\n' ;; *) printf 'no\n' ;; esac`

Use the selected PR argument when present; otherwise use the detected PR URL.
If both are empty, ask the user for `/review-pr <number-or-url>`.

## Gather PR Context

After resolving the selector, gather this context before reviewing:

PR title, body, URL, number, base branch, head branch, author, state, commits,
and changed files:
!`selector=""; for arg in $1; do [ "$arg" = "--post" ] && continue; selector="${selector:+$selector }$arg"; done; selector="${selector:-$(gh pr view --json url --jq .url 2>/dev/null)}"; if [ -n "$selector" ]; then gh pr view "$selector" --json title,body,url,number,baseRefName,headRefName,author,state,commits,files; fi`

Changed file summary:
!`selector=""; for arg in $1; do [ "$arg" = "--post" ] && continue; selector="${selector:+$selector }$arg"; done; selector="${selector:-$(gh pr view --json url --jq .url 2>/dev/null)}"; if [ -n "$selector" ]; then gh pr diff "$selector" --name-only; fi`

PR diff:
!`selector=""; for arg in $1; do [ "$arg" = "--post" ] && continue; selector="${selector:+$selector }$arg"; done; selector="${selector:-$(gh pr view --json url --jq .url 2>/dev/null)}"; if [ -n "$selector" ]; then gh pr diff "$selector" --patch; fi`

Commits on the PR branch compared with the base branch:
!`selector=""; for arg in $1; do [ "$arg" = "--post" ] && continue; selector="${selector:+$selector }$arg"; done; selector="${selector:-$(gh pr view --json url --jq .url 2>/dev/null)}"; if [ -n "$selector" ]; then base=$(gh pr view "$selector" --json baseRefName --jq .baseRefName); head=$(gh pr view "$selector" --json headRefName --jq .headRefName); git log --oneline "origin/$base..origin/$head" 2>/dev/null || git log --oneline "$base..HEAD" 2>/dev/null || true; fi`

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

## Confirmed GitHub Posting Workflow

Default behavior is local-only. When `--post` is absent, produce the local
review report and stop without invoking `gh pr review`, `gh api`, or any other
GitHub write command.

When `--post` is present, prepare a GitHub pull request review but do not submit
it immediately. First show a posting preview containing:

- PR URL.
- Review event, using `COMMENT` unless the user explicitly asks for another
  supported GitHub review event.
- Consolidated review body exactly as it would be posted.
- Inline comment count.
- Exact `gh pr review` command for summary-only reviews, or exact `gh api`
  endpoint and JSON payload for reviews with inline comments.

Use `gh pr review` only when there are no inline comments to post:

```sh
gh pr review "$selector" --comment --body-file "$review_body_file"
```

Use GitHub's pull request reviews API when inline comments are included:

```sh
gh api "repos/:owner/:repo/pulls/$pr_number/reviews" \
  --method POST \
  --input "$review_payload_file"
```

The API payload must include the review `body`, `event`, and the validated
`comments` array from the inline payload preview. Do not include malformed,
unmappable, or summary-only findings in `comments`.

After showing the posting preview, ask the user to confirm before running any
GitHub write command. Accepted confirmation values are exactly:

- `yes`
- `y`
- `confirm`
- `post it`
- `go ahead`

Treat all other responses, including empty, ambiguous, or negative responses,
as cancellation. On cancellation, report that nothing was posted and leave the
local review report available in the conversation.

Only after receiving an accepted confirmation value may you run the previewed
`gh pr review` command or `gh api` request. Do not post if the command or API
payload has changed since the user confirmed; show the updated preview and ask
again.

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
- Posting status: local-only when `--post` is absent; pending confirmation,
  posted, or cancelled when `--post` is present.

Do not post the review to GitHub unless `--post` is present and the user gives
one of the accepted confirmation values after seeing the exact payload.
