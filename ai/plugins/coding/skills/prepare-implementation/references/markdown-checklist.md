# Markdown implementation checklist

Write project-local `PLAN.md` unless the user specifies another path. Produce a
task checklist, not JSON. Inspect relevant project paths, instructions, and real
verification commands; mark missing checks unknown/unavailable rather than
inventing them. Planning does not execute tests or create execution-state files.

This is the Markdown task-source adapter for the same
[execution contract](story-execution.md) and [review protocol](story-review.md)
as Ralph JSON. Acceptance and delivery gates are shared; execution differs.
Ralph remains serial. Codex may use concurrent implementation workers under
[Codex concurrency](codex-concurrency.md), retaining native Goal continuation and
compaction without an external Ralph loop. Read that reference when planning
concurrency or executing this adapter.

## Plan contract

- Record objective, requirement sources, stable plan revision and approved scope
  baseline, scope/non-goals, working branch,
  authorization, delivery expectations, verification commands, and material gaps.
- Choose bounded-task or fuller PRD/dependency planning from scope. Map every
  story to approved request/brief or PRD requirements with one completion tracker.
  Explain dependency order and add phases when they clarify larger work. A separate
  PRD and full-run metadata are optional. Always record required plan archival
  under completed-run-archive.md, including exact paths and actual authority;
  use copy-only preservation when full-run enrollment is absent.
