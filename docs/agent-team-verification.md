# Agent-team verification and activation limits

Historical record: the runner and dedicated story role described below were
retired on 2026-10-24. Their previous measurements are retained as recorded, not
claims about the replacement. Current behavior and validation are in
[story review verification](story-review-verification.md).


The run-agent-team coding skill defines a harness-agnostic native team procedure.
The normal main AI session owns dispatch, Git, integration and canonical task
state. The optional multi-agent-coordinator supplies advice, not essential policy,
a primary entry point or runtime APIs. No nested manager or role loading is needed.
Ralph remains serial under its own native lifecycle/review instructions. Team
delivery/review references belong to run-agent-team. Only archive-run shares
executable archival functionality.

## Entry and host capabilities

Use the active harness's actual skill-selection and native delegation mechanisms.
The core team-execution.md, task-concurrency.md, delivery and review contracts do
not require Codex, a custom primary or a child coordinator. A different harness
may execute them only if the required native worker/capacity/reviewer and
session-continuation controls are actually available and authorized. Missing
controls block the affected path; switching a label does not supply them.
Preferred model controls are optional; explicit user model constraints still apply.

### Conditional Codex CLI entry

For Codex CLI only, select run-agent-team with `/skills`, or explicitly use its
discovered `$run-agent-team` name in a normal request. Use the picker when qualification or
names are ambiguous. Then set `/goal <objective>` naming the approved plan and
existing execution scope. The command alone does not select the skill or supply
grants; a user objective to implement the approved plan includes its initial
and subsequent scoped local commits.
Do not rely on undocumented combined slash-command/skill parsing. For example,
after selecting the skill in the current main session:

```text
/goal Execute the approved PLAN.md using run-agent-team. This main session owns orchestration. Target up to four concurrent implementation workers within actual runtime/resource capacity, reserving capacity for an independent reviewer with the complete reviewer and review-story contracts within the skill's budgets. Apply the skill's model preferences and supported fallbacks. Preserve pending work and report missing worktree authority or native capability.
```

