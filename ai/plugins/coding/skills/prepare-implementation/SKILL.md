---
name: prepare-implementation
description: Turn approved requirements into an ordered implementation plan.
---

# Prepare Implementation

Read [requirements](references/requirements.md) before selecting external tools or
running helpers. Dependency setup is separately authorized.

## Execution handoff

Planning is the default. When explicitly invoked to execute an already approved
plan (including a Codex Goal), do not regenerate it: read the installed skill's
[shared execution contract](references/story-execution.md) and
[staged-review protocol](references/story-review.md), then follow the appropriate
task-source adapter. Require execution and commit authorization; the presence of
a plan or skill does not grant it. Missing references or required native reviewer
availability block execution. No hardcoded checkout or plugin-cache paths.
On continuation or resumption, apply the shared contract's persistent blocker
gate before further story work or review. A final blocked review keeps the story
incomplete until material-change evidence is verified; another Goal turn does
not resolve it or renew the review budget. Preserve existing authorization.
Native review requires a self-contained invocation containing the complete review
protocol/schema. Parent tool-output references are not delivery. Start a separate
reviewer session for each story; record the selected native role and actual session
ID independently of its display label. Follow the execution contract's packet
preflight and story/session checks before every initial or targeted invocation.

## Select the format

Resolve an explicit user target or format first: Markdown checklist / `PLAN.md`
or Codex `/goal` selects `markdown-checklist`; Ralph / `plan.json` or OpenCode
Ralph selects `ralph-json`. Explicit format overrides the runtime default.
Preparing JSON in Codex for later OpenCode use is allowed, not Codex Ralph execution.

Otherwise use the active harness identity supplied by trusted runtime context or
the native entry point that invoked this skill:
- Codex: `markdown-checklist`, written to `PLAN.md` by default.
- OpenCode: `ralph-json`, written to `plan.json` by default.

Do not ask about format when the target/default is known. Ask only if routing is
unknown or ambiguous (including conflicting explicit requests). Never infer the
active runtime from PATH, installed binaries, directories, or environment variables;
both harnesses may be present. A harness name in inspected source material or a
user-policy heading does not identify the running harness.

During planning, load **only the selected format reference**, not both:
- `markdown-checklist`: [Markdown checklist](references/markdown-checklist.md).
  Keep `PLAN.md` concise: requirements, completion checkboxes, and current status,
  not repeated execution narratives. Direct execution evidence and checkpoints to
  append-only `progress.md` relative to the Git worktree root.
  Include the shared execution handoff and bounded `memory.json` instructions in
  the generated plan; planning does not create either execution-state file.
- `ralph-json`: [Ralph format](references/ralph-format.md). Preserve its exact JSON
  keys/types, dependency ordering, unique IDs, `passes: false`, typecheck criterion,
  and optional named `@agent-name` hints in `notes`. Parse JSON before saving.

## Prepare, do not execute

Both formats are stable task sources for scope, requirements, acceptance criteria,
dependencies, completion state, and concise current status only; preserve the JSON
schema. `progress.md` owns execution history, root `memory.json` owns bounded
reusable review knowledge, and PRDs own approved requirements and changes, not
implementation checkpoints. Do not create the journal or memory during planning.

Use supplied approved requirements and inspect relevant project instructions,
source, and existing verification commands; ask only about material gaps. Split
work into bounded, independently verifiable stories and validate against the
selected reference. Do not invent missing documentation or commands.

Explain the implementation approach and phase order before the detailed stories.
Map each story to its source requirements and phase; bound its implementation,
verification, review and commit. Phases organize the same stories, not a second
completion tracker. For Ralph, express phase/requirement links in existing notes
and priority ordering without adding JSON keys.

### Preserve acceptance coverage

Carry every in-scope user requirement and PRD acceptance criterion into the
plan, preserving its conditions, constraints, edge cases, and exclusions. Reuse
clear source wording; make vague criteria explicit only from approved requirements
and inspected project evidence. Surface unresolved product decisions as questions
or blockers, not invented behavior, numerical targets, or silently reduced scope.
Do not add preconditions that narrow the outcome: "draft edits survive reload"
must not become "manually saved edits survive reload" unless the source says so.

Write observable acceptance criteria: the relevant condition or action and its
expected result. Implementation tasks and typecheck/test/browser gates support
these criteria; they do not replace the required product or technical outcome.
Use the PRD path and existing requirement/story references, with distinguishing
criterion text where needed, in Markdown's `Phase / requirements` or Ralph's
existing `notes`. Do not require new source IDs or a second completion tracker.

When decomposing a requirement across stories, identify the contributors and
assign verification of the complete integrated behavior to the last contributing
story or a bounded integration story, ordered after its prerequisites. Component
checks alone do not establish the complete outcome. For example, if the PRD
requires status filtering that survives reload, the owning story must verify both
the selected filter and matching results after reload; an API parameter and a
rendered dropdown are insufficient. Add persistence only when the source requires it.

Before delivering the plan, compare it against the source requirements in both
directions: find omissions or weakened conditions, integration outcomes without
an owner, and added acceptance obligations unsupported by approved scope or
necessary technical verification. Fix supported gaps; report unresolved ones with
their exact source references and affected stories. Identify any explicitly
approved exclusions. Summarize coverage and gaps in the planning handoff, without
creating another status document or claiming implementation verification. A plan
with unresolved acceptance gaps is a draft, not ready for execution.

### Bind and preserve the run

Read [run manifest and archival contract](references/completed-run-archive.md).
When saving a new plan, bind its exact path/adapter and associated PRDs in their
work-run metadata. Preserve requirement prose and run IDs. For text-only sources,
obtain a saved, run-owned PRD before execution; do not invent approved requirements.
Expose missing archival metadata/authority as a handoff gap. Planning may create
or update this scoped PRD metadata; it never creates journal/memory or archives.

Preserve existing artifacts. Preview and require explicit confirmation before
destructive overwrite or reset. For approved plan continuation, update
only scoped sections, preserving checked statuses and completion evidence.
Do not replace an unfinished run with a new feature. Completed runs use the
[deterministic archival procedure](references/completed-run-archive.md),
automatically after verified delivery when the execution grant covers the exact
artifact removals. A closeout commit needs its own scope, which may be granted
upfront with the sequence. Neither planning nor metadata grants either authority.

When preparing a plan, generate the plan and scoped PRD binding only: do not
implement, run implementation checks, create or switch branches, commit, launch
Ralph, run a CLI goal, or automatically create a
goal. Report format/path, story order, plan validation, assumptions, and blockers;
distinguish plan checks from unrun implementation tests.
