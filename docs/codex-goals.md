# Codex goals and implementation checklists

Use `prepare-implementation` to turn approved requirements into a Markdown story
checklist. The skill defaults to `PLAN.md` when trusted runtime context or the
invoking native entry point identifies Codex, unless you explicitly request another
format. OpenCode defaults to Ralph's `plan.json`; its native `/plan-work` wrapper supplies
the JSON default. If routing is unavailable or ambiguous, the skill asks rather
than inferring the harness from `PATH`, installed tools, folders, environment
variables, or policy headings.
Both formats preserve bounded stories, dependency ordering, and verifiable criteria.

## Prepare

Ask Codex to use the installed `prepare-implementation` skill with your requirements.
Use the skill identifier shown by the runtime rather than guessing plugin namespace
syntax. The skill reads only the selected format reference and creates the plan;
it does not implement, run project tests, create branches, start a goal, or create
`docs/progress.md` or `memory.json`.

Each new Markdown story starts unchecked and contains:

- Stable ID, priority, dependencies, user benefit, and relevant paths.
- Observable acceptance criteria and applicable verification commands.
- Research, implementation, verification, bounded staged review, and remediation steps.
- An instruction to append execution checkpoints to `docs/progress.md`, not the plan.

The plan records the exact required working branch, not a branch suggestion.
Review the plan before execution. Existing plans, checked statuses, and evidence
must be preserved unless their replacement/reset is explicitly approved. Missing
commands or evidence are recorded as unknown, not invented.

## Execute with native goals

Codex CLI 0.153.4 was inspected with goals enabled. Check `/goal` in your installed
client; feature availability and account permissions remain runtime concerns. No
Ralph profile or additional runner is required.

Goal inherits Ralph's full shared execution, memory, review, prepared-branch, and
per-story commit contract. The task adapter uses Markdown story checkboxes in
`PLAN.md` instead of JSON `passes` in `plan.json`; native runtime controls remain
distinct. The canonical sources are
[story-execution.md](../ai/plugins/coding/skills/prepare-implementation/references/story-execution.md)
and [story-review.md](../ai/plugins/coding/skills/prepare-implementation/references/story-review.md).
At execution time, load both in full relative to the advertised installed
`prepare-implementation` skill, not through the dotfiles checkout or hardcoded
plugin-cache paths. The executor supplies the full review protocol to the wrapper;
the shared reference, not the native wrapper, owns the exact JSON schema.

Before launching, prepare a Git worktree with an existing commit on the plan's
exact working branch. Before any writes (including logs), and again before staging
and committing, reject detached HEAD, `main`, `master`, and branch mismatch.
Execution never creates, switches, or repairs the branch. Preserve unrelated work;
overlapping story changes or unrelated staged content that cannot be safely
isolated block execution.

Example goal, to enter only when choosing to authorize this scope after reviewing
the plan. Quoting or documenting this template is **not** execution permission:

```text
/goal Complete the approved stories in PLAN.md in standard mode. I authorize
scoped implementation, necessary project dependencies, required checks, and one
commit per successfully verified and reviewed story in this approved sequence,
subject to repository rules and runtime approvals. Load the advertised installed
prepare-implementation skill and read references/story-execution.md and
references/story-review.md in full. Follow their shared contract using the
CodexGoalMarkdown adapter and native story-reviewer when the mode/risk budget
requires it. Require the plan's exact existing branch and an existing commit;
reject main/master, detached HEAD, and mismatch before any writes. Do not create
or switch branches. Keep the plan stable with completion state and concise current
status in PLAN.md; append execution notes, evidence, dispositions, and resumption
checkpoints to docs/progress.md, and
maintain bounded version-1 memory.json only as the shared contract permits.
Preserve unrelated work. Stop with the story pending for missing required input,
protocol, reviewer/session, permission, invalid memory, or failed checks, review,
or commit. Report actual checks, review provenance, commit hashes, and remaining
limitations. Do not push, deploy, post externally, or perform sensitive operations
without separate explicit approval.
```

The plan is a completion contract, not permission to bypass sandbox or MCP rules.
Execution and story-commit authorization must be explicit and may cover the bounded
approved sequence. A plan, mode, or shared protocol cannot grant it. Narrower
planning-only, read-only, or no-commit requests remain binding and cannot establish
delivered stories. Dependency approvals still follow project/runtime rules;
Docker lifecycle, migrations including local/test, service operations, global
changes, and other sensitive actions require separate approval.

### Shared review and delivery gate

Use the shared `fast`, `standard` (default), or `deep` mode and implementation-risk
matrix. At most two native implementation advisors may contribute per story;
they are read-only and provide guidance, not edits, checks, posts, or delegation.
Record recommended, used, and skipped advisors with reasons.

The staged-review budget is identical to Ralph's:

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
OpenCode enforces `steps: 3` and an exact Git allowlist. Codex uses at most two
evidence-gathering tool turns then a result as behavioral guidance, not an equivalent
hard step cap or immutable sandbox/MCP restriction; parent runtime controls apply.

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

## Context and checkpoints

Keep `PLAN.md` as the stable plan and completion checklist. Append current results,
status, implementation notes, review dispositions, and the next action to
`docs/progress.md` after each reviewed story and before pausing or handing off blocked
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

Planning creates neither log nor memory. Resolve `docs/progress.md` and `memory.json`
from the worktree root, even with a custom plan path. After branch and worktree
guards pass, execution creates the journal only when a permitted checkpoint is
required and otherwise appends without resetting it. Never rewrite earlier entries
or headers, or read/migrate legacy execution logs. Existing plan notes are preserved;
explicitly approved cleanup during execution must preserve them in `docs/progress.md`
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

With one active plan per worktree, archive only after all tasks are verified and
required story commits succeed. Follow the [shared archival procedure](../ai/plugins/coding/skills/prepare-implementation/references/completed-run-archive.md):
preview and obtain explicit approval, append a final summary, copy the actual plan,
`docs/progress.md`, and existing `memory.json` to a unique archive, verify contents,
then remove approved active copies. Archive the memory with the run; do not reset
the journal or automatically create new state. Archive commits require separate
authorization. Ralph uses the same procedure, but only after runner validation
and exit. Neither workflow archives as a side effect of requirements drafting.

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
