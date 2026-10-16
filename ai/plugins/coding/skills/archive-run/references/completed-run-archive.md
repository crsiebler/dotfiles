# Deterministic completed-run archival

The serialized adapter identifier `CodexGoalMarkdown` denotes the existing
Markdown checklist/evidence format; it does not require the Codex harness.
Keep existing manifests and identifiers unchanged. Runtime capability checks
belong to the invoking execution workflow, not this archival helper.

One active run belongs to one Git worktree. The installed skill's
[archive helper](../scripts/archive_run.py) owns file selection, validation,
copying, verification, and active-copy removal. Do not reproduce these operations
with LLM-written shell commands. Python 3.11+, Git, and POSIX file locks are
required; no packages, model calls, or network access are needed.

## Required plan archival; optional full-run enrollment

Archive the plan after the entire goal is reached. Prefer the verified full-run
procedure below when enrolled; otherwise use copy-only plan preservation. If
completion archival was missed, preserve the old completed plan before generating
its replacement. Failed preservation blocks replacement; never silently overwrite.
An unfinished plan must be continued or explicitly reconciled, not replaced.

Ordinary bounded-task execution needs no separate PRD or work-run manifest. The
verified full-run procedure requires enrollment. The authorized execution owner
verifies/binds the manifest and any approved saved requirements snapshot before
the first execution checkpoint. Planning preserves supplied metadata only;
requirements authoring owns outcomes, scope and acceptance. Missing
archival inputs block archival, not an otherwise valid execution plan. Do not
retroactively fabricate structured observations or completed task evidence.

## Run manifest

Each associated PRD contains exactly one fenced `work-run` JSON block. All PRDs
for a run contain the same manifest; bind the task source before the first execution checkpoint, without
changing the Ralph task-source schema. Paths are relative to the Git worktree
root, even when the PRD or plan is in another directory.

```work-run
{
  "version": 1,
  "run_id": "search-20261003",
  "feature": "search",
  "adapter": "CodexGoalMarkdown",
  "task_source": "PLAN.md",
  "prds": ["tasks/prd-search.md"],
  "journal": "progress.md",
  "memory": "memory.json",
  "archive_on_completion": true
}
```

Use a stable, unique lowercase run ID and feature slug: letters, digits, hyphens,
at most 80 characters. For OpenCode use `RalphJSON` and `plan.json`; `prd.json` is
not the current Ralph task source. Additional PRDs must be explicitly declared,
run-owned, and have distinct basenames, including case-insensitive comparison.
Never collect PRDs with a wildcard. The journal and memory paths are fixed at
root `progress.md` and `memory.json`. Missing memory is normal; missing PRD,
task source, journal, manifest, or completion evidence blocks archival.

Requirements authoring does not create run metadata. For an enrolled archival
workflow, the authorized execution owner generates the stable run ID and binds adapter,
task_source and associated PRD inventory before the first execution checkpoint. Preserve existing run
IDs and approved requirement prose during scoped revisions. Legacy unbound
metadata may be reconciled before execution under that same scoped authority; never fabricate legacy evidence. Metadata
expresses intended behavior, not user authorization.

## Completion and authority

An execution request may authorize the whole approved sequence, including
automatic archival/removal of its exact declared active artifacts and one
closeout commit. Once granted, carry that authority through continuation; do not
request it again. If archival/removal or commit authority is genuinely missing,
preview the exact paths/result and request only the missing scope. Narrower
instructions and runtime restrictions still apply. Planning only verifies existing preservation receipts and current hashes before
authorized replacement; missing or mismatched evidence blocks replacement. The
authorized execution/closeout owner performs preservation, never planning itself.

For each delivered story, the executor stages a structured `story-result` block
in `progress.md` with the completion marker, after passing checks and review but
before the story commit. Follow the invoking workflow's pre-commit evidence and marker finalization rules.
These records report observed outcomes; they must never fabricate passing checks,
native review sessions, or approvals. The helper independently verifies that
each passing record and its completed task marker occur together in reachable
Git history and that all active artifacts match HEAD. It does not rerun tests,
reperform reviews, or establish the truth of an executor's recorded observations.

For Goal, invoke the helper after the final successful authorized story commit.
For Ralph, the **invoking assistant**, outside the story agent, waits for the
supervisor to validate completion and return exit zero, then invokes the helper.
The story agent must not archive or remove plan.json inside the last iteration.
The helper also refuses a held runner lock, live recorded runner/child process,
stop file, or runner state other than completed. A fully checked old plan without
structured records or a validated Ralph completion ledger is insufficient.
CLI-only Ralph invocations without an invoking assistant do not automatically
archive; do not claim that the supervisor implements a post-run hook.

## Invoke the installed helper

Discover `archive-run` and resolve `scripts/archive_run.py` relative
to its advertised installed base. Never use checkout or hardcoded cache paths
in generated plans. The following placeholders are data, not executable examples:

```sh
python "<installed-skill-base>/scripts/archive_run.py" \
  --project "<absolute-worktree-root>" --prd "tasks/prd-search.md" --dry-run
python "<installed-skill-base>/scripts/archive_run.py" \
  --project "<absolute-worktree-root>" --prd "tasks/prd-search.md"
```