The example grants no authority by itself. Confirm the existing actual integration
root/branch and task-worktree lifecycle. When actually requested by the user,
this plan implementation authorizes its scoped initial, story and closeout local
commits without a second approval; it does not authorize archival/removal.
Official [command syntax](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
and [skill invocation](https://learn.chatgpt.com/docs/build-skills) support these
separate entry steps; neither a skill nor goal creates missing host tools.

## Verification scope

Repository contract tests validate bundle resource closure, evaluation-fixture
structure, dependency/ownership examples, and disposable two-worktree Git
isolation/base ancestry. They do not spawn models, enforce an agent's cwd, or
establish native role selection, model routing or observed overlap. Fixtures
contain expected behavior, not passed model runs. No live team smoke is claimed.

For the model-preference revision, local validation passed: create-skill bundle
validation, `make validate-ai`, and 40 tests across agent-team, runtime-selection,
coding-workflow and agent-contract suites. The evaluation fixture adds cases for
unknown coordinator telemetry, a Luna-pinned reviewer, inheritance-only workers,
an explicit Astra requirement, pending-commit recovery and a held-out alternate
model combination. These cases were inspected against the revised instructions;
they have not been executed as live model evaluations. No installed skill was
updated and no stopped run was resumed by these checks.

### Sustained coordination source revision

The source contract now keeps capacity, work phases, queue pressure and event
checkpoints in task-concurrency.md, with worker readiness and exclusive repair
ownership in team-execution.md. The waiting-candidate limit defaults to one with
one feasible worker, otherwise two, reduced when project resources require it.
Handed-off source-only and worker-remediation candidates count toward pressure;
already active workers may finish even when their results exceed the limit.
Review/session budgets and verified integration delivery remain unchanged.

Static walkthrough of evaluation cases 25–31 and 33 against the revised source:

| Cases | Source assessment |
| --- | --- |
| 25: slow SDK check | Event checkpoints now require reassessment at a yield and eligible dispatch before waiting again, using the existing check handle. Previously dispatch/refill was not tied to check yields. |
| 26, 33: substantial repair versus tiny fix | Handoff rules now specify original-worker remediation, exclusive transfer in both directions and focused rechecks; small integration fixes remain with the main thread. Previously remediation ownership was left to the main thread without this distinction. |
| 27: missing shared hooks | Worker packets and handoffs now require feasible checks and early hook constraints, with an explicitly unqualified source-only result and minimal integration compile checkpoint. |
| 28: saturated queue | The explicit limit stops new-story admission; incoming results are preserved and qualification/delivery drains pressure before refill. Previously no waiting-candidate bound was defined. |
| 29: uncertain capacity | Documented semantics and supported inspection now distinguish observed occupancy from unknown labels and identify the affected admission without stopping safely eligible work. |
| 30: retained review session | The existing same-session safeguard is retained and explicitly applied to review-finished checkpoints; an idle label does not permit release. |
| 31: justified serialization | Existing resource/dependency guards still prevent conflicting SDK use and premature dependent dispatch; event checkpoints do not override them. |

Case 32 combines these events across delivery cycles and remains held out for a
later authorized runtime evaluation. Existing planning/non-trigger and model
fallback cases are retained. These assessments compare instruction coverage, not
executed model behavior or measured performance.

Local validation for this revision passed with the existing Conda `dotfiles`
Python 3.11.16/PyYAML 6.0.3: create-skill `check` and bundle `validate`,
`make validate-ai`, `git diff --check`, and 63 tests across agent-team,
runtime-selection, story-execution, story-blocker, coding-workflow and agent-contract
suites. Tests inspect all 33 evaluation records for structure/resource closure;
they do not execute those prompts. The system command wrappers emitted temporary
cache warnings during `make`, but validation completed with exit zero and reported
valid AI sources. No standalone repository typecheck target exists.
No live team, application plan, installed copy, publication or repository commit
was part of this source validation. Runtime occupancy, check yielding and sustained
delivery performance remain unmeasured; use the expanded verification reference
under separate live-execution scope to establish them.

Codex CLI 0.162.0 was inspected locally in October 2026. In the exposed task
runtime, native custom-role selection for story-reviewer could not be established.
Removing the coordinator dependency does not repair that separate review-tool gap.
Installed role pins and global defaults can differ from preferred model selection.
The revised policy accepts supported fallback models and unknown coordinator
telemetry unless explicit user constraints prohibit them. Source omission does
not establish installed inheritance. Required native review
and same-session continuation still block affected execution if unavailable.

## Activation and recovery

Source delivery does not refresh installed skills, roles or runtime settings.
Before live validation, separately authorize any necessary coding-plugin/role/
configuration refresh, preserve customizations, restart and verify unique discovery
in a fresh task. Then use the loaded skill's disposable two-worker smoke in the
selected harness under actual native-model/worktree/check/fixture-commit/archive scope. The main session
must dispatch directly without reading or invoking the coordinator. Verify worker
model evidence/fallbacks, capacity, supported reviewer binding and same-session continuation first.
No global installation, cache cleanup or live model experiment is part of source
checks. Missing required gates block the smoke. Contract-supplied binding is
supported when the selector alone is absent and those gates are satisfied.

For a run stopped only by the earlier mandatory Sol/Astra policy, activate the
revised skill through separately authorized installation, or obtain an explicit
user override of those installed model requirements for that run. In the resumed
run, reconcile the existing candidate, passing review, reviewer session and
consumed passes. Preserve valid delivery evidence and complete a pending commit
only after checking the candidate and existing commit grant. This policy change
does not resume a stopped goal, resolve unrelated blockers or grant another review.

For older delegated runs, first quiesce the prior dispatcher and reconcile every
live worker/reviewer, worktree/base assignment, candidate and consumed pass before
the main session takes ownership. Never duplicate a possibly-live owner or reset
review budgets. Planning and ordinary coding remain independent; Ralph never
loads team contracts. The earlier removed launcher remains recoverable in Git
commit 4864f67; no launcher or OpenCode migration is introduced here.

## Reviewer binding correction (2026-10-24)

A reported runtime prompt asked for an exception because spawn had no native
role-selection parameter. Source inspection found that both the entry skill and
story execution required exact native selection, and evaluation case 3 expected
a blocker. This was an instruction mismatch, not evidence that independent
delegation itself was unavailable.

The workflow now supports native-role selection or full contract delivery to a
fresh independent generic agent. Both preserve candidate restrictions, pins,
complete review-story packets and same-session budgets. Explicit native-role
requirements, missing contracts, unsupported enforcement, unavailable independent
delegation or missing continuation still block. The review record names reviewer
as the responsibility and records the actual binding/type in evidence.

Case 3 now covers the reported missing-selector path. Cases 34–39 cover pins,
explicit native-role requirements, missing instructions, implementer independence,
targeted continuation and unavailable continuation. These are authored evaluation
cases, not executed model results. Static resource/contract tests cannot prove
that a future agent will avoid the prompt. Historical runtime results above are
unchanged. Installed activation remains separate.

## Plan-launch commit authority (2026-10-24)

The execution contract previously said a launch "may cover" local commits and
separately required explicit story-commit authorization. The reported initial
commit prompt exposed that ambiguity. An explicit request to implement an
approved plan now covers the initial and subsequent scoped local commits,
including continuation and closeout of authorized artifacts. No extra commit
wording or repeated approval is required.

The initial checkpoint is limited to the approved plan and required task-owned
metadata. Implementation still needs checks/review; unrelated work, narrower
no-commit instructions, runtime denials and external/destructive-action boundaries
remain protected. Archival/removal authority is distinct from committing its
authorized result.

The new instruction-contract regression failed against the previous wording,
then passed after the update. The full suite ran 279 tests: 278 passed and one
existing Codex strict-mode check was skipped. Evaluation cases 40–47 cover
initial/continuing authority, planning-only and no-commit requests, dirty state,
failed gates, closeout and external actions. They are authored cases, not live
agent results. Installed configuration was not changed.
