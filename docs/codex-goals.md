# Codex goals and implementation checklists

Use `prepare-implementation` to turn approved requirements into a Markdown story
checklist. The skill defaults to `PLAN.md` when trusted runtime context or the
invoking native entry point identifies Codex, unless you explicitly request another
format. OpenCode defaults to Ralph's `plan.json`; its native `/plan-work` wrapper supplies
the JSON default. If routing is unavailable or ambiguous, the skill asks rather
than inferring the harness from `PATH`, installed tools, folders, environment
variables, or policy headings.
Both formats preserve bounded stories, dependency ordering, and verifiable criteria.
For a clear bounded task, carry the approved request or brief directly into the
plan; a separate PRD and archive manifest are optional. Larger work can use fuller
PRDs, design/phase context and explicit dependency/integration coverage.
`write-requirements` defines outcomes, scope and acceptance; planning owns story
breakdown, worker selection and any optional archive enrollment. Codex Goal and
Ralph/OpenCode are separate worker choices; never launch one inside the other.

## Prepare

Ask Codex to use the installed `prepare-implementation` skill with your requirements.
Use the skill identifier shown by the runtime rather than guessing plugin namespace
syntax. The skill reads only the selected format reference and creates the plan;
it does not implement, run project tests, create branches, start a goal, or create
`progress.md` or `memory.json`.

Each new Markdown story starts unchecked and contains:

- Stable ID, priority, dependencies, user benefit, and owned paths.
- One integration owner, explicit task worktree/branch/base assignments, and
  shared build/output and host resource coordination before worker dispatch.
- Observable acceptance criteria and applicable verification commands.
- The shared implementation/verification/review handoff once, instead of a
  repeated lifecycle checklist per story.
- An instruction to append execution checkpoints to `progress.md`, not the plan.

The plan records a stable approved revision and scope baseline, plus the exact
required working branch. Completion checkboxes change without advancing the
scope revision. Material scope, acceptance or dependency revisions require
reconciliation against user approval and delivery evidence; a new revision label
is not new authority. Missing/self/cyclic dependency references block planning.
Ralph encodes dependencies in existing notes and priority order and executes
serially. Codex admits dependency-ready native workers after Kahn-style graph
validation, including missing-reference and cycle rejection. No independent
scheduler or additional task store is required.
Review the plan before execution. Existing plans, checked statuses, and evidence
must be preserved unless their replacement/reset is explicitly approved. Missing
commands or evidence are recorded as unknown, not invented.

## Execute with native goals

Codex CLI 0.153.4 was inspected with goals enabled. Check `/goal` in your installed
client; feature availability and account permissions remain runtime concerns. No
Ralph profile or additional runner is required.

Goal shares requirements, acceptance, memory, bounded review and per-story commit
gates with Ralph. Its Markdown adapter permits concurrent implementation workers;
Ralph's JSON adapter remains serial. The task adapter uses Markdown checkboxes in
`PLAN.md` instead of JSON `passes` in `plan.json`; native runtime controls remain
distinct. The canonical sources are
[story-execution.md](../ai/plugins/coding/skills/prepare-implementation/references/story-execution.md)
and [story-review.md](../ai/plugins/coding/skills/prepare-implementation/references/story-review.md).
At execution time, load both in full relative to the advertised installed
`prepare-implementation` skill, not through the dotfiles checkout or hardcoded
plugin-cache paths. The executor supplies the full review protocol to the wrapper;
the shared reference, not the native wrapper, owns the exact JSON schema.

Before launching, prepare the lead's integration worktree with an existing commit
on the plan's exact working branch. Each task worktree needs an established clean
committed baseline and an explicit absolute path, exact branch, approved base and
owned paths. Before writes (including logs), staging and committing, verify the
assigned root/branch; reject detached HEAD, `main`, `master` and mismatch.
Before dispatch, verify delivered prerequisite integration commits are ancestors
of the task's assigned base. A clean pre-created worktree with a stale base blocks
that assignment; prepare a suitable base under the lifecycle grant without
silently resetting or rebasing pending work.
An explicit scoped lifecycle grant permits Codex task branch/worktree creation
from approved existing commits. Never switch the user's checkout, repair mismatch,
or copy/commit dirty work to manufacture a baseline. Preserve unrelated work.
Missing preparation, overlapping ownership or unrelated staged content that
cannot be isolated blocks the affected task, not independently eligible work.

Example goal, to enter only when choosing to authorize this scope after reviewing
the plan. Quoting or documenting this template is **not** execution permission:

```text
/goal Execute the approved revision of PLAN.md in standard mode using the installed
prepare-implementation shared execution/review contracts. I authorize in-scope
implementation, required checks, budgeted delegation, scoped task worktree setup
from approved commits and one local commit per
passing story across this eligible sequence. Preserve unrelated work and all
branch, review, permission and sensitive-operation boundaries.
```

