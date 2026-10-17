---
name: prepare-implementation
description: Turn approved requirements into an ordered implementation plan with stories, acceptance criteria, dependency DAG, and recommended agents. Planning only; does not execute the plan or invoke another coding workflow.
---

# Prepare Implementation

Read [requirements](references/requirements.md). Use approved PRDs or a supplied
bounded-task brief, relevant repository evidence and actual verification commands.
Create the story list, preserve observable acceptance, validate the dependency DAG,
and recommend suitable known custom agents for each task. Do not choose runtime
models, dispatch workers, create execution state or invoke an execution skill.
A request to execute an existing plan is outside this planning skill; leave the
plan intact and report that boundary rather than regenerate it or route implicitly.

## Scale and format

For clear small work, carry the approved request/brief directly into the plan;
a separate PRD and phase narrative are optional. Larger work links approved PRDs,
source criteria, phases where useful and integration acceptance owners. Neither
path may weaken acceptance coverage or invent approved scope.

Honor an explicit format/target. Otherwise trusted Codex runtime context selects
[Markdown checklist](references/markdown-checklist.md), default PLAN.md; trusted
OpenCode context selects [Ralph JSON](references/ralph-format.md), default plan.json.
Read only the selected format reference. Ask only when routing is unknown or
conflicting; never infer the active runtime from PATH, directories or binaries.
Preparing Ralph JSON in Codex is allowed and does not execute Ralph.

Record approved scope/non-goals, requirement sources, stable revision and scope
baseline, story IDs/priorities, explicit dependency edges, acceptance criteria,
verification commands and recommended known agents. Missing branch/worktree
preparation or execution authority is a handoff gap, not permission to create it.
Recommendations are data, not native delegation or automatic model routing.
Use [DAG construction](references/dependency-graph.md) to reject missing references,
self-dependencies and cycles. Explain ordering and integrated acceptance ownership.

### Preserve acceptance coverage

Carry every in-scope user requirement and any PRD acceptance criterion into the
plan, preserving its conditions, constraints, edge cases, and exclusions. Reuse
clear source wording; make vague criteria explicit only from approved requirements
and inspected project evidence. Surface unresolved product decisions as questions
or blockers, not invented behavior, numerical targets, or silently reduced scope.
Do not add preconditions that narrow the outcome: "draft edits survive reload"
must not become "manually saved edits survive reload" unless the source says so.

Write observable acceptance criteria: the relevant condition or action and its
expected result. Implementation tasks and typecheck/test/browser gates support
these criteria; they do not replace the required product or technical outcome.
Use the approved request/brief or PRD path and existing requirement/story references,
with distinguishing
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

## Preserve plans and lifecycle data

Planning creates no progress.md or memory.json, runs no implementation tests,
creates/switches no branches/worktrees, and makes no commits. Put execution history
in neither the plan nor PRD. Preserve existing completed markers and evidence on
approved in-place revisions; scope/dependency changes need reconciliation against
actual approval and existing delivery evidence.

Before saving a different plan at an occupied path, require verified preservation
of the previous completed plan and its associated evidence. Inspect archive receipt
and source hashes; if archival was missed, leave the previous plan intact and
report the exact preservation action needed before replacement. Failed or missing
preservation blocks the new-plan write. Never replace an unfinished run, fabricate
completion or execute cleanup as a planning side effect. A verified archive is
required before replacement, not an optional plan-generation convenience.

For a full-run archival-enrolled plan, planning may preserve supplied lifecycle metadata
under [run manifest data](references/run-manifest.md), preserving existing IDs and
approved requirement prose. This records artifact ownership only; it grants no
execution, removal or closeout commit authority. A separate PRD/manifest remains
optional for a bounded task; the prior-plan preservation obligation still applies.

Deliver the plan path/format, source coverage, story/dependency order, recommended
agents, validation, assumptions and unresolved handoff gaps. Do not launch an
execution workflow or offer a quoted command as if authorization had been granted.
