# Ralph iteration control

This protocol applies to the OpenCode Ralph runner, not native Codex Goal.
Read it alongside story-execution.md and story-review.md at execution time.
The runner, not an agent, persists the current iteration as `running` before it
launches OpenCode. Continuation is denied until a fresh outcome is validated.

## Ownership and handoff

- Work at the Git worktree root on the exact story selected by the runner.
- The initial worktree/index must be clean and plan.json committed. The runner
  fingerprints tracked index/worktree content and nonignored untracked files.
  Submodules are unsupported. Matching staged/unstaged work from a previous
  validated handoff belongs to recovery; unexpected user changes require a stop.
- The runner supplies `RALPH_ITERATION_ID`, `RALPH_STORY_ID`, and
  `RALPH_OUTCOME_FILE` as environment variables and in the invocation context.
  Use those exact IDs/path; never guess or reuse an older result.
- The outcome is project-local `.ralph-outcome-<32-lowercase-hex-ID>.json`.
  Write one complete JSON object, preferably by atomic replacement. Keep it out
  of Git staging and commits, along with `.ralph-stop`. They remain local audit
  artifacts; the runner rejects tracked control files, even if later removed.
- Do not edit the ledger at `git rev-parse --git-path ralph/state.json`, counts,
  lock, or other outcomes. Runner ownership is a protocol boundary, not isolation
  from an unrestricted process running as the same user.

## Outcomes

After a successful passing story commit, write:

```json
{
  "version": 1,
  "iteration_id": "<supplied iteration ID>",
  "story_id": "<supplied selected story ID>",
  "status": "completed"
}
```

Completion requires a new descendant commit containing the selected story's
`passes: true`, no other plan changes, and no remaining nonignored candidate
changes. Neither a provisional marker, final message, nor zero process exit is
enough. The runner cannot prove the semantic correctness of tests or reviews;
the executor must truthfully satisfy the shared gate.

For unfinished but recoverable implementation/review work, write:

```json
{
  "version": 1,
  "iteration_id": "<supplied iteration ID>",
  "story_id": "<supplied selected story ID>",
  "status": "retryable",
  "finding_ids": ["stable-unresolved-finding-id"],
  "attempted_action": "Concrete fix attempted and why it was insufficient",
  "next_action": "Specific materially different next approach within authorization",
  "evidence": "Actual check/review result and relevant artifact path"
}
```

Keep the story incomplete and preserve the candidate. Append a checkpoint to
worktree-root `docs/progress.md` only when the shared write guards permit it,
with unresolved findings, attempted fixes, checks, reviewer provenance, and the
next action before writing the outcome. Do not update review memory from a failed
review. The runner requires changed candidate state or new verification evidence
relative to a prior handoff. Repeating the same finding set and normalized next
action stops recovery. Textual evidence is an agent attestation, not machine proof
that a new approach will work; do not paraphrase a failed approach to evade limits.

A fresh authorized recovery receives a new iteration ID and a new bounded review
cycle for the same story. It must inspect the checkpoint and existing candidate,
carry forward prior findings/dispositions, and continue remediation. Within that
cycle, use one initial and at most one targeted same-reviewer-session pass.

For human input/approval, missing required reviewer/protocol/session/tools,
failed commit/finalization, contradictory requirements, or no credible fix:

```json
{
  "version": 1,
  "iteration_id": "<supplied iteration ID>",
  "story_id": "<supplied selected story ID>",
  "status": "blocked",
  "reason": "Concise blocker and required human action; no secrets"
}
```

Append the checkpoint to `docs/progress.md` when safe, write the blocked outcome,
then create `.ralph-stop` with
a concise reason if file access is available. Create the stop file last because
the runner observes it while OpenCode is running and terminates the managed
process group. Never clear it automatically. If no outcome can be written, report
the blocker and exit; absence of an outcome still stops continuation.

## Budgets, interruption, and resumption

- Default recovery allowance is two additional sessions per story (three total).
  `--max-story-retries 0..5` explicitly changes the persisted budget, not consumed
  counts. Do not ask the model to increase the limit itself.
- `--max-iterations` bounds sessions per invocation. A validated ready handoff
  can resume later if its candidate is unchanged; counters survive restart.
- `.ralph-stop` always stops, even with a completed plan or `--resume`.
- Missing/malformed/stale outcomes, unsuccessful process exits, timeouts, and
  signals stop without another automatic session. A crash leaves durable
  `running` state rather than an implicit retry instruction.
- Humans may reconcile work, clear the stop file, then invoke `ralph --resume`.
  It accepts the reconciled baseline but never resets counts, bypasses a live
  prior session, switches plans, or accepts an uncommitted completion marker.
  Do not delete the ledger to reset budgets or automatically issue `--resume`.
- A separate interactive assistant may use the installed `recover-ralph` skill
  to diagnose with `ralph --status` and prepare approved repairs. Removing the
  exact inspected stop file or launching Ralph requires an exact-action preview
  and explicit user confirmation. This exception never applies to the autonomous
  executor clearing its own stop. No helper may edit the ledger or reset counts.
- `--iteration-timeout SECONDS` is optional, default 0 (unlimited). Expiry
  terminates the managed OpenCode process group and stops; it is not an idle
  output detector. Child processes that deliberately escape that group are not
  covered. Review the interruption before resuming.
- On a usage-limit stall without process exit, only an enabled timeout, user
  signal, or stop file can end the running session. There is no guaranteed
  provider-specific quota detection.

Reports must distinguish committed completion, recoverable pending work, and
human-blocked work. Never claim a solution is impossible merely because a retry
budget was exhausted; report the attempts and the unresolved decision instead.

Do not archive state or append post-run summaries inside the final iteration.
After the runner validates completion and exits, a separate interactive assistant
may offer the explicitly approved [completed-run archive](completed-run-archive.md).
Never remove `plan.json` before runner validation or modify runner controls as
part of archival.
