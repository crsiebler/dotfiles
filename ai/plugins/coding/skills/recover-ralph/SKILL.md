---
name: recover-ralph
description: Diagnoses stopped Ralph runs, guides approved repairs, and prepares continuation without automatically restarting the agent loop.
---

# Recover Ralph

This is an interactive recovery workflow for the primary assistant, not another
autonomous Ralph iteration. Default to read-only assessment and finish with a
recovery report. Invoking this skill is not authorization to edit, remove a stop
file, raise a budget, commit, start Ralph, or perform the originally blocked action.
The autonomous Ralph executor must not invoke this workflow to clear its own stop.

## Inspect first

1. Establish the user's intended project and Git worktree root. Run `ralph --status`
   there, without execution flags. If unsupported, report the installed-version
   mismatch and propose an authorized update; never fall back to plain `ralph`.
2. Use the advertised installed `prepare-implementation` skill to locate its
   `references/ralph-control.md` and `references/story-execution.md`; read them for
   the applicable contract, not to generate a plan or begin story execution.
   Resolve relative to the installed skill, not checkout or guessed cache paths.
   Missing protocol is a blocker, not permission to invent one.
3. Read the relevant `plan.json` story, recent worktree-root `docs/progress.md`
   checkpoints if present, stop reason if present, and the outcome matching the
   ledger's iteration and story
   IDs. Locate the ledger through `git rev-parse --git-path ralph/state.json`.
   Do not select an outcome by timestamp alone or trust a file's name without
   validating its IDs. Inspect only necessary fields and summarize safely; do not
   dump raw ledger/outcome/log contents, environment values, or credentials.
4. Check branch, HEAD, committed plan markers, staged/unstaged changes, candidate
   ownership, last attempts, and remaining retries. A checkbox or outcome alone
   is not proof of delivery. Distinguish runner-owned partial work from user edits.
   Do not stage, unstage, reset, or overwrite anything during assessment.
5. Check for an active runner or surviving prior process using read-only process
   inspection. A lock is not proof that every child has stopped; a PID alone is
   not proof of process identity. If uncertain, stop for inspection. Never kill a
   process merely because its PID appears in the ledger.

`--status` is a read-only snapshot, not a repair, permission grant, or guarantee.
Exit zero means a diagnosis was produced, not that execution is safe. Its reasons
are intentionally generic to avoid exposing secrets. Runtime prerequisites and
the technical resolution of a blocker need separate evidence.

## Explain and propose

Give a concise report:

- Project, selected story, last runner/outcome state, and evidence inspected.
- Why Ralph stopped; distinguish confirmed root cause from uncertainty.
- What was already attempted, what remains, and remaining recovery allowance.
- Whether the runner is active, and any worktree/branch/commit inconsistencies.
- Exact proposed repair, its scope/risks, verification, and approvals needed.
- Whether the assistant can perform the repair or the user must perform it.

An approval blocker requires approval for that actual operation, not a retry.
A permission denial must not be evaded via another tool or identity. Missing
credentials should be configured privately by the user; do not read credential
stores. Invalid state, a changed plan identity, ambiguous ownership, rewritten
history, or exhausted retries require explicit reconciliation, not a reset.
Do not call a task impossible just because the automatic retry budget expired.

## Repair only within approval

Preview the bounded action and obtain user approval before remediation writes or
commands with side effects. Existing explicit approval can cover the displayed
repair scope; do not repeatedly ask for the same grant. Sensitive operations,
dependency installs, commits, and process/service changes retain their separate
policy requirements. Alternatively, provide instructions for the user to perform
the action, then inspect the resulting evidence instead of assuming success.

Perform only the approved repair and relevant verification. Preserve unrelated
work and story completion evidence. Never edit/delete the runner ledger, lock,
retry counters, or previous outcome files; never fabricate an outcome to satisfy
the supervisor. Do not reset `memory.json` or mark a story complete to unblock it.
Do not raise recovery limits without a separately previewed and approved budget
decision using the runner's supported option, never direct state editing.

Append a dated recovery checkpoint to worktree-root `docs/progress.md` only within
approved repair scope: story/iteration, original blocker, actual approvals, repair, checks, remaining
issues, and next action. Preserve prior entries. If the branch or state makes even
that write unsafe, report the checkpoint in the response instead.
Create the journal only when this permitted checkpoint is required, never during
read-only diagnosis. Do not read or migrate legacy execution logs.

## Prepare, then optionally resume

Rerun `ralph --status` and inspect the final candidate, branch, committed markers,
process state, and retry allowance. A changed candidate or persisted blocked state
can still say "needs reconciliation" after a valid repair: status never rewrites
the ledger. Explain that distinction; do not claim the ledger is now ready.
If the substantive blocker, ownership, prerequisites, or budget remain unresolved,
leave the stop file intact and report what remains. Finish by default with either
"ready to resume after approval" or "not ready", with supporting evidence.

If the user wants the assistant to clear the stop and/or launch Ralph:

1. Preview the exact worktree, stop-file path and current identity/content digest
   when present, the reason it is now safe to clear, and the exact proposed
   command and limits, for example `ralph --resume --max-iterations 5
   --iteration-timeout 1800`. Choose limits with the user; they are not defaults.
   Explain that launch authorizes scoped passing-story commits and consumes model
   usage. Removal and launch are separate actions and can be approved separately.
2. Obtain explicit confirmation after that preview. Approval to repair is not
   approval to remove `.ralph-stop` or restart the loop. Never add `--resume` or
   raise retries merely to make an error disappear.
3. Immediately recheck the branch/HEAD, candidate, ledger iteration/story, stop
   file identity, and process state. If they changed materially since the preview,
   stop and obtain a new approval for revised actions.
4. With exact-path removal approval, remove only the verified `.ralph-stop` at
   the intended worktree root. Do not follow symlinks, remove directories, use a
   wildcard, delete state/outcomes, or clear a newly replaced stop file. If absent,
   skip removal; crashes may leave only a blocked/running ledger.
5. Run the approved command only with explicit launch approval. Observe its
   result; do not retry automatically if it refuses or stops again. Report
   preparation separately from actual launch and verified completion.

The narrow stop-removal exception applies only to this separate interactive
assistant acting on explicit user confirmation. Autonomous Ralph must still
never clear its stop file, reset state, or increase its own budget.
