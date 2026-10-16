---
name: run-agent-team
description: Execute an authorized Codex coding plan with parallel agents, a swarm, or an agent team using one coordinator, dependency-ready workers, isolated worktrees, and existing delivery gates. Use for explicit multi-agent coding requests or planned parallel execution; not planning-only work, simple edits, or Ralph execution.
---

# Run Agent Team

Read [requirements](references/requirements.md) and the
[Codex team contract](references/codex.md) before execution. Dependency setup,
installation, publication and live model experiments remain separately scoped.
Use trusted runtime identity; this execution adapter is Codex-only. RalphJSON
remains serial. Do not start a new controller, scheduler, service, or task registry.

## Entry and ownership

Invoke this workflow explicitly or from an assigned multi-agent-coordinator.
Do not make requirements, planning or ordinary coding methods call it implicitly.
An adequate approved story plan is required input. If missing, report the exact
input gap; do not invoke a planner or regenerate the plan. Normal coding skill
discovery applies when coding begins; no particular development skill is an
orchestration prerequisite.

The main thread is the sole integration owner. It owns version control, worktree
lifecycle, merging/conflict writes, canonical task markers, append-only progress
and bounded memory. Establish exactly one dispatcher: prefer the existing native
`multi-agent-coordinator`, explicitly selected on `gpt-6.1-sol`, for team execution
with supported nested delegation. The main thread hands it the approved plan and
bounded dispatch authority, then integrates its returned candidates. It does not
run a competing worker/reviewer dispatch loop. The coordinator dispatches workers
and requested advisors/reviewers but cannot write Git or canonical task state.

If exact coordinator invocation/model selection or nested delegation is unavailable,
a verifiably selected Sol main thread may adopt the discovered coordinator guidance
and dispatch direct workers itself. Disclose guidance adoption rather than native
role invocation. This fallback needs all required worker/reviewer controls and
actual grants; do not switch the main thread's model or install settings silently.
Never proxy-spawn for a child, recursively create coordinators, or run two dispatchers.
Before transfer, verify the old dispatcher is quiescent and reconcile all live
worker/reviewer IDs, assignments and consumed budgets. Uncertain ownership blocks
transfer; unavailable fallback prerequisites block affected execution.

## Preflight and dispatch

Use one compact capability/ownership preflight. Inspect actual callable native
role/model/follow-up controls, installed pins, nesting support and capacity.
Delegated mode requires exact coordinator selection on Sol, supported nested
workers/reviewers and a bounded nesting/delegation grant. Main-thread fallback
requires observed Sol selection and direct worker/reviewer controls. Both require
exact native story-reviewer selection and same-session continuation when the risk
budget specifies it. Record selection evidence and unknown effective settings
honestly; never install settings, bypass pins or substitute a generic reviewer.
A file or role label proves no invocation capability. No capability-probe agents.

Select `gpt-6-luna` explicitly for implementation workers. Use `gpt-6-astra` for
reviews, conflict analysis, architecture and cross-domain analysis under [runtime selection](references/runtime-selection.md), within existing
advisor/review/remediation allowances and actual model-use scope. Keep the
dispatcher on Sol; preserve the main thread's selected model in delegated mode.
A model change does not reset review attempts, add a second gate or grant an
autonomous retry. Role definitions remain reusable without model pins.

Default to two implementation workers; honor narrower user limits and actual
runtime/resource capacity. Count management and other occupied sessions using the
runtime's actual open/active semantics. Reserve a required review slot or verify
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
[concurrency](references/codex-concurrency.md) and
[runtime selection](references/runtime-selection.md) contracts. Resolve resources
relative to this advertised installed bundle. Delivery and review are tailored to
Codex; no planning or alternative execution workflow is invoked.
At full completion discover archive-run for its executable archival capability;
resolve its helper/API contract from that loaded bundle, never sibling paths.
For enrolled runs, verify/bind metadata before the first checkpoint under actual
scoped authority; preserve existing manifests. Planning remains independent.

CodexGoalMarkdown uses the existing approved checklist and explicit prepared
branch, rejecting main/master/detached HEAD. The dispatcher validates missing
references, self-dependencies and cycles; the main thread prepares clean task
worktrees under its lifecycle grant. Workers edit/check only assigned roots/paths.
The dispatcher owns admission; the main thread owns integration and shared state.
Never invoke Ralph or its runner from this workflow.

Read the exact existing Codex plan and revision. Preserve story IDs, dependency
edges, acceptance criteria and completed evidence. Validate all references,
self-dependencies and cycles; use Kahn-style readiness ordered by priority then
document order. Release a predecessor only after the main thread acknowledges verified
integration checks, bounded review and its authorized integration commit. A worker result or isolated
branch commit never satisfies that dependency.

Require clean committed task worktrees with explicit absolute paths, exact
non-main branches, approved full bases containing delivered prerequisites and
nonoverlapping owned paths. Verify actual containment, including symlinks, before
writes. Native spawn neither allocates a worktree nor binds cwd. Use assigned
paths/workdir for files, Git and checks. Never copy dirty work to make a baseline.
Use private outputs and existing project controls for shared builds/caches/host
resources; serialize conflicts if exclusion cannot be established.

Integrate one bounded candidate at a time through the shared checks and risk-based
review. Use permitted self-review only where that budget allows; otherwise supply the dispatcher with the
full protocol/profile for exact native `story-reviewer` and preserve its session.
Allow one initial and at most one targeted pass per attempt. Do not add a worker
staged review, extra coordinator approval or reviewer-of-reviewer cycle. Follow shared
pre-commit evidence and provisional marker finalization; report delivered completion
only after successful authorized integration commit. Keep evidence in progress,
not plan narratives or a new registry.

On failure, preserve candidate/history and block its dependent subgraph; continue
only safely isolated eligible work. Reconcile uncertain spawn/results through
native session state before any retry. Never duplicate a possibly-live owner.
Resume from observed plan revision, roots/branches/bases, live IDs, delivery
commits, reviewer session/passes and resource ownership. Transfer dispatch ownership only
after the prior dispatcher is quiescent and the handoff is reconciled; integration
and canonical state remain owned by the main thread. Apply the persistent blocker gate before further story work or review. Persistent
final review blockers require material-resolution evidence, not a new agent/model.

After the entire goal is delivered and writers are quiescent, perform required
archival under the shared contract and actual authority. Report pending closeout
rather than fabricating success. No implicit push, post, install, deployment,
worktree removal or global configuration change.

Report actual dispatch/integration owners, task/session/model selection evidence,
parallel/serial decisions, worktree/base/path assignments, delivered commits,
checks/review, preserved blockers and archival status. Use
[verification](references/verification.md) for evaluation and activation gates.
