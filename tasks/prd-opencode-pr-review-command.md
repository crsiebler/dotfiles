# PRD: OpenCode PR Review Command

## Introduction

Add an OpenCode-powered `/review-pr` command that replicates GitHub Copilot automated pull request reviews using OpenCode's existing provider/model infrastructure. The command should run from within OpenCode, gather pull request context with Git and GitHub CLI, execute a tiered set of specialist subagent reviews, generate high-signal findings, support inline GitHub review comments, and only post to GitHub after explicit user confirmation.

This feature replaces the user's soon-to-be unavailable GitHub Copilot automated PR review workflow while preserving manual control, review quality, and safety.

## Goals

- Provide a manual `/review-pr` OpenCode command that detects the current branch's pull request by default.
- Generate Copilot-style PR reviews using OpenCode and the configured provider/model layer, without calling OpenAI directly from scripts or commands.
- Use specialist subagents to improve review coverage while minimizing noisy comments.
- Support GitHub inline line comments in the first implementation by validating findings against PR diff lines.
- Support optional GitHub posting with a full preview and explicit confirmation before any `gh` command mutates GitHub state.
- Produce reusable prompt instructions that are clear, structured, and suitable for future refinement.

## User Stories

### US-001: Add Reusable PR Review Prompt
**Description:** As an OpenCode user, I want a reusable PR review prompt file so that the review behavior is consistent across repositories and command invocations.

**Acceptance Criteria:**
- [ ] Add a reusable markdown prompt file for PR review behavior.
- [ ] Prompt defines review objectives, severity levels, finding schema, noise-reduction rules, and posting safety requirements.
- [ ] Prompt explicitly states that OpenCode's provider/model layer handles AI execution and no direct OpenAI API calls are made by the command.
- [ ] Prompt includes rules for summary findings versus inline comments.
- [ ] Prompt includes specialist subagent instructions for `code-reviewer`, `qa-expert`, `security-engineer`, `security-auditor`, `documentation-engineer`, and `compliance-auditor`.
- [ ] `make -n install` succeeds.

### US-002: Add `/review-pr` Command
**Description:** As an OpenCode user, I want to run `/review-pr` from a PR branch so that OpenCode reviews the pull request without requiring me to paste the PR URL.

**Acceptance Criteria:**
- [ ] Add an OpenCode command file for `/review-pr`.
- [ ] With no argument, the command detects the PR for the current branch using `gh pr view`.
- [ ] The command accepts a PR number argument, for example `/review-pr 123`.
- [ ] The command accepts a PR URL argument, for example `/review-pr https://github.com/owner/repo/pull/123`.
- [ ] If no PR can be detected, the command asks the user to provide a PR number or URL instead of guessing.
- [ ] The command gathers PR title, body, URL, base branch, head branch, changed files, commits, and diff.
- [ ] The command reads the reusable PR review prompt.
- [ ] `make -n install` succeeds.

### US-003: Run Tiered Specialist Subagent Reviews
**Description:** As an OpenCode user, I want the command to use multiple specialist subagents so that the review catches correctness, test, security, documentation, and compliance issues without unnecessary noise.

**Acceptance Criteria:**
- [ ] The default review always includes `code-reviewer`, `qa-expert`, and `security-engineer` review passes.
- [ ] The command conditionally includes `security-auditor` when changed files or diff content touch authentication, authorization, secrets, dependencies, inputs, networking, file access, logging, or trust boundaries.
- [ ] The command conditionally includes `documentation-engineer` when changed files or diff content touch user-facing behavior, commands, APIs, environment variables, configuration, installation, or operational behavior.
- [ ] The command conditionally includes `compliance-auditor` when changed files or diff content touch PII, PHI, financial data, retention, consent, audit trails, licensing, accessibility, or regulated workflows.
- [ ] Each subagent returns findings using the shared finding schema.
- [ ] The orchestrator deduplicates findings with the same root cause.
- [ ] The orchestrator keeps the highest severity when merging duplicate findings.
- [ ] `make -n install` succeeds.

### US-004: Generate Valid Inline Review Comments
**Description:** As an OpenCode user, I want review findings to appear as GitHub inline line comments when possible so that authors can see actionable feedback directly on the changed code.

**Acceptance Criteria:**
- [ ] The command parses the PR diff and builds a map of valid commentable lines per changed file.
- [ ] Findings intended for inline comments include `path`, `line`, `side`, and `body` fields compatible with GitHub's pull request review API.
- [ ] Added or modified lines map to `side: "RIGHT"`.
- [ ] Deleted lines map to `side: "LEFT"`.
- [ ] Findings that do not map to valid diff-visible lines are moved to the consolidated summary instead of being posted inline.
- [ ] The command supports multi-line comment fields only when both start and end lines map to valid diff-visible lines.
- [ ] The command previews the inline review payload before posting.
- [ ] The command does not post malformed or unmappable inline comments.
- [ ] `make -n install` succeeds.

### US-005: Preview and Confirm GitHub Posting
**Description:** As an OpenCode user, I want to review exactly what will be posted to GitHub before anything is submitted so that accidental comments or incorrect reviews are avoided.

**Acceptance Criteria:**
- [ ] By default, `/review-pr` generates a local review report and does not post to GitHub.
- [ ] When run with `--post`, the command prepares a GitHub review but does not submit it immediately.
- [ ] Before posting, the command shows the PR URL, review event, consolidated review body, inline comment count, and exact `gh` command or API payload.
- [ ] The command asks for explicit confirmation before posting.
- [ ] Accepted confirmation values include `yes`, `y`, `confirm`, `post it`, or `go ahead`.
- [ ] Ambiguous or negative responses do not post anything.
- [ ] The command uses `gh pr review` or `gh api` only after confirmation.
- [ ] `make -n install` succeeds.