- Apply [acceptance coverage](../SKILL.md#preserve-acceptance-coverage). Use
  `Phase / requirements` (phase optional) to identify source criteria and, for split behavior,
  contributing stories and the story owning integrated acceptance. Put observable
  outcomes in acceptance criteria, alongside the relevant verification gates.
- The working branch must be an exact prepared Git branch before execution, not
  main/master or detached HEAD, with an existing commit. During planning it may
  be unknown, but label that an execution blocker. Planning creates no branches.
  Authorized Codex execution may prepare task branches/worktrees from approved
  existing commits under codex-concurrency.md; never switch the user's checkout.
- Use unique stable IDs (`US-001`), numeric priorities, and explicit dependencies
  (`none` or earlier IDs). Validate references, dependency order, and acyclicity.
  Validate the complete graph with Kahn-style readiness/cycle checks and reject
  missing references. The lead admits ready stories in priority/document order;
  dependencies require verified integration delivery, not worker completion.
- Name one integration owner. Before dispatch, assign each worker its stable
  story ID, absolute worktree, exact branch, approved base commit and owned paths.
  Record shared build/output ownership and host resource coordination. Require
  an established clean committed baseline; never copy or commit user dirty work
  to prepare a task. Native child spawn does not bind cwd; use assigned paths.
- Bound each story to one focused implementation, verification, review, and
  commit unit. Include user benefit, relevant paths, observable criteria, tests,
  typecheck, formatting/lint commands, and `verify-interface` for UI changes.
  Report unavailable checks honestly; unmet required criteria block completion.
- Start new story, acceptance, and workflow checkboxes unchecked. Preserve
  existing checked state and evidence during approved scoped continuation.
- Require the shared `fast`/`standard`/`deep` advisor and staged-review budgets,
  defaulting to `standard`. Mode-permitted self-review is not independent review.
  Native review must use `story-reviewer`; never substitute a general reviewer
  or a human ad hoc to bypass an unavailable required gate.
- Keep scope, requirements, criteria, dependencies, completion checkboxes, and
  concise current status in the plan, not repeated execution narratives.
  Execution evidence and checkpoints go in append-only `progress.md`;
  validated patterns/suppressions go in bounded `memory.json`. These paths are
  relative to the worktree root, even when the task source has a custom path.
- Mark a story delivered only after checks, review, and an explicitly authorized
  per-story commit succeed. Planning/plan approval is not execution or commit
  permission. A clear authorized launch may grant implementation, tests, budgeted
  delegation and local commits across the eligible sequence without repeating
  activation per story. Honor narrower instructions and report undelivered work.

## Recommended advisors

Preserve supplied implementation recommendations; infer only useful exact known
role names, never a quota. Codex implementation specialists may write and test
in explicitly assigned task worktrees. Read-only advisors remain under the shared
mode budget (at most two per story). The lead owns integration and trackers.
Record worker ownership and each advisor's bounded question in the plan;
record actual invocation or a skip reason in `progress.md` at execution time.
For planned Codex team execution, identify run-agent-team as the dispatch owner
procedure and name one batch lead for both dispatch and integration. Record
model/capacity limits and worktree ownership in the handoff, not another registry.
A planning document grants no team execution or worktree lifecycle authority.
Discovery is not invocation and a definition does not prove native availability.

The staged reviewer is fixed to Codex `story-reviewer` when the mode requires
native review. Supplied general review recommendations may inform risk/advisor
selection but cannot replace this gate or extend its budget. The executor loads
the full installed `story-review.md` and supplies it with the compact packet,
without embedding the diff; retain the actual returned native reviewer ID for
at most one targeted same-session follow-up.
Embed the complete protocol/schema in the invocation message itself, never an
inherited tool-output reference. Apply the execution contract's packet preflight.
Start a fresh reviewer session per story and record its actual selected role and
returned ID alongside the story/attempt; labels alone do not establish identity.

## Template

Replace placeholders using project evidence; repeat only the story section.
Include the shared resume handoff once so a Goal loads the contract even when
the skill is not otherwise active. Do not repeat an execution checklist in every
story. The compact shape is suitable for bounded tasks; larger work can add design,
phases and PRD references without introducing another completion tracker.

```markdown
# Implementation plan: <feature>

## Objective and context
- Objective: <observable outcome>
- Sources: <approved request/brief or PRDs and inspected paths>
- Plan revision: <stable scope revision, e.g. v1; approved baseline revision/ref when known>
- Scope / non-goals: <included and excluded work>
- Working branch: <exact prepared branch; unknown is an execution blocker>
- Integration owner: <one lead; owns integration index, markers, progress and memory>
- Mode: standard
- Authorization: <actual sequence execution/delegation/local-commit grant or pending>
- Delivery: one authorized commit per verified and reviewed story
- Verification: <real commands; supported exemptions and unavailable checks>
- Assumptions / open questions: <material gaps or none>

## Approach and dependencies
<source-backed approach and prerequisite order; phases only if useful>

## Ordered stories

### US-001 - <bounded story title>
- [ ] Story complete
- Priority: 1
- Depends on: none
- Phase / requirements: <approved request/brief criteria or PRD references; phase optional>
- User story: As a <user>, I want <capability> so that <benefit>.
- Relevant paths: <source/test paths>
- Worker assignment: <absolute task worktree; exact branch; approved base commit>
- Owned paths: <bounded repository-relative paths; shared paths have one owner>
- Shared resources: <build/output roots; host resource ownership/coordination or none>
- Implementation advisors: <optional known roles and bounded questions, or none>

#### Acceptance criteria
- [ ] <required behavior: condition/action and expected result>
- [ ] <source constraints/edge cases; integration outcome and contributors if split>
- [ ] <required tests/typecheck/lint/browser criteria; supported exemptions>

## Resume and delivery
- For authorized execution, load the installed prepare-implementation skill; read
  references/story-execution.md and references/story-review.md in full relative
  to its advertised base. Follow CodexGoalMarkdown, the mode/risk budgets and
  native story-reviewer when required. Missing protocol/tools/reviewer blocks;
  do not invent paths or substitute a general reviewer.
- Read this plan, relevant append-only progress.md entries and memory.json if
  present from the worktree root. Planning creates neither file. Execution may
  create a journal only after branch and unrelated-work guards pass; invalid
  memory blocks, missing memory is normal. Preserve history; update bounded
  memory only from verified reusable findings after passing review.
- Execute the approved plan revision; completion-marker updates do not advance
  its scope revision. Reconcile material scope/acceptance/dependency revisions
  against user approval and delivery evidence; a revision label is not a grant.
- Carry the actual authorized launch scope across eligible stories and
  continuation; verify it without another activation request per story. Require
  the exact existing prepared branch and commit before writes, staging and commit;
  reject main/master, detached HEAD and mismatch. Prepare task branches/worktrees
  only with a scoped lifecycle grant and clean committed baseline; never switch
  the user's checkout or copy/commit dirty work as preparation.
- For authorized Codex team execution, discover run-agent-team and follow its
  preflight and dispatch-before-wait contract. One designated lead owns dispatch
  and integration; workers must not route back into orchestration. Keep native
  story-reviewer availability and all existing gates.
- Admit dependency-ready stories under codex-concurrency.md. Workers use explicit
  assigned paths; the lead owns integration, progress and memory. Coordinate host
  resources and shared outputs; freeze only the candidate and conflicting resources.
  Other isolated workers may continue. Integrate one bounded story with applicable
  checks and at most two read-only advisors. Stage only its intended candidate;
  keep it immutable during
  review. Supply the full protocol/schema in each native invocation; use a fresh
  actual reviewer session per story and at most one initial plus one targeted
  remediation pass in the same session. Preserve final blockers until verified
  material resolution; continuation never resets review budgets.
- Record actual checks, review/session provenance, findings/dispositions, authority
  and checkpoints in progress.md. Finalize only the selected completion marker
  after checks/review pass. Delivery requires its authorized local commit; on
  failed finalization/commit follow shared marker restoration and stop. Never
  claim unchecked, blocked, unverified or uncommitted work delivered.
- Report delivered scope, actual commit hashes/checks/review and remaining gaps.
  Keep Codex native Goal and Ralph/OpenCode separate; never start nested loops,
  implicit pushes, deployments, posts or sensitive operations.
```

For a Python client story, `python-pro` may advise on implementation risks while
the executor edits/tests and `story-reviewer` performs the required staged review.
Documentation-only work may record typecheck as not applicable with an explicit
reason. These are examples, not mandatory architecture or fixed agent counts.

## Handoff and existing plans

Complete the shared acceptance-coverage audit before handoff. Report source
coverage, integrated acceptance owners, approved exclusions, and exact unresolved
gaps; do not present a draft with acceptance gaps as ready for execution.
Report path, dependency/ordering checks, assumptions, unresolved verification,
branch preparation, and authorization gaps. Offer this launch text only after
plan review; do not enter it or execute anything during planning:

```text
/goal Execute the approved revision of PLAN.md in standard mode using the installed
prepare-implementation shared execution/review contracts. I authorize in-scope
implementation, required checks, budgeted delegation, scoped task worktree setup
from approved commits and one local commit per
passing story across this eligible sequence. Preserve unrelated work and all
branch, review, permission and sensitive-operation boundaries.
```

Every completed goal requires plan archival. A bounded task without a separate
PRD uses copy-only preservation under completed-run-archive.md. If full-run
archival is selected, planning additionally records the exact primary PRD path,
bound run ID and actual archival/removal plus closeout commit scope. Add the
following optional closeout instruction only for that enrolled workflow:

```text
After verified delivery, I authorize the installed archive_run.py to archive the
exact run-owned PRDs and task source in the bound work-run manifest, root
progress.md and existing memory.json, removing only verified active copies, and
one closeout commit. Preserve unrelated files and runner controls.
```

The user must actually grant that scope; quoted launch text is not authorization.
Codex continues in its native thread and rereads state after compaction/resumption.
Do not force fresh sessions, install compaction hooks, invent runner iteration
limits, or run `/compact` as a shell command.

Do not create/reset progress or memory during planning. Existing plans may have
implementation notes: preserve them and completed checkboxes. Relocating that
evidence requires explicit cleanup approval during authorized execution and must
preserve it in progress.md before removing it from the plan. Do not replace an
unfinished run. If completion archival was missed, use the shared copy-only
preservation fallback and verify its receipt/hashes before an authorized new-plan
write; failed preservation blocks replacement. Archive completed runs under the shared
[archival procedure](completed-run-archive.md). A resumed old plan missing the
branch or shared contract needs a scoped plan update, not silent execution with
weaker rules.
