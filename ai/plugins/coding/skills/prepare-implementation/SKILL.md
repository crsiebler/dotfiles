---
name: prepare-implementation
description: Plan autonomous implementation of approved PRDs or bounded requirements with agent-executable acceptance checks, dependency DAG, and upfront resolution of approval gates. Planning only; does not execute the plan.
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

Honor an explicit format/target. Otherwise use the
[Markdown checklist](references/markdown-checklist.md), default PLAN.md, in every
harness. For an explicitly requested different format, preserve its supplied
schema and observable acceptance; ask only for genuinely missing format details.
Planning does not launch any controller or execution workflow.

Record approved scope/non-goals, requirement sources, stable revision and scope
baseline, story IDs/priorities, explicit dependency edges, acceptance criteria,
verification commands and recommended known agents. Missing branch/worktree
preparation or required authority blocks unattended readiness; it is not permission
to create it or defer a human gate until implementation.
Recommendations are data, not native delegation or automatic model routing.
Use [DAG construction](references/dependency-graph.md) to reject missing references,
self-dependencies and cycles. Explain ordering and integrated acceptance ownership.

### Plan for autonomous implementation

The default endpoint is implemented requirements, automated verification, required
independent agent review, and scoped local delivery. Include only agent-executable,
noninteractive verification in implementation stories and completion gates.
Do not add manual QA, human test-result confirmation, deployment verification,
production smoke tests, or stakeholder sign-off as routine implementation tasks.
Deployment or deployment verification belongs only when explicitly in scope and
automatable with authorized tools, environments and observable results.

For every verification gate, identify the command or tool-driven procedure,
inputs/fixtures, expected result and story that owns it. Existing tests, builds,
lint/typecheck and automated browser flows are suitable where relevant. New tests
or automation may be implemented as scoped work before the dependent check; they
need a feasible supported execution path, not an already-written test. An agent
running a noninteractive command is automation; a person clicking through a test
or interpreting its result is a manual dependency.

Use equivalent automation for ordinary behavioral requirements without adding an
approval gate just for choosing the test method. If a PRD or governing instruction
explicitly requires human acceptance or a non-automatable operation, identify the
conflict before launch and obtain an approved scope or method resolution. Keep
that unresolved requirement outside executable stories as a planning blocker;
never silently drop it, claim it passed, or defer it to implementation closeout.
Optional manual follow-up is outside this goal and cannot block its completion.

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
criterion text where needed, in the plan's requirement references. Do not require new source IDs or a second completion tracker.

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

## Resolve approval gates and manual prerequisites

Read [execution readiness](references/execution-readiness.md) for every plan.
Assess preparation through the requested delivery/closeout endpoint, including
applicable instructions, workflow gates, manual steps and runtime permission
prompts. Audit only the autonomous implementation scope above; do not expand it
into release operations or manual testing. Resolve foreseeable human dependencies upfront using existing authority,
verified completed prerequisites, or explicitly approved approach/scope changes.
Ask only for genuinely missing decisions or bounded approval; never re-request
unchanged grants. Planning does not perform setup or relax runtime restrictions.

Record the audit and evidence in the plan. An unresolved mandatory gate means
unattended readiness is blocked: deliver a draft with the exact required action,
not a launch-ready plan that asks the user again during implementation. Required
future-result approval cannot be satisfied by blanket advance permission. Keep
the final implementation request separate from planning; readiness grants no
authority to start. The executor rechecks readiness before edits or dispatch.

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

A later explicit user request to implement this approved plan authorizes initial
and subsequent scoped local commits unless narrower instructions exclude them.
Do not require a separate commit-approval step in the handoff. This rule does not
turn plan drafting, approval alone or a suggested launch command into execution.

Deliver the plan path/format, source coverage, story/dependency order, recommended
agents, validation, approval/manual-gate resolutions, unattended readiness and
remaining blockers. Do not launch an
execution workflow or offer a quoted command as if authorization had been granted.

For system design, load [the focused reference](references/system-design.md) only when relevant.