### US-006: Install Review Command Assets
**Description:** As a dotfiles maintainer, I want the review command assets installed with the rest of the OpenCode configuration so that the command is available after running `make install`.

**Acceptance Criteria:**
- [ ] `make install` installs the reusable PR review prompt to `$HOME/.config/opencode/`.
- [ ] Existing command installation copies `/review-pr` into `$HOME/.config/opencode/commands/`.
- [ ] Installation backs up any overwritten prompt file with a timestamped backup when applicable.
- [ ] README documents the `/review-pr` command, arguments, required tools, and posting behavior.
- [ ] AGENTS.md documents the install and cleanup behavior if backup or cleanup targets change.
- [ ] `make -n install` succeeds.

## Functional Requirements

- FR-1: The system must provide an OpenCode command named `/review-pr`.
- FR-2: The command must run entirely within OpenCode's infrastructure and must not directly call OpenAI APIs.
- FR-3: The command must use the currently configured OpenCode provider/model unless a future explicit agent override is configured.
- FR-4: The command must detect the current branch PR with `gh pr view` when no PR argument is provided.
- FR-5: The command must accept a PR number argument.
- FR-6: The command must accept a PR URL argument.
- FR-7: The command must gather PR metadata, changed files, commits, and diff before reviewing.
- FR-8: The command must use a reusable markdown prompt file for review standards and output requirements.
- FR-9: The default specialist review set must include `code-reviewer`, `qa-expert`, and `security-engineer`.
- FR-10: The command must conditionally run `security-auditor`, `documentation-engineer`, and `compliance-auditor` based on changed files and diff content.
- FR-11: All subagent findings must use a shared schema with severity, confidence, category, file, line, title, evidence, recommendation, and inline comment fields.
- FR-12: The orchestrator must deduplicate findings before generating final output.
- FR-13: The orchestrator must suppress low-value findings such as style-only preferences, formatter issues, speculative rewrites, and duplicate comments.
- FR-14: The command must parse PR diff hunks to determine valid GitHub inline comment targets.
- FR-15: The command must only create inline comments for findings that map to valid diff-visible lines.
- FR-16: The command must move unmappable findings into the consolidated review summary.
- FR-17: The default command behavior must generate a local review report only.
- FR-18: The command must support a `--post` option for GitHub posting.
- FR-19: The command must preview the review body, inline comments, and exact posting command or payload before posting.
- FR-20: The command must require explicit user confirmation before posting to GitHub.
- FR-21: The command must avoid external temporary directories and use the current working directory for any temporary review files.
- FR-22: Temporary review files must be cleaned up after command completion unless the user requests preserving them for debugging.

## Non-Goals

- This feature will not add a GitHub Actions workflow for automatic PR reviews.
- This feature will not run reviews outside OpenCode's command infrastructure.
- This feature will not implement direct OpenAI API calls or manage `OPENAI_API_KEY` inside the command.
- This feature will not automatically approve, request changes, or comment on PRs without user confirmation.
- This feature will not replace existing `code-review-analyzer` or `code-review-resolver` skills.
- This feature will not resolve review threads automatically.
- This feature will not guarantee inline comments for findings that do not map to changed diff lines.
- This feature will not force all specialist subagents to run on every PR.

## Design Considerations

- The default workflow should be safe and review-only: `/review-pr` generates output but does not post.
- The generated review should prioritize findings over summary prose.
- The review should resemble a senior engineer's concise PR review, not a broad code-quality audit.
- Inline comments should be short, specific, and actionable.
- Consolidated summary comments should capture broad or cross-file issues.
- The prompt should explicitly discourage noise, subjective style comments, and issues already covered by linters or formatters.

## Technical Considerations

- The command depends on GitHub CLI (`gh`) being installed and authenticated.
- The command depends on being run inside a Git repository with a GitHub remote.
- Posting inline comments requires the GitHub pull request review API because `gh pr review` does not provide complete control over multiple inline comments.
- GitHub inline comments require valid diff positions or valid `line` and `side` values for changed lines.
- The command should prefer consolidated comments when line mapping is uncertain.
- Any generated temporary payload files should be created under the current working directory to avoid OpenCode permission prompts.
- If Makefile install behavior changes, backup and cleanup documentation should remain in sync with README.md and AGENTS.md.

## Success Metrics

- Running `/review-pr` from a PR branch detects the correct PR without requiring a URL.
- Review output contains actionable findings with fewer than 10% low-value or duplicate comments in normal use.
- Inline comments post only to valid changed lines and do not fail due to malformed review payloads.
- `/review-pr --post` never mutates GitHub state without explicit confirmation.
- The command can be installed with `make install` and verified with `make -n install`.
- The generated review is useful enough to replace the user's GitHub Copilot automated PR review workflow for manual OpenCode-driven reviews.

## Open Questions

- Which OpenCode model should be preferred for this workflow if the active session model is not suitable for code review?
- Should a dedicated `pr-code-reviewer` agent be added later to force a specific model and permissions?
- Should the command preserve review payload files when GitHub posting fails for easier debugging?
- Should the command support flags such as `--summary-only`, `--inline-only`, `--security`, or `--no-post-cleanup` in a later iteration?
- Should an approval-style review event ever be supported, or should the command only post `COMMENT` and `REQUEST_CHANGES` events?
