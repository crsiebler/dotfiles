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

## Shared-resource consumers

RalphJSON and recovery discover this bundle only to read story-execution.md,
story-review.md and ralph-control.md. That resource-loading path does not enter
the Codex team preflight, require Sol/Luna/coordinator APIs or change Ralph's
serial runner. Native wrappers select their explicit adapter/profile.

## Entry and ownership

Invoke this workflow explicitly or from an assigned multi-agent-coordinator.
Do not make requirements, planning or ordinary coding methods call it implicitly.
An adequate approved story plan is required input. If missing, report the exact
input gap; do not invoke a planner or regenerate the plan. Normal coding skill
discovery applies when coding begins; no particular development skill is an
orchestration prerequisite.

The main thread is the sole dispatch and integration owner. It owns version
control, merging, conflicts, canonical task markers, append-only progress and
bounded memory. Workers return bounded changes and evidence. A coordinating
subagent may provide analysis, but cannot take over Git, trackers or dispatch.
Do not proxy-spawn for a child or create recursive managers. A native role file
cannot promote a child to primary or change the main thread's selected model.

## Preflight and dispatch

Use one compact capability/ownership preflight. Verify the main thread's selected
`gpt-6.1-sol` setting, callable worker model controls, capacity accounting and exact
native story-reviewer selection/same-session continuation when the budget requires
it. Record selection evidence and unknown effective settings honestly. A conflicting
installed pin blocks that model path; never alter runtime settings to pass.
Missing required reviewer capability blocks execution, not permission to substitute
a generic reviewer. Inspect actual tool schemas; names and files prove no capability.

Select `gpt-6-luna` explicitly for implementation workers. Use `gpt-6-astra` for reviews, conflict analysis, architecture and cross-domain
analysis under [runtime selection](references/runtime-selection.md), within existing
advisor/review/remediation allowances and actual model-use scope. Keep the main thread
on Sol. A model change does not reset review attempts, add a second gate or grant
an autonomous retry. Role definitions remain reusable without model pins.

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

Read this skill's [story execution](references/story-execution.md),
[review protocol](references/story-review.md),
[concurrency](references/codex-concurrency.md) and
[archival](references/completed-run-archive.md) contracts in full, relative to
this advertised installed bundle. They own execution, runtime selection, review,
state and delivery. No planning skill is a runtime dependency. For enrolled runs,
verify/bind run metadata before the first checkpoint under actual scoped authority;
preserve existing manifests. Ralph still requires its clean committed plan before
launch; invoking Ralph does not authorize setup commits.

Read the exact existing Codex plan and revision. Preserve story IDs, dependency
edges, acceptance criteria and completed evidence. Validate all references,
self-dependencies and cycles; use Kahn-style readiness ordered by priority then
document order. Release a predecessor only after verified integration checks,
bounded review and its authorized integration commit. A worker result or isolated
branch commit never satisfies that dependency.

Require clean committed task worktrees with explicit absolute paths, exact
non-main branches, approved full bases containing delivered prerequisites and
nonoverlapping owned paths. Verify actual containment, including symlinks, before
writes. Native spawn neither allocates a worktree nor binds cwd. Use assigned
paths/workdir for files, Git and checks. Never copy dirty work to make a baseline.
Use private outputs and existing project controls for shared builds/caches/host
resources; serialize conflicts if exclusion cannot be established.

Integrate one bounded candidate at a time through the shared checks and risk-based
review. Use permitted self-review only where that budget allows; otherwise invoke
exact native `story-reviewer` with full protocol/profile and preserve its session.
Allow one initial and at most one targeted pass per attempt. Do not add a worker
staged review, extra coordinator approval or reviewer-of-reviewer cycle. Follow shared
pre-commit evidence and provisional marker finalization; report delivered completion
only after successful authorized integration commit. Keep evidence in progress,
not plan narratives or a new registry.

On failure, preserve candidate/history and block its dependent subgraph; continue
only safely isolated eligible work. Reconcile uncertain spawn/results through
native session state before any retry. Never duplicate a possibly-live owner.
Resume from observed plan revision, roots/branches/bases, live IDs, delivery
commits, reviewer session/passes and resource ownership. Transfer ownership only
after the prior lead is quiescent and the handoff is reconciled. Apply the persistent blocker gate before further story work or review. Persistent
final review blockers require material-resolution evidence, not a new agent/model.

After the entire goal is delivered and writers are quiescent, perform required
archival under the shared contract and actual authority. Report pending closeout
rather than fabricating success. No implicit push, post, install, deployment,
worktree removal or global configuration change.

Report actual dispatch/integration owners, task/session/model selection evidence,
parallel/serial decisions, worktree/base/path assignments, delivered commits,
checks/review, preserved blockers and archival status. Use
[verification](references/verification.md) for evaluation and activation gates.
