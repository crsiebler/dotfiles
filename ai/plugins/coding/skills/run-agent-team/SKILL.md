---
name: run-agent-team
description: Execute an authorized coding plan with parallel agents, a swarm, or an agent team using the normal main session as coordinator, dependency-ready workers, isolated worktrees, and existing delivery gates. Use for explicit multi-agent coding requests or planned parallel execution; not planning-only work, simple edits, or Ralph execution.
---

# Run Agent Team

Read [requirements](references/requirements.md) and the
[team execution contract](references/team-execution.md) before execution.
Dependency setup, installation, publication and live model experiments remain
separately scoped.
Use trusted runtime identity and inspect actual native capabilities. This skill
is AI harness agnostic; no particular harness or custom primary is required.
RalphJSON remains a separate serial workflow. Do not start a new controller,
scheduler, service, or task registry.

## Harness-specific entry (conditional)

Use the active harness's supported skill-selection mechanism. Read the
[Codex CLI entry](references/codex.md) only for a Codex CLI goal/skill invocation.
For other harnesses, inspect their actual entry and native delegation controls;
never assume those CLI commands or synthesize missing tools.

## Entry and ownership

Invoke this workflow explicitly in the normal main AI session.
Do not make requirements, planning or ordinary coding methods call it implicitly.
An adequate approved story plan is required input. If missing, report the exact
input gap; do not invoke a planner or regenerate the plan. Normal coding skill
discovery applies when coding begins; no development skill or coordinator role
is an orchestration prerequisite.

The main thread is the sole integration owner and the only dispatcher. It owns
native worker/advisor/reviewer calls, version control, worktree lifecycle,
merging/conflict writes, canonical task markers, append-only progress and bounded
memory. Follow this skill directly; reading or invoking `multi-agent-coordinator`
is optional advice within the existing read-only advisor budget, never a required
primary agent or child dispatcher. No custom coordinator selection, nested
delegation or role-guidance adoption is required. Never proxy-spawn for a child,
delegate orchestration or run competing dispatch loops. Before taking over a
prior run, verify its former dispatcher is quiescent and reconcile all live
worker/reviewer IDs, assignments and consumed budgets. Uncertain ownership blocks
takeover.

## Preflight and dispatch

Use one compact capability/ownership preflight. Inspect actual callable native
worker/model/follow-up/session controls, installed pins and capacity. Require
direct worker/reviewer controls, including exact native story-reviewer selection
and same-session continuation when the risk budget specifies it. Record selection
evidence and unknown effective settings
honestly; never install settings, bypass pins or substitute a generic reviewer.
A file or role label proves no invocation capability. No capability-probe agents.

Keep the current main session for coordination. Preferred models are
`gpt-6.1-sol` for coordination, `gpt-6-luna` for implementation and `gpt-6-astra`
for review, conflict analysis, architecture and cross-domain analysis. These are
preferences, not execution prerequisites. Follow the fallback and explicit-user
constraint rules in [runtime selection](references/runtime-selection.md).
Unknown coordinator model telemetry or a different installed reviewer model alone
does not block execution. Preserve the exact native reviewer role and all gates;
never change roles to obtain a preferred model. Stay within existing
advisor/review/remediation allowances and actual model-use scope. Do not silently
switch the main thread's model or install settings.
A model change does not reset review attempts, add a second gate or grant an
autonomous retry. Role definitions remain reusable without model pins.

Default to two implementation workers; honor narrower user limits and actual
runtime/resource capacity. Count all occupied sessions using the runtime's actual
open/active semantics. Reserve a required review slot or verify
supported release of a completed handed-off worker before review. Never close a
live writer or a reviewer needed for the permitted same-session targeted pass.

When two or more eligible independent substantial coding tasks exist and the
grant, resources and capacity permit, dispatch at least two before waiting for
results. Refill available capacity from ready tasks. Do not split tiny work merely
to manufacture parallelism. Serial exceptions require an exact recorded reason:
dependency chain, overlapping ownership, exclusive resource, insufficient capacity,
unavailable capability/authority, or work too small for useful partitioning.
Dispatch-before-wait is the operational rule; observed wall-clock overlap is a
separate verification result.

## Execute and deliver

Read this bundle's [story delivery](references/story-execution.md), complete
[review protocol](references/story-review.md),
[concurrency](references/task-concurrency.md) and
[runtime selection](references/runtime-selection.md) contracts. Resolve resources
relative to this advertised installed bundle. Delivery and review belong to
this team workflow; no planning or alternative execution workflow is invoked.
At full completion discover archive-run for its executable archival capability;
resolve its helper/API contract from that loaded bundle, never sibling paths.
For enrolled runs, verify/bind metadata before the first checkpoint under actual
scoped authority; preserve existing manifests. Planning remains independent.

The Markdown checklist workflow uses the existing approved checklist and explicit prepared
branch, rejecting main/master/detached HEAD. The main thread validates missing
references, self-dependencies and cycles, then prepares clean task worktrees
under its lifecycle grant. Workers edit/check only assigned roots/paths.
The main thread owns admission, integration and shared state.
Never invoke Ralph or its runner from this workflow.

Read the exact existing approved plan and revision. Preserve story IDs, dependency
edges, acceptance criteria and completed evidence. Validate all references,
self-dependencies and cycles; use Kahn-style readiness ordered by priority then
document order. Release a predecessor only after verified integration checks,
bounded review and its authorized integration commit. A worker result or isolated
branch commit never satisfies that dependency.

Require clean committed task worktrees with explicit absolute paths, exact
non-main branches, approved full bases containing delivered prerequisites and
nonoverlapping owned paths. Verify actual containment, including symlinks, before
writes. Do not assume native spawn allocates a worktree or binds cwd; inspect
actual controls and verify the assigned root before writes. Use assigned paths
and working directories for files, Git and checks. Never copy dirty work to make a baseline.
Use private outputs and existing project controls for shared builds/caches/host
resources; serialize conflicts if exclusion cannot be established.

Integrate one bounded candidate at a time through the shared checks and risk-based
review. Use permitted self-review only where that budget allows; otherwise directly
invoke exact native `story-reviewer` with the full protocol/profile and preserve
its session.
Allow one initial and at most one targeted pass per attempt. Do not add a worker
staged review, extra coordinator approval or reviewer-of-reviewer cycle. Follow
pre-commit evidence and provisional marker finalization; report delivered completion
only after a successful authorized integration commit. Keep evidence in progress,
not plan narratives or a new registry.

On failure, preserve candidate/history and block its dependent subgraph; continue
only safely isolated eligible work. Reconcile uncertain spawn/results through
native session state before any retry. Never duplicate a possibly-live owner.
Resume from observed plan revision, roots/branches/bases, live IDs, delivery
commits, reviewer session/passes and resource ownership. Take over prior dispatch
only after its owner is quiescent and the handoff is reconciled. Dispatch,
integration and canonical state remain owned by the main thread. Apply the
persistent blocker gate before further story work or review. Persistent
final review blockers require material-resolution evidence, not a new agent/model.

After the entire goal is delivered and writers are quiescent, perform required
archival under the shared contract and actual authority. Report pending closeout
rather than fabricating success. No implicit push, post, install, deployment,
worktree removal or global configuration change.

Report actual dispatch/integration owners, task/session/model selection evidence,
parallel/serial decisions, worktree/base/path assignments, delivered commits,
checks/review, preserved blockers and archival status. Use
[verification](references/verification.md) for evaluation and activation gates.