`--dry-run` performs validation and returns JSON without filesystem writes.
When scoped archival authority already exists, invoke the normal command
automatically after completion; preview is optional, not a new approval gate.
`--run-id` disambiguates repeat calls when several archived runs used the same
now-absent PRD path. Exit 0 means preview, archived, or already_archived as stated
in the JSON `status`; exit 2 means blocked. Never interpret preview as archival.

## Result and failure behavior

The helper creates a unique UTC timestamped directory with microseconds:

```text
archive/YYYY-MM-DDTHHMMSSffffffZ-feature/
  prd-search.md
  PLAN.md                   # Or plan.json
  progress.md
  memory.json               # If present
  _archive.json             # Source mapping, hashes, commits, evidence, provenance
```

All artifacts are peers, including PRDs originally under tasks/ and custom plan
paths. The receipt retains each original path. No tasks/ or docs/ subdirectory is
created. The helper preserves file contents byte-for-byte; its receipt supplies
the deterministic closeout summary without rewriting or appending invented
narrative to the journal. The receipt records actual current HEAD/branch and
the Git commits carrying the story records. Historical branch metadata remains
in the archived task source unchanged.

The helper takes an exclusive archive lock at the per-worktree Git metadata path
returned by `git rev-parse --git-path archive-run.lock`. The persistent lock is
outside the tracked worktree; never reset/delete it. Linked worktrees have
independent locks. The helper copies into a fresh project-local
`.pending-<run_id>` directory, verifies bytes, publishes to a reserved fresh final
directory, rechecks all sources, and removes only the declared unchanged copies.
It preserves unrelated files, empty source directories, existing archives, and
all Ralph controls. It never stages, commits, pushes, resets runner state, or
creates a replacement plan/journal/memory. New execution starts with fresh memory.
Bounds: 2 MiB per input, 32 PRDs, 1,000 stories/history commits/archive entries.
Unsafe paths, symlinks, nonregular files, collisions, invalid metadata/memory,
missing or failed evidence, and changed/uncommitted artifacts are refused.

On failure, preserve sources and any partial archive; report JSON and inspect
the exact partial state. Never retry cleanup, overwrite an archive, or delete
pending directories automatically. A completed repeat invocation verifies the
receipt and archived bytes and returns already_archived without writes. Active
copies or incomplete receipts block that shortcut and need scoped reconciliation.
The helper serializes archive writers; execution must already have stopped.

Archival may run on any branch, including main/master or detached HEAD, after
delivery. It verifies reachable commits, including a squash commit containing the
actual records and completed plan. Missing retained Git evidence blocks rather
than falling back to a merge claim. Do not create/switch branches for archival;
execution still requires its exact prepared branch.

After successful archival, make the separately authorized closeout commit only
on an allowed working branch. Stage the returned source removals and destination
files explicitly, excluding runner controls. The metadata lock requires no staging
or ignore rule. Use the repository's commit convention, for example
`chore(workflow): archive completed search`.
If no commit authority exists, report the uncommitted archive. Failure to commit
does not undo the verified archive or authorize another story/cleanup attempt.
Shipping remains an explicit separate action; never push implicitly.

## Copy-only plan preservation fallback

Use the installed `archive_run.py --project "<absolute-worktree-root>"
--preserve-plan "<exact-project-relative-plan-path>"` for bounded plans without a
manifest or legacy plans whose verified archival inputs are unavailable. Add
`--include-prd "<exact-associated-PRD-path>"` for each inspected run-owned PRD;
never glob. `--dry-run` is read-only. Stop writers first; keep Ralph stopped until
its supervisor has validated completion and exited. Honor pending runner controls.

The helper copies the plan, available root progress.md/memory.json and explicitly
selected PRDs into a fresh `archive/<UTC-timestamp>-plan-preservation/`. It verifies
all copied and active bytes and writes `_preservation.json` last, with source
mapping, SHA-256 hashes, observed HEAD, `delivery_verified: false` and
`active_sources_removed: false`. It accepts uncommitted/legacy bytes solely to
prevent loss; it never fabricates manifests, passing checks, review or commits.
This receipt is distinct from `_archive.json` and cannot satisfy verified-run
archival or prove an unfinished plan complete. Symlinks, unsafe paths, flat-name
collisions, active runners and changed sources are refused. A partial directory
without its verified receipt is not a successful archive; preserve it and report
the failure rather than retrying automatically.

At goal completion use the applicable existing grant for this copy-only archival;
request only genuinely missing scope. Before replacing a completed plan, verify
the receipt and every preserved file/hash, then compare all current source bytes
with the receipt. If they differ, stop and reconcile instead of overwriting.
The new-plan request may cover replacement of that exact completed plan; narrower
confirmation rules still apply. Do not reset or remove prior progress/memory/PRDs
through this mode. Their active copies remain preserved, and their retirement
needs scoped reconciliation before starting a new run. If archival or replacement
is blocked, leave the previous plan intact and report the exact paths and reason.
A closeout commit remains separately authorized. No implicit push or installation.
