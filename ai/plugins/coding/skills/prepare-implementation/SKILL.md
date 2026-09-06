---
name: prepare-implementation
description: Turn approved requirements into an ordered implementation plan.
---

# Prepare Implementation

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

Load **only the selected reference**, not both:
- `markdown-checklist`: [Markdown checklist](references/markdown-checklist.md).
- `ralph-json`: [Ralph format](references/ralph-format.md). Preserve its exact JSON
  keys/types, dependency ordering, unique IDs, `passes: false`, typecheck criterion,
  and optional named `@agent-name` hints in `notes`. Parse JSON before saving.

## Prepare, do not execute

Use supplied approved requirements and inspect relevant project instructions,
source, and existing verification commands; ask only about material gaps. Split
work into bounded, independently verifiable stories and validate against the
selected reference. Do not invent missing documentation or commands.

Preserve existing artifacts. Preview and require explicit confirmation before
destructive overwrite, archive, or reset. For approved plan continuation, update
only scoped sections, preserving checked statuses and completion evidence.

Generate the plan only: do not implement, run implementation checks, create or
switch branches, commit, launch Ralph, run a CLI goal, or automatically create a
goal. Report format/path, story order, plan validation, assumptions, and blockers;
distinguish plan checks from unrun implementation tests.
