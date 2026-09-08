# Recovering a stopped Ralph run

Ralph stops rather than repeatedly starting paid sessions when it lacks a valid
handoff, needs human input, or exhausts safe recovery. Diagnosis is separate from
restarting it. Start in the affected project's Git worktree root, not necessarily
this dotfiles checkout.

## Diagnose without changes

```sh
ralph --status
```

This command does not launch OpenCode, write state, create a lock, clear a stop,
or change retry counts. It reports runner state, current and next stories, last
outcome status, candidate/branch checks, attempt counts and remaining allowance,
detectable blockers, and local evidence paths. An exit code of zero means it
produced a diagnosis, not that the run is ready. It must be used alone, without
execution options such as `--resume` or `--max-iterations`.

Reasons and arbitrary content are withheld to avoid printing secrets. The report
is a snapshot, not a concurrency or successful-recovery guarantee. It does not
check runtime prerequisites or determine whether a code fix is correct. Missing
or malformed evidence is reported as a blocker; a held runner lock means wait and
inspect again after it stops. Verify surviving process identity separately before
considering any process action.

## Ask an assistant for help

In OpenCode, use the interactive command:

```text
/recover-ralph Assess why Ralph stopped in this project. Explain the blocker and
propose a repair. Do not change files or resume until I approve the actions.
```

In another supported harness, ask the primary assistant to load its advertised
`recover-ralph` skill. The skill is shipped in the `coding` bundle and does not
require a new subagent. It diagnoses the OpenCode Ralph runner, not a Codex Goal.
The autonomous Ralph executor must not use it to clear its own stop.

The assistant will inspect the applicable story, matching outcome and ledger,
recent progress, stop reason, Git changes, branch/commit evidence, and remaining
retries. It should explain the root cause, attempted fixes, uncertainty, and a
bounded resolution. It can perform approved repairs or provide steps for you to
perform, then verify the results. It must not invent credentials, approvals,
outcomes, or evidence to make the run continue.

| Stop condition | Recovery direction |
| --- | --- |
| Approval or missing input | Decide on the actual blocked action; restarting is not approval |
| Test/review failure | Inspect prior attempts and approve a concrete different fix |
| Missing tool or protocol | Fix the prerequisite with approval; do not substitute a weaker gate |
| Crash, timeout, or quota stall | Inspect partial work and surviving processes; resolve capacity before launch |
| Candidate changed | Reconcile ownership and changes before accepting a new baseline |
| Provisional completion | Preserve evidence; verify actual committed delivery, never just flip `passes` |
| Exhausted retries | Decide whether more attempts are justified; no automatic budget increase |
| Invalid ledger, plan identity mismatch, or rewritten history | Stop for explicit state/history reconciliation; never delete the ledger to start over |

## Repair and prepare

Approve a specific repair scope or perform the correction yourself. The assistant
then runs applicable checks and, when authorized, appends a recovery checkpoint to
worktree-root `docs/progress.md`. Create it only for a permitted repair checkpoint,
never during read-only assessment. Do not read or migrate legacy execution logs.
Existing history and unrelated work stay intact. Runner state,
retry counts, locks, and old outcomes must not be edited or removed by the helper.

After repair, the assistant reassesses the project and reports **ready to resume
after approval** or **not ready**, with evidence. `ralph --status` can still report
persisted blocked state or candidate mismatch; it is deliberately read-only and
does not acknowledge human reconciliation on your behalf. The helper's conclusion
does not mean the runner has already accepted the new baseline.

The default recovery workflow ends here. It does not spend another model session.

## Clear and resume with confirmation

If `.ralph-stop` exists, you can clear it yourself or explicitly authorize the
interactive assistant to remove that exact inspected file. This exception does
not apply to the autonomous Ralph executor. Retain any needed audit evidence
first; never remove a replaced stop file, follow a symlink, or delete a directory
or wildcard set of control files. No removal is needed when a crash left no stop
file. `make clean` does not remove Ralph controls or history.

The assistant must preview stop-file removal and the exact proposed launch
command, then obtain explicit confirmation. Approving repairs alone grants
neither action. You may approve removal without launching, or run Ralph yourself:

```sh
ralph --resume --max-iterations 5 --iteration-timeout 1800
```

These example limits mean five sessions this invocation and thirty minutes per
session; pick limits appropriate to the work. The per-story recovery budget
persists and is not reset by restarting. `--resume` acknowledges reconciliation;
it does not override stop files, plan/branch mismatches, active-session checks,
invalid completion evidence, or exhausted retries. If no ledger exists, use a
normal start after satisfying the clean-start requirements instead.

Immediately before approved removal/launch, recheck the stop identity, branch,
HEAD, candidate, ledger iteration/story, and process state. Material changes
invalidate the preview and require renewed confirmation. If the runner refuses,
report the new blocker instead of automatically retrying or increasing limits.

## Installation and evidence

Update both the single-file Ralph executable and the OpenCode command/skill assets
through the documented, separately authorized installation targets. Restart
OpenCode afterward; start a new Codex thread after refreshing its plugin. If an
older runner rejects `--status`, update it rather than running plain `ralph` as a
diagnostic fallback. Skill availability is not proof of an updated executable.

The runner's exact handoff contract is in
[`ralph-control.md`](../ai/plugins/coding/skills/prepare-implementation/references/ralph-control.md).
Status regression tests use isolated Git repositories and a fake harness, including
unchanged-state checks. Skill scenarios specify expected assistant behavior; they
are not evidence of live model recovery or a guarantee the next attempt succeeds.