This clear plan launch covers the eligible sequence, including continuation,
without another activation prompt per story. The executor verifies the grant and
its limits and asks only for genuinely missing authority or input. Bare Goal or
Ralph labels, plan approval and quoted examples do not grant execution or commits.
Honor any narrower no-commit or delegation limits. No special launch wording is
required when the user's actual request clearly grants the intended scope.

The plan is a completion contract, not permission to bypass sandbox or MCP rules.
Execution and story-commit authorization must be explicit and may cover the bounded
approved sequence, including budgeted delegation when granted. A plan, mode, or shared protocol cannot grant it. Narrower
planning-only, read-only, or no-commit requests remain binding and cannot establish
delivered stories. Dependency approvals still follow project/runtime rules;
Docker lifecycle, migrations including local/test, service operations, global
changes, and other sensitive actions require separate approval.

### Concurrent tasks and shared resources

Read the installed skill's `references/codex-concurrency.md` in full for this
adapter. The lead admits stories by dependency readiness and priority; predecessor
delivery requires integrated checks, review and an authorized commit. A worker
completion claim or isolated commit does not release dependencies.

Assign task worktrees/branches/bases and bounded owned paths explicitly. Native
child spawn does not bind cwd: file operations, Git and check commands must use
the assigned absolute worktree. One lead owns integration branch/index, canonical
markers, progress and memory. Workers return patches and evidence without creating
competing trackers. Required native tools/roles and model selection must be
available in the actual runtime; this source change activates none of them.

Use private build/output roots where possible. Separate worktrees still share
host resources and may reach shared caches/services/output paths. Designate one
owner and use project cross-worktree coordination for conflicting operations;
otherwise serialize them or report the missing mechanism. Optional hooks are
guardrails, not automatic path isolation or a substitute for resource ownership.

Integrate and verify one bounded story candidate at a time in the lead's owned
index. Freeze that candidate and conflicting resources through review and commit;
unrelated implementation workers in separate worktrees may continue. Changed
integration content invalidates old check/review evidence and does not reset
review budgets. Keep required reviewer identity and the existing per-attempt gates.

### Shared review and delivery gate

Use the shared `fast`, `standard` (default), or `deep` mode and implementation-risk
matrix. At most two native implementation advisors may contribute per story;
they are read-only and provide guidance, not edits, checks, posts, or delegation.
Record recommended, used, and skipped advisors with reasons.

The staged-review selection matrix is identical to Ralph's:

| Mode | Trivial | Standard | Test-sensitive | High-risk |
| --- | --- | --- | --- | --- |
| fast | Self | Self | Native | Native |
| standard | Self | Native | Native | Native |
| deep | Native | Native | Native | Native |

Self-review uses the full shared protocol and schema; it is not independent review
or a fallback for missing required native review. Codex native review uses exactly
`story-reviewer`, not `code-reviewer`, a general specialist, or a human substitute.
OpenCode Ralph uses its native `ralph-reviewer`; the generic generated OpenCode
`story-reviewer` has no shell access and is not a substitute.

Run configured formatters and required typecheck/lint/tests before staged review;
UI work also requires executor-owned `verify-interface` browser evidence. Reviewers
only inspect project-local files and permitted staged Git evidence, never run
checks, edit, browse, use MCP, or post externally. One initial holistic pass and
at most one targeted remediation pass are allowed. Resume the same actual native
agent ID for targeted review; no fresh audit, replacement session, or third pass.
The executor selects `expanded-initial` from the CodexGoalMarkdown adapter and
sends explicit packet lines:

```text
Review profile: expanded-initial
Pass type: initial
```

For same-session remediation, retain the profile and send `Pass type: targeted`.
Self-review explicitly selects the same profile and pass type in review context.
The native wrapper requires this profile; missing, unknown, or conflicting
selection blocks before evidence gathering, with the exact problem in
`residual_risks`. Never infer the harness from tools, binaries, paths, or role
names. The profile is input-only and grants no tools or runtime overrides.

