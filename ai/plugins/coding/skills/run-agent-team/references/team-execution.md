# Main-session team execution

This is an invocation procedure, not a runtime adapter implementation. Resolve
trusted active-harness identity and inspect the tools actually exposed. Stop an
unsupported execution path rather than guessing argument names or role support.
The normal main AI session directly owns dispatch, Git, integration and
canonical task state. No custom coordinator selection or nested manager is needed.

## Explicit entry

Select run-agent-team explicitly through the active harness's supported skill
mechanism, naming the approved plan and existing execution scope. Inspect actual
entry/tool schemas rather than inventing slash commands or inferring capabilities
from a harness name. An explicit user request to implement the approved plan
includes initial and subsequent scoped local commits; record and carry that grant
without repeated prompts. A bare goal label or selected skill alone grants no
execution, worktree, commit, installation or publication authority. Use
[commit authority](story-execution.md#authorization-and-prepared-branch) for the
initial checkpoint and exclusions. A custom primary is not required. The main AI
session coordinates directly.

## One preflight record

Apply [autonomous execution scope](story-execution.md#autonomous-execution-scope)
before dispatch. Required verification and closeout must have an authorized
noninteractive path; do not introduce manual test or deployment gates. Confirm
the readiness record, including missing authority for required closeout, before
starting implementation. This is not permission to weaken required acceptance.

The main thread records in the existing execution checkpoint:
- Exact plan path/revision, approved outcome and integration root/branch/base.
- Main session as the only dispatcher and integration/Git/canonical state owner,
  with actual session identity and model evidence when available (otherwise
  unknown).
- Worker/model/delegation limits, observed occupied capacity versus uncertainty,
  documented session semantics, required reviewer capacity and supported
  inspection/continuation/release controls; queue limit and its rationale under
  [capacity and queue control](task-concurrency.md#capacity-and-queue-control).
- Actual native worker/model controls and installed pins; reviewer binding and same-session continuation where required by the risk budget.
- Existing execution, worktree, commit and closeout grants; missing scope/tools.
- Approved endpoint and readiness evidence, agent-executable verification paths,
  planned automation dependencies, and any newly discovered mandatory blocker.

No coordinator role, primary-agent switch, nesting or role-guidance adoption is
required. The main session follows this workflow directly. Bounded planning or
research advice does not transfer dispatch, Git or tracker ownership.
Missing required reviewer controls blocks affected
execution; self-review follows only the existing risk budget. No automatic model
switch, installation, capability-probe agents or proxy-spawning. Apply
[runtime selection](runtime-selection.md): model preferences and unknown telemetry
alone do not block; explicit user constraints and required review capabilities
still apply. Use [reviewer binding](story-execution.md#reviewer-binding) when
the runtime lacks a role selector.

## Direct packets and delivery

Implementation uses available native execution agents without requiring a custom
implementation role. Confirm the actual runtime interface in preflight;
ordinary work may remain in the main session.
No built-in override, role installation or primary-agent switch is required.

Every worker packet includes story ID/criteria, source requirements, delivered
prerequisite commits, absolute task worktree, exact branch/full base, bounded owned
paths/interfaces, private output locations, resource constraints, model selection
or inheritance/pin evidence and required role identity and relevant loaded skills. Identify feasible
compilation and focused verification commands with working directories, required
build hooks/generated inputs, and any known unavailable checks or shared resources.
Include test inputs/fixtures, expected results, check ownership and budgets; name
any prerequisite test/automation authoring. Preserve the approved autonomous
endpoint in each packet: no manual QA, human result-confirmation or added release
gate. Deployment verification requires explicit scope and an automated path.
An optional human follow-up is not a worker handoff or delivery condition.
Workers do not orchestrate, subdelegate, stage, commit, merge or modify canonical
task state. Normal coding skill discovery applies.

The main thread validates the DAG, prepares worktrees and verifies base ancestry
before admission. Fill Kahn-ready capacity in priority then document order;
fill the worker target with independent eligible stories before waiting when
limits permit, dispatching at least two when available. Apply the concurrency
contract's capacity, queue and event rules before each wait; the worker target
does not override qualification or delivery pressure.

## Handoff and remediation

Workers execute available relevant compilation and focused checks before handoff.
Return actual session/story IDs, base/candidate, changed paths, commands/results,
private output locations, failures, unrun checks and blockers. Distinguish checks
passed on the worker candidate from qualification of the integrated candidate.
Report missing shared build hooks early, before accumulating uncompiled work.
The main thread arranges the smallest integration compile checkpoint using the
existing hooks and resource controls; do not duplicate a broad build system or
install dependencies automatically. A necessary source-only handoff is explicitly
unqualified, includes the missing checks/reason and compile checkpoint, and cannot
satisfy delivery until required checks pass. Run other feasible checks meanwhile.

Return substantial bounded source remediation to the original worker when feasible
within the existing authorization and delegation/remediation budgets. First verify
that the prior writer is quiescent and explicitly transfer exclusive ownership of
the exact candidate revision, worktree and bounded paths; record the transfer in
the existing checkpoint and confirm it with the recipient before writes. Supply
failure evidence, required changes and focused rechecks. The worker edits only
its assigned source; the main thread retains shared integration files, Git/index,
canonical state, review coordination and commits. Never allow simultaneous writers
to a candidate or edit a candidate under active review. If repair needs shared
integration changes, the main thread applies those in sequence. Reconcile returned
changes and quiescence, transfer ownership back, then integrate and recheck.
Keep small integration fixes with the main thread when delegation adds unnecessary
overhead. If worker remediation is infeasible, record why and retain bounded local
repair or block the affected story; no replacement worker or retry expands budgets.

Integrate one candidate, run required checks, freeze that candidate/conflicting
resources, then directly invoke the required reviewer. Supply the complete
unchanged protocol/profile/schema in each packet, not an inherited reference;
retain its actual native session for the permitted targeted pass. Other isolated
workers may continue. The main thread owns remediation coordination and final
markers, progress/memory/authorized commit operations. Remediation changes
invalidate affected check/review evidence; preserve the existing permitted passes
and persistent blocker gate. No extra approval or review gate.

Worker results do not release dependencies. Require successful integration
checks/review, actual authorized commit and current plan revision, then verify
those prerequisite commits are ancestors of each dependent's assigned clean base.
Record evidence in the existing checkpoint, not another queue or task registry.
Use the current main session and supported model preferences or recorded fallbacks
under runtime-selection.md. Keep reusable role files unpinned; respect any installed
pins. Source text activates no installed settings.

## Failure and restart

Append actual settings/IDs, assignments/bases, checks/reviews, delivered commits
and consumed passes to progress.md. Inspect native state and owned files after
interruption; an uncertain worker may remain live. Do not duplicate its work.
For an older delegated run, first quiesce its prior dispatcher and reconcile all
live workers/reviewers, assignments, candidates and consumed budgets before taking
main-session ownership. Missing identity or unresolved ownership blocks takeover.
Final blocked review preserves candidate/history and consumed budget; new agents
or models do not resolve it. Continue only independently eligible isolated work.
Global stops stop the batch. After verified delivery, quiesce writers and apply
required archival under actual authority. Preserve old plans if closeout fails.
