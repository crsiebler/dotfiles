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

Honor the supplied assignment before selecting a mode:
- A worker follows its bounded story packet and the advertised `develop-code`
  method only. It must not route back here, spawn a coordinator, or subdelegate.
- An already designated batch lead adopts the supplied contract directly; it
  must not create another coordinator.
- An initial caller establishes one batch lead through the preflight below.

For an explicit swarm/team request without an adequate plan, discover
`prepare-implementation` and prepare the missing bounded plan/handoff first.
Preserve approved requirements, scope, acceptance and state. Reuse existing
execution, delegation, worktree and commit grants; request only genuinely missing
scope. Planning-only work creates neither agents nor execution state. Do not
silently treat an explicit team request as serial execution.

Prefer native `multi-agent-coordinator` on explicitly selected `gpt-6.1-sol` as
both sole dispatch owner and sole integration owner for the batch. The parent
supervises scope after handoff; it does not also dispatch, stage, commit, or edit
canonical trackers. Workers return changes and evidence. The coordinator owns
integration checks, existing review gates, authorized story commits, completion
markers, append-only progress and bounded memory. Give the owner explicit
integration root/branch, plan path/revision, grant, limits and role.

When nesting or manager capacity is unavailable, an already selected Sol parent
may load the discovered coordinator's instructions and be the sole lead with
direct workers. Disclose guidance adoption, not native custom-role invocation.
Do not use parent proxy-spawning for a coordinating child. This fallback still
requires all worker, model and dedicated-reviewer capabilities. Missing required
native review is a blocker, never grounds to substitute a generic reviewer.

## Preflight and dispatch

Use one compact capability/ownership preflight. Inspect actual native tool
schemas, available role registrations and installed model pins. Every mode needs
supported worker model selection, known capacity accounting, and required native
`story-reviewer` selection plus same-session continuation before worker calls.
Delegated mode additionally needs exact coordinator invocation/model selection and
permitted nesting. Parent-direct mode instead needs a selected Sol parent and
readable discovered coordinator guidance; it does not require a coordinator child
or nesting. Never let that fallback weaken the worker or reviewer gates.
A file, label, source change or generic child is not proof of these capabilities.
Record requested settings, selection evidence and unobserved effective settings
honestly. A conflicting role pin blocks that model path; never install or alter
settings automatically to make the preflight pass.

Select `gpt-6-luna` explicitly for implementation workers. For justified ambiguity,
security or difficult failure, use `gpt-6-astra` only within the existing advisor,
review or remediation allowance and actual model-use scope. Keep the coordinator
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

Discover `prepare-implementation`; load its `references/story-execution.md`,
`references/story-review.md`, `references/codex-concurrency.md` and
`references/completed-run-archive.md` relative to its advertised installed base.
They remain canonical for graph/ownership, review schemas/budgets, commits,
persistent blockers and archival. Do not use hardcoded checkout/cache/sibling
paths or duplicate those contracts here.

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
staged review, coordinator approval or reviewer-of-reviewer cycle. Follow shared
pre-commit evidence and provisional marker finalization; report delivered completion
only after successful authorized integration commit. Keep evidence in progress,
not plan narratives or a new registry.

On failure, preserve candidate/history and block its dependent subgraph; continue
only safely isolated eligible work. Reconcile uncertain spawn/results through
native session state before any retry. Never duplicate a possibly-live owner.
Resume from observed plan revision, roots/branches/bases, live IDs, delivery
commits, reviewer session/passes and resource ownership. Transfer ownership only
after the prior lead is quiescent and the handoff is reconciled. Persistent final
review blockers require material-resolution evidence, not a new agent/model.

After the entire goal is delivered and writers are quiescent, perform required
archival under the shared contract and actual authority. Report pending closeout
rather than fabricating success. No implicit push, post, install, deployment,
worktree removal or global configuration change.

Report actual dispatch/integration owners, task/session/model selection evidence,
parallel/serial decisions, worktree/base/path assignments, delivered commits,
checks/review, preserved blockers and archival status. Use
[verification](references/verification.md) for evaluation and activation gates.