RalphJSON explicitly selects `three-step`; OpenCode enforces `steps: 3` and an
exact Git allowlist. An `expanded-initial` initial review permits up to 40 small
read-only evidence calls, counting calls in batches individually.
Start with staged filenames, status, and statistics; read manageable patch groups
without requiring an aggregate patch. Recover only missing sections after
truncation using permitted staged Git reads; never repeat oversized requests.
Track relevant changed files and directly affected contracts and assess the
evidence holistically. Stop when coverage is sufficient: 40 calls is a ceiling,
not a target. Return `blocked` with exact missing sections in `residual_risks` if
required evidence remains unavailable at the ceiling or through permitted tools.
Targeted review under either profile retains at most two evidence-gathering turns
and only prior findings and remediation regressions. The configurable reading
budget is behavioral guidance, not an equivalent hard step cap or immutable sandbox/MCP
restriction; parent runtime controls apply. See the
[activation steps](ai-configuration.md#installation-and-replacement-behavior) and the
reviewer refresh guidance in that guide before starting a new review cycle.

Validate the exact JSON response. Missing required protocol, reviewer, invocation
or resumption capability/session, malformed or blocked review, and failed required
checks stop delivery with the story pending. In-scope critical/high/medium findings
block; low findings block when they violate requirements. Record each disposition
as `accepted_fixed`, `rejected_false_positive`, `deferred_out_of_scope`, or
`unresolved_blocker`, with evidence. Do not defer an unmet criterion to pass review.

After passing checks/review, update validated memory, append final evidence, and
provisionally check only the selected story for its authorized commit. Inspect the
complete intended staged candidate and branch again. Delivery requires a successful
story commit, using `feat(<story-id>): <story-title>` with actual values. Failed
finalization or commit restores only that provisional checkbox in worktree/index
where authorized, preserves other work, appends the blocker, and stops without
retrying, amending, or bypassing hooks. Report unsafe restoration or logging
explicitly. Reconcile stale markers against Git delivery evidence on resumption.
Report the actual commit hash in the final response; the committed log retains
pre-commit pending status, without a second bookkeeping commit.

### Blocked stories and evidence-gated resumption

A final native review `blocked` verdict stops delivery and further review attempts
for that story immediately. Preserve its candidate, unchecked status, findings,
dispositions, checks, reviewer ID, and historical evidence. Append a safe checkpoint
to `progress.md` naming the exact blocker, what must materially change, the
evidence required before resumption, consumed review passes, and existing authority.
If write guards prohibit the checkpoint, report it in the response instead.

Truncation before the verdict remains recoverable within the current review's
permitted evidence budget. A final blocked verdict ends that recovery; it cannot
be repackaged as a targeted pass. Automatic continuation, elapsed time, another
turn, compaction, or a new reviewer session neither resolves the blocker nor resets
the review budget. Rewording a request, raising output limits after repeated
truncation, or replacing the reviewer alone is not resolution evidence.

Before resuming, verify current-state evidence against the recorded resolution
requirements and append the actual material change and remaining constraints.
For example, confirm that the exact previously unavailable staged sections are
now accessible through permitted tools, rather than merely proposing higher limits.
Only verified resolution can permit a new bounded initial attempt under existing
scope, preserving the failed attempt's history. Valid initial reviews with
actionable findings still use verified remediation and at most one targeted pass
in the same session; do not use this gate to evade exhausted remediation budgets.
Carry forward existing user authorization. Ask only for genuinely new authority
or missing input, naming the exact constraint rather than repeating approval requests.

Another story may proceed only if independently eligible under dependencies and
priority ordering and safely isolated from the preserved blocked candidate through
implementation, staging, checks, and commit. Otherwise report the blocker and stop
work; do not manufacture experiments or bookkeeping to sustain activity.
The canonical [persistent blocker gate](../ai/plugins/coding/skills/prepare-implementation/references/story-execution.md#persistent-blockers-and-goal-resumption)
is separate from evidence-reading budgets and leaves Ralph's explicit recovery
handoffs and persisted counters unchanged.

### Native controls

| Command | Action |
| --- | --- |
| `/goal` | View the current goal |
| `/goal pause` | Pause it |
| `/goal resume` | Resume it |
| `/goal clear` | Clear it |

Codex maintains the objective in the thread and can continue at idle turn
boundaries. It is not a background daemon that keeps executing after the process
exits. Completion, interruption, blockers, and budget limits can stop progress.
Do not assume a Markdown checkbox or a model's completion claim proves the
acceptance criteria; retain the supporting verification and review evidence.

The story-review stop and the overall native Goal status are distinct. The
[upstream Goal continuation prompt](https://github.com/openai/codex/blob/main/codex-rs/ext/goal/templates/goals/continuation.md)
inspected for this contract requires the same impasse for at least three consecutive
Goal turns, including the original turn, before `update_goal` with status `blocked`.
User resumption starts a fresh native blocked audit. Follow the actual runtime's
lifecycle instructions and exposed capabilities if they differ; these dotfiles do
not implement or override that audit. While it is pending, report the unchanged
impasse without repeating reviews or inventing activity. Once its conditions are
met, use the supported native blocked-status transition. A fresh native audit does
not reset the story blocker or review budget. Do not invent a restart loop,
continuation controller, unsupported Goal setting, or false completion claim.

## Context and checkpoints

Keep `PLAN.md` as the stable plan and completion checklist. Append current results,
status, implementation notes, review dispositions, and the next action to
`progress.md` after each reviewed story and before pausing or handing off blocked
or incomplete work. Identify entries by plan/feature and story ID. Record evidence
before provisionally checking completion boxes; missing checks, review, or a
successful authorized commit keep a story undelivered.
Read the plan, relevant log entries, and bounded memory when resuming or after
compaction.
Preserve existing history, and link to artifacts instead of copying every tool log.
Record actual runtime, model and source, mode, supplied limits, check commands and
outcomes, findings/dispositions, intended commit, and next checkpoint. Record the
actual native reviewer agent ID (Ralph uses `task_id`), or self-review with its
budget reason; mark unavailable metadata unknown. Do not invent iteration limits
or claim Codex has Ralph's external hard iteration controller, fresh-session loop,
or completion sentinel.

Planning creates neither log nor memory. Resolve `progress.md` and `memory.json`
from the worktree root, even with a custom plan path. After branch and worktree
guards pass, execution creates the journal only when a permitted checkpoint is
required and otherwise appends without resetting it. Never rewrite earlier entries
or headers, or read/migrate legacy execution logs. Existing plan notes are preserved;
explicitly approved cleanup during execution must preserve them in `progress.md`
before trimming the plan. Keep future execution narratives out of the plan and PRD.

Look up project-local `memory.json` before reading it. Absence is normal: use
`{"version":1,"patterns":[],"suppressions":[]}` in process without creating a file
at startup. Present memory must validate as version 1 with valid entries and at
most 20 patterns and 20 suppressions. Invalid/unreadable memory blocks without
overwrite. Create/update memory only after passing review. Promote reusable
learning only from `accepted_fixed` findings with passing verification; suppress
only evidenced `rejected_false_positive` findings, never newly demonstrated
failures. Deduplicate and enforce bounds before staging. Keep operational knowledge
in memory, append-only audit history in progress, and only mature durable repository
guidance in the nearest `AGENTS.md`; substantive guidance changes precede review.

Rely on native automatic compaction, or use `/compact` manually when appropriate.
Automatic story-boundary compaction is [deferred](backlog.md#codex-checkpoint-compaction).
No global or plugin lifecycle hook is installed for it.

## Completed-run archival

Archival is optional: an unenrolled bounded task finishes after verified story
delivery and reports its evidence without another PRD or cleanup workflow.
When deterministic archival is requested, planning owns the saved PRD inventory
and work-run binding; requirements drafting adds no runner/archive metadata.

For an enrolled run, with one active plan per worktree, archive only after all
tasks are verified and required story commits succeed. Follow the [shared archival procedure](../ai/plugins/coding/skills/prepare-implementation/references/completed-run-archive.md):
invoke the installed archive_run.py automatically under the existing scoped
archival/removal grant, passing the exact primary PRD and absolute worktree root.
The optional PRD work-run manifest declares the task source and associated PRDs; committed
story-result records bind observed check/review results to completed story markers.
The script verifies and archives PRDs, plan, root progress.md and existing
memory.json together as peers in a unique timestamped directory, preserving
bytes and recording a receipt. It never resets history or creates new state.
A closeout commit needs its own scope, which may be authorized upfront. Ralph's
invoking assistant uses the same helper after supervisor validation and successful
exit; CLI-only Ralph has no post-run hook. Neither workflow archives during
requirements drafting. Legacy runs lacking metadata/records need scoped
enrollment when archival is requested; never fabricate evidence or automatically
relocate old journals.

Archival is allowed on any branch, including `main`/`master`, even if the original
branch was merged and deleted. Verify run ownership and delivery using retained
commits or merged PR/squash-commit evidence together with the journal. Record the
original branch and current archival branch/HEAD; do not switch branches or rewrite
historical plan metadata. Missing completion evidence still blocks archival.
Implementation and resumption retain their exact prepared-branch requirements.

## Verification status

Routing scenarios are recorded in `tests/fixtures/implementation_planning_evals.json`
for manual evaluation. Static source checks do not establish model behavior. Before
relying on unattended execution, evaluate a bounded goal in an authorized disposable
project, including exact-branch rejection, native reviewer invocation and same-session
targeted review, memory validation, interruption/resumption, and failed delivery.
Static checks do not prove live Goal continuation, reviewer permissions, or commits.

Sources: [Follow a goal](https://developers.openai.com/codex/use-cases/follow-goals),
[Using Goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex),
[CLI slash commands](https://developers.openai.com/codex/cli/slash-commands).
