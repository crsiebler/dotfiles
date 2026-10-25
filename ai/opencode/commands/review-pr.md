---
description: Review a GitHub pull request with OpenCode's generic reviewer
---

# Review Pull Request

Review a GitHub pull request using OpenCode's generic reviewer and local
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

## PR Review Standards

Use these standards for all PR review passes and for the consolidated
report. These standards are self-contained in this command; do not read external
review standards files.

### Review Objectives

Find issues that materially affect correctness, maintainability, security, test
reliability, documentation accuracy, or compliance risk. Prioritize actionable
findings over broad commentary. Avoid repeating obvious details from the diff
unless they support a concrete recommendation.

Review the PR title, body, commits, changed files, and diff before producing
findings. Treat the diff as the source of truth for inline comment placement.
Use repository instructions and local conventions when they are available.

### Severity Levels

- `critical`: A confirmed vulnerability, data loss risk, broken production
  path, or compliance failure that should block merge.
- `high`: A likely runtime failure, security weakness, test gap for critical
  behavior, or user-visible regression that should be fixed before merge.
- `medium`: A correctness, maintainability, documentation, or operational issue
  that is worth fixing but does not obviously block safe merge.
- `low`: A small improvement with clear value and low risk, such as a minor
  clarity issue or local consistency problem.

Do not report `low` findings unless they are clearly actionable and specific to
the changed code.

### Finding Schema

Return findings as structured items with these fields:

```json
{
  "severity": "critical|high|medium|low",
  "title": "Short imperative summary",
  "body": "Explain the issue, impact, and suggested fix.",
  "path": "relative/path.ext or null",
  "line": 123,
  "side": "RIGHT|LEFT|null",
  "start_line": 120,
  "start_side": "RIGHT|LEFT|null",
  "end_line": 123,
  "end_side": "RIGHT|LEFT|null",
  "source": "reviewer|auditor|summary"
}
```

Use `path`, `line`, and `side` only when the finding maps to a valid
diff-visible line. Use `RIGHT` for added or modified lines and `LEFT` for
deleted lines. Use multiline fields only when every referenced line is valid and
visible in the PR diff. If a finding cannot be safely mapped to a diff-visible
line, set line fields to `null` and include it in the consolidated summary.

### Noise-Reduction Rules

- Report only issues introduced or exposed by the PR.
- Do not flag unchanged legacy code unless the PR depends on it in a way that
  creates a new risk.
- Do not request stylistic changes unless they affect readability,
  maintainability, or consistency with existing project conventions.
- Do not duplicate findings with the same root cause. Keep the clearest finding
  and highest severity.
- Do not speculate. State assumptions explicitly when evidence is incomplete.
- Prefer one precise finding over several adjacent comments for the same issue.
- Avoid praise-only comments and generic summaries.

### Summary Findings vs Inline Comments

Use inline comments for findings that can be attached to a specific changed line
and where local context helps the author act. Inline comment bodies should be
concise and include the concrete impact and fix.

Use the consolidated summary for findings that apply across files, depend on
missing tests or documentation, describe architectural concerns, or cannot be
mapped to a valid diff-visible line. The summary should include:

- Overall review result.
- Blocking findings by severity.
- Non-blocking findings when actionable.
- Residual risks and testing gaps.
- A short note when no findings were discovered.

### Posting Safety Requirements

- Default to generating a local review report only.
- Do not post comments or submit a GitHub review unless the user explicitly
  requests posting and confirms the exact payload.
- Before posting, show the PR URL, review event, consolidated review body, inline
  comment count, and the exact `gh` command or API payload.
- Never post malformed inline comments. Move unmappable comments to the summary.
- Never include secrets, tokens, credentials, or sensitive environment values in
  review output.
- If GitHub context is missing or ambiguous, ask for the PR number or URL rather
  than guessing.

## Review delegation

The main session gathers PR context, invokes native OpenCode subagents and
consolidates their evidence. It owns all dispatch and any authorized posting.
Review agents do not delegate or write externally. Do not call provider APIs
directly or simulate a native review pass.

| Role | Activation | Responsibility |
| --- | --- | --- |
| `reviewer` | Default: one pass | Assess correctness, regression coverage and the relevant review lenses together; perform authorized focused verification. |
| `auditor` | Optional: a distinct controls assessment is needed | Inspect policy, security or compliance evidence within an explicitly bounded scope; no tests, browser execution or remediation. |

Use `review-code` for the review method and select lenses from actual changed
behavior. Security defects, testing quality, documentation and accessibility are
concerns within the same reviewer pass, not reasons to dispatch another role or
duplicate the reviewer. Load applicable standards skills only for the actual stack.
An auditor adds value only when a separate control or obligation needs assessment;
security-sensitive code alone does not require both roles.

For rendered UI changes, the reviewer uses `verify-interface` for affected flows,
including accessibility and interaction behavior. Use `run-tests` for relevant
project checks when needed. Honor inspection-only mode: no tests, builds or browser
flows. In execute mode, supply authorized commands, time/resource limits, the
candidate revision and worktree, and any existing app/server provenance. Missing
dependencies or a running app are verification gaps, not installation or service
startup authority. Do not claim rendered verification from source inspection.

For each invoked role, provide PR metadata, changed files, diff, commits,
repository instructions, selected concerns, the candidate identity and the shared
finding schema in this command. Require candidate preservation and
actual check results, including failed or unavailable checks. Do not run tests
against a mixed candidate and attribute them to the PR head. Recheck identity and
tracked state after any execution. Ordinary PR review does not require story
packets, execution journals or story-review cycles.

Verify that the intended native role is callable. If required independent review
is unavailable, report the missing pass and its impact; do not label the main
session's analysis as independent review or claim the gate passed. An invoked role
with no actionable findings returns an empty findings list plus residual risks
and checks not run.

Consolidate results before writing the final report:

- Deduplicate root causes, preserving the best-supported severity and clearest
  evidence; do not raise severity solely because two reviewers repeated a claim.
- Combine useful remediation details without repeating the same issue.
- Preserve the finding's actual `source`; identify supporting sources when useful.
- Discard speculative, generic or unchanged-code findings outside the requested
  scope under the review standards' noise-reduction rules.

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

After showing the posting preview, obtain explicit, unambiguous natural-language
confirmation before running any GitHub write command. No magic words are required.
Carry approval for the unchanged preview through continuation without asking again.
A negative response cancels posting; an absent response leaves it pending and an
ambiguous response requires clarification. Keep the local review report available.

Only then run the previewed `gh pr review` command or `gh api` request. A changed
target, review action, or content requires a new preview and approval; mechanical
payload encoding alone does not invalidate approval for the same operation.

## Review Instructions

Use the PR review standards in this command as the source of truth for review
objectives, severity levels, finding schema, noise-reduction rules, summary
versus inline comment rules, posting safety requirements, and review
reviewer guidance.

Produce a consolidated local review report using this schema:

```markdown
## PR Review Report
- PR: <title> - <url>
- Branches: <base> <- <head>
- Review passes: <roles invoked, selected concerns and actual verification>
- Findings: <ordered by severity, with file/line when valid>
- Summary-only findings: <findings not safely mappable inline>
- Inline payload preview: <valid GitHub review comment fields only>
- Residual risks: <checks not run or confidence limits>
- Posting status: local-only | pending confirmation | posted | cancelled
```

Do not post the review to GitHub unless `--post` is present and the user gives
unambiguous confirmation after seeing the exact payload. Carry that unchanged
approval forward; do not require another confirmation on continuation.
