# Markdown implementation checklist

Write project-local `PLAN.md` unless the user specifies another path. Produce a
task checklist, not JSON. Inspect relevant project paths, instructions, and real
verification commands; mark missing checks unknown/unavailable rather than
inventing them. Planning does not execute tests or create execution-state files.

This is the Markdown task-source adapter for the same
[execution contract](story-execution.md) and [review protocol](story-review.md)
as Ralph JSON. The formats differ, not the story lifecycle. Codex retains native
Goal continuation and compaction; it does not run the external Ralph loop.

## Plan contract

- Record objective, requirement sources, scope/non-goals, working branch,
  authorization, delivery expectations, verification commands, and material gaps.
- The working branch must be an exact prepared Git branch before execution, not
  main/master or detached HEAD, with an existing commit. During planning it may
  be unknown, but label that an execution blocker. Do not create/switch branches.
- Use unique stable IDs (`US-001`), numeric priorities, and explicit dependencies
  (`none` or earlier IDs). Validate references, dependency order, and acyclicity.
  Execution selects the lowest numeric priority eligible incomplete story.
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
  Execution evidence and checkpoints go in append-only `docs/progress.md`;
  validated patterns/suppressions go in bounded `memory.json`. These paths are
  relative to the worktree root, even when the task source has a custom path.
- Mark a story delivered only after checks, review, and an explicitly authorized
  per-story commit succeed. Planning/plan approval is not execution or commit
  permission. Honor narrower instructions and report undelivered work.

## Recommended advisors

Preserve supplied implementation recommendations; infer only useful exact known
role names, never a quota. The executor implements and tests. Implementation
specialists are read-only advisors under the shared mode budget (at most two),
not competing file editors. Record the role's bounded question in the plan;
record actual invocation or a skip reason in `docs/progress.md` at execution time.
Discovery is not invocation and a definition does not prove native availability.

The staged reviewer is fixed to Codex `story-reviewer` when the mode requires
native review. Supplied general review recommendations may inform risk/advisor
selection but cannot replace this gate or extend its budget. The executor loads
the full installed `story-review.md` and supplies it with the compact packet,
without embedding the diff; retain the actual returned native reviewer ID for
at most one targeted same-session follow-up.

## Template

Replace placeholders using project evidence; repeat only the story section.
The resume instructions below must be included in the generated plan so a Goal
loads the shared contract even when the planning skill is not otherwise active.

```markdown
# Implementation plan: <feature>

## Objective and context
- Objective: <observable outcome>
- Sources: <requirements and inspected paths>
- Scope: <included work>
- Non-goals: <excluded work>
- Working branch: <exact prepared branch; unknown is an execution blocker>
- Mode: standard
- Authorization: <actual execution/commit grant, or pending; sensitive actions excluded>
- Delivery: one authorized commit per verified and reviewed story
- Verification commands: <real format/lint/typecheck/test commands and unavailable checks>
- Assumptions / open questions: <material gaps or none>

## Ordered stories

### US-001 - <bounded story title>
- [ ] Story complete
- Priority: 1
- Depends on: none
- User story: As a <user>, I want <capability> so that <benefit>.
- Relevant paths: <source/test paths>
- Recommended implementation advisors: <known roles or none>
- Advisor questions: <bounded read-only guidance needed or not needed>
- Staged reviewer: story-reviewer when required by the shared mode/risk budget

#### Acceptance criteria
- [ ] <observable behavior>
- [ ] <regression/edge case verified>
- [ ] <typecheck passes; explicit treatment of unavailable checks>

#### Execution checklist
- [ ] Verify authorization and exact prepared branch; read project instructions and state.
- [ ] Research and implement this story with tests; use only budgeted read-only advisors.
- [ ] Run formatting, lint, typecheck, tests, and UI verification as applicable.
- [ ] Stage the intended candidate and complete the shared mode-aware review gate.
- [ ] Resolve findings, rerun affected checks, and perform at most one targeted re-review.
- [ ] Update bounded memory and append progress; finalize task metadata and commit.

## Resume and delivery
- For authorized execution, load the installed prepare-implementation skill and
  read references/story-execution.md and references/story-review.md relative to
  that skill's reported base directory. Follow its CodexGoalMarkdown adapter.
  If discovery, a reference, or required story-reviewer invocation is unavailable,
  stop with the blocker; do not invent a path, substitute a reviewer, or skip rules.
- Read this plan, relevant latest docs/progress.md entries, and memory.json if
  present, resolving state paths from the worktree root. Keep this plan concise:
  scope, requirements, criteria, dependencies, completion state, and current status.
  Put commands/results, changed paths, review findings/dispositions, blockers,
  approvals, actual advisor use, commit status, and resumption checkpoints in
  append-only docs/progress.md; never rewrite its history. Create it only when
  authorized execution requires a checkpoint and branch/unrelated-work guards pass.
- Missing memory.json is normal: check existence before reading, use empty
  version-1 memory in process, and create it only after passing review. Preserve
  invalid memory and stop; keep at most 20 patterns and 20 suppressions.
- Recheck the prepared branch before changes, staging, and commit. No branch
  creation/switching, implicit pushes, external posts, or sensitive-operation grants.
- Native review uses story-reviewer, its supplied shared JSON schema, and at most
  one initial plus one targeted same-session pass. Self-review is permitted only
  by the mode/risk budget; malformed/blocked review stops delivery.
- Provisional completion boxes are staged only after checks/review pass; a story
  is delivered only after its authorized commit succeeds. On failure follow the
  shared marker-restoration and checkpoint procedure. Never claim unchecked work done.
- [ ] Final report: actual commits, checks/review outcomes, delivered scope, remaining gaps.
- After all tasks are verified and committed, offer separately approved archival
  using references/completed-run-archive.md from the installed skill. Do not move
  active state or commit an archive under story-commit authorization alone.
```

For a Python client story, `python-pro` may advise on implementation risks while
the executor edits/tests and `story-reviewer` performs the required staged review.
Documentation-only work may record typecheck as not applicable with an explicit
reason. These are examples, not mandatory architecture or fixed agent counts.

## Handoff and existing plans

Report path, dependency/ordering checks, assumptions, unresolved verification,
branch preparation, and authorization gaps. Offer this launch text only after
plan review; do not enter it or execute anything during planning:

```text
/goal Execute the approved PLAN.md using prepare-implementation's shared story
execution and staged-review contracts in standard mode. I authorize scoped
implementation, required project dependencies, checks, and one commit per passing
story. Read PLAN.md, docs/progress.md, and memory.json as specified. Keep task
checkboxes and concise current status in PLAN.md, append execution history to
docs/progress.md, and update bounded memory only from validated review evidence.
Preserve unrelated work and existing
permission boundaries; ask for sensitive operations. Stop on branch, verification,
review, memory, or commit blockers. Do not push, deploy, or post externally.
```

The user must actually grant that scope; quoted launch text is not authorization.
Codex continues in its native thread and rereads state after compaction/resumption.
Do not force fresh sessions, install compaction hooks, invent runner iteration
limits, or run `/compact` as a shell command.

Do not create/reset progress or memory during planning. Existing plans may have
implementation notes: preserve them and completed checkboxes. Relocating that
evidence requires explicit cleanup approval during authorized execution and must
preserve it in docs/progress.md before removing it from the plan. Do not replace an
unfinished run. Archive completed runs only under the shared
[archival procedure](completed-run-archive.md). A resumed old plan missing the
branch or shared contract needs a scoped plan update, not silent execution with
weaker rules.
