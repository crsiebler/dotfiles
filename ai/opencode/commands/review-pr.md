---
name: review-pr
description: Review a GitHub pull request with OpenCode specialist reviewers
---

# Review Pull Request

Review a GitHub pull request using OpenCode specialist reviewers and local
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

Use these standards for all specialist PR review passes and for the consolidated
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
  "source": "code-reviewer|qa-expert|security-engineer|security-auditor|documentation-engineer|compliance-auditor|ui-designer|ux-researcher|summary"
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

### Specialist Reviewer Guidance

- `code-reviewer`: Focus on correctness, maintainability, error handling, API
  contracts, concurrency, data flow, and project conventions. Prioritize defects
  that can be shown from the diff and local code context.
- `qa-expert`: Focus on missing or weak tests, brittle assertions, fixture gaps,
  regression risk, and validation coverage. Only report missing tests when the
  behavior is important enough to justify a required change.
- `security-engineer`: Use when the diff touches secure coding risk, subprocess
  or shell execution, filesystem mutation, network calls, secrets or environment
  variables, authentication, authorization, permissions, encryption, dependency
  changes, deserialization, parsing untrusted input, logging sensitive values,
  or deployment/configuration surfaces. Focus on implementation-level security
  defects. Do not use for local-only scripts, tests, docs, formatting, or
  refactors unless one of these risk surfaces is present.
- `security-auditor`: Use only for deeper security, compliance, or policy review
  when the diff touches authentication, authorization, secrets, credential
  handling, dependency or supply-chain risk, deployment, regulated data,
  auditability, trust boundaries, or externally reachable behavior. Do not run
  both security reviewers unless the change is explicitly security-sensitive or
  high-risk.
- `documentation-engineer`: Use when the diff changes user-facing behavior,
  commands, APIs, environment variables, configuration, installation, or
  operational behavior. Focus on stale, missing, or misleading docs that would
  affect users or operators.
- `compliance-auditor`: Use when the diff touches PII, PHI, financial data,
  retention, consent, audit trails, licensing, accessibility, or regulated
  workflows. Focus on compliance obligations, evidence, policy alignment, and
  merge-blocking gaps.
- `ui-designer`: Use when frontend components, pages, layouts, routes,
  templates, styles, design tokens, icons, images, animations, interaction
  behavior, accessibility-relevant markup, responsive behavior, or
  rendering-related frontend dependencies/configuration changed. It must load and
  use the `dev-browser` skill to verify affected flows for UX quality,
  accessibility, visual consistency, responsive behavior, interaction clarity,
  and industry best practices. Do not use for backend-only code, local-only
  scripts, CLIs, tests, docs, comments, logging, formatting, or refactors with no
  rendered UI impact.
- `ux-researcher`: Use when user flows, task completion paths, navigation,
  forms, modals, onboarding, dashboards, validation messages, empty/error/loading
  states, accessibility-affecting behavior, responsive behavior, or user-facing
  copy changed. It must load and use the `dev-browser` skill to verify the
  changed frontend experience for UX standards, accessibility, flow consistency,
  usability heuristics, and industry best practices. Do not use for internal
  implementation changes that do not alter visible behavior or interaction flow.

## Specialist Subagent Workflow

Run specialist review passes against the gathered PR context before producing
the consolidated report. OpenCode's subagent system handles the specialist work;
do not call model provider APIs directly.

Delegation contract:

- The primary agent gathers PR context, selects specialists, and consolidates
  findings.
- Specialist passes must be invoked through OpenCode's Task/subagent mechanism
  when available.
- If a required specialist is unavailable, disclose that the pass was skipped or
  simulated and lower confidence in the residual risks.
- Do not silently replace specialist review with generic primary-agent analysis.

Always run these default specialist passes:
- `code-reviewer`: correctness, maintainability, error handling, API contracts,
  data flow, and project conventions.
- `qa-expert`: missing or weak tests, brittle assertions, fixture gaps,
  regression risk, and validation coverage.

Conditionally add these specialist passes when the changed file list or diff
content indicates their domain is relevant:
- `security-engineer`: include when files or diff content touch secure coding
  risk, subprocess or shell execution, filesystem mutation, network calls,
  secrets or environment variables, authentication, authorization, permissions,
  encryption, dependency changes, deserialization, parsing untrusted input,
  logging sensitive values, or deployment/configuration surfaces. Do not run for
  local-only scripts, tests, docs, formatting, or refactors unless one of these
  risk surfaces is present.
- `security-auditor`: include only for deeper security, compliance, or policy
  review when files or diff content touch authentication, authorization, secrets,
  credential handling, dependency or supply-chain risk, deployment, regulated
  data, auditability, trust boundaries, or externally reachable behavior. Do not
  run both `security-engineer` and `security-auditor` unless the change is
  explicitly security-sensitive or high-risk.
- `documentation-engineer`: include when files or diff content touch
  user-facing behavior, commands, APIs, environment variables, configuration,
  installation, or operational behavior.
- `compliance-auditor`: include when files or diff content touch PII, PHI,
  financial data, retention, consent, audit trails, licensing, accessibility,
  or regulated workflows.
- `ui-designer`: include when frontend components, pages, layouts, routes,
  templates, styles, design tokens, icons, images, animations, interaction
  behavior, accessibility-relevant markup, responsive behavior, or
  rendering-related frontend dependencies/configuration changed. It must load and
  use the `dev-browser` skill to verify affected flows for UX quality,
  accessibility, visual consistency, responsive behavior, interaction clarity,
  and industry best practices. Do not run for backend-only code, local-only
  scripts, CLIs, tests, docs, comments, logging, formatting, or refactors with no
  rendered UI impact.
- `ux-researcher`: include when user flows, task completion paths, navigation,
  forms, modals, onboarding, dashboards, validation messages, empty/error/loading
  states, accessibility-affecting behavior, responsive behavior, or user-facing
  copy changed. It must load and use the `dev-browser` skill to verify the
  changed frontend experience for UX standards, accessibility, flow consistency,
  usability heuristics, and industry best practices. Do not run for internal
  implementation changes that do not alter visible behavior or interaction flow.

Specialist selection must be strict. For low-risk local code changes, run only
`code-reviewer` and `qa-expert`. Optional specialists should be added only when
their trigger conditions are clearly present in the changed files or diff.

For each specialist pass, provide the PR metadata, changed file summary, diff,
commits, repository instructions, and PR review standards. Require every
specialist to return findings using the shared finding schema from the standards.
If a specialist has no actionable findings, it should explicitly return
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
  not satisfy the PR review standards' noise-reduction rules.

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

Use the PR review standards in this command as the source of truth for review
objectives, severity levels, finding schema, noise-reduction rules, summary
versus inline comment rules, posting safety requirements, and specialist
reviewer guidance.

Produce a consolidated local review report using this schema:

```markdown
## PR Review Report
- PR: <title> - <url>
- Branches: <base> <- <head>
- Specialist passes: <agents used and why>
- Findings: <ordered by severity, with file/line when valid>
- Summary-only findings: <findings not safely mappable inline>
- Inline payload preview: <valid GitHub review comment fields only>
- Residual risks: <checks not run or confidence limits>
- Posting status: local-only | pending confirmation | posted | cancelled
```

Do not post the review to GitHub unless `--post` is present and the user gives
one of the accepted confirmation values after seeing the exact payload.
