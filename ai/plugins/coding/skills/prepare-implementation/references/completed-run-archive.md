# Completed-run archival

One active plan belongs to one Git worktree. Ralph and Codex Goal use the same
completed-run archive, not an automatic reset when a new feature is planned.
This is a separately approved manual operation, not a runner feature or authority
granted by planning, story execution, or story-commit approval.

## Verify and obtain approval

1. Verify every story/task is complete, required checks and reviews passed, and
   required story commits succeeded using actual Git and journal evidence. A
   checkbox, `passes: true`, or process exit alone is insufficient. After a merge,
   use retained commits or verifiable merged PR/squash-commit evidence together
   with the journal to establish delivery. The original branch need not exist;
   its deletion or lack of ancestry after a squash merge is not itself a blocker.
   Do not rewrite the plan's historical branch or invent missing commit evidence.
   If completion evidence is missing or the run is unfinished, stop without
   archiving or replacing its plan.
2. For Goal, wait until the final story commit succeeds. For Ralph, additionally
   wait until the runner validates completion and exits; leave root `plan.json`
   and the final candidate unchanged until then. Stop files, unresolved runner
   state, or active processes block archival pending human reconciliation.
3. Inspect the exact worktree, current branch (or detached HEAD), HEAD commit,
   state-file ownership, and changes. Completed-run archival is permitted on any
   branch, including main/master or a different feature branch, without requiring
   the plan's original branch to exist or be checked out. Branch identity is
   provenance, not an archival gate; never create or switch branches for archival.
   Verify the files belong to the completed run, not another active run, and
   preserve unrelated work. Preview a final journal summary, all source and
   destination paths, removal of the active copies, and whether a separate archive
   commit is requested. Obtain explicit approval before any archival writes.
4. Recheck that the approved evidence and paths have not materially changed. Use a
   unique project-local `archive/YYYY-MM-DD-feature-name/` destination; never
   overwrite an archive, follow out-of-worktree symlinks, or use wildcard cleanup.

## Preserve the complete run

After approval, append the final summary to `docs/progress.md`: feature/task source,
actual story commits, checks/review outcomes, remaining limitations, and archival
approval/destination. This permitted checkpoint may create the journal if absent;
never fabricate missing execution evidence. This is post-run finalization, not an
extra story bookkeeping commit. Record the original plan branch, current archival
branch/HEAD, and any merged-delivery evidence used when the original commits are
unavailable.

Copy the actual task source and existing state together, preserving relative paths:

```text
archive/YYYY-MM-DD-feature-name/
  PLAN.md                 # Or plan.json, whichever this run used
  memory.json             # If present
  docs/
    progress.md
```

For a custom task-source path, preserve its worktree-relative path. Do not archive
both plan formats unless both are verified run-owned and explicitly approved.
Verify every copy matches its source and recheck that sources are unchanged
immediately before removing any approved active copy.
On failure, preserve sources and available archive evidence, report partial state,
and stop; do not overwrite, delete, or retry cleanup automatically.

Move the journal intact by this verified copy/remove procedure; never truncate or
rewrite its history. Archive memory with the run rather than carrying it into a
new run. New execution starts with fresh bounded memory; durable repository
guidance already promoted through the reviewed workflow remains in `AGENTS.md`.
Do not create a replacement plan, journal, or memory as part of archival.

Leave PRDs, unrelated files, and all Ralph ledger/lock/stop/outcome controls intact.
Archival does not reset runner state or authorize reuse of a completed Ralph
worktree; new Ralph runs still need their own valid prepared worktree and plan.
PRD replacement uses the separate requirements preservation guard.

This branch-independent permission applies only to completed-run archival. New
implementation or resumed execution still requires its exact prepared branch and
all existing execution guards; archival approval does not grant execution authority.

Report archived paths, verification, removed active paths, and any partial work.
Commit only with separate explicit authorization, following repository checks and
Git rules; otherwise report the uncommitted archive changes. Never push implicitly.
