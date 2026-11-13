# OpenCode existing-data startup recovery

Current state: a later explicitly authorized cleanup removed all live sessions
and reclaimed the database space; see [follow-up cleanup](#follow-up-cleanup).
The recovery evidence below records the earlier history-preserving operation.

Verified November 13, 2026 against installed OpenCode v2.1.4. The earlier
Nemotron pilot's 180-second timeout was caused by native history migration,
not a requirement to use an empty data directory.

## Cause and recovery

The normal database, `~/.local/share/opencode/opencode.db`, was 138,489,708,544
bytes (128.98 GiB). It contained 4,373 V1 sessions, 92,410 messages, 561,935
parts and 3,213,962 obsolete event rows. V2 session tables were empty.

The exact v2.1.4 migration first clears the old event table in 1,000-row batches
inside one transaction, then commits a migration marker and converts sessions.
The existing service's stack sample showed SQLite deleting overflow pages.
Interrupting a standalone process during that transaction can roll back the
cleanup, forcing the next process to repeat it. Database size alone was not
evidence of corruption or a reason to reset history.

The already-running background service was allowed to finish. It advanced from
event cleanup through session conversion to `{"phase":"completed"}`. No manual
DELETE/DROP, migration-marker edits, database replacement, binary upgrade,
service restart or persistent configuration changes were performed.

The background service remained the same process throughout. Once migration
finished, this supported authenticated status request returned in 0.087 seconds:

```sh
opencode api GET /api/experimental/migration/v1
```

Result: `{"status":"completed"}`. This is a read-only status operation, not a
migration command. During heavy migration work it can itself be delayed; a
request timeout alone does not establish a failed migration. Avoid repeatedly
launching and terminating competing standalone servers over the same database.

## Normal Nemotron verification

The preserved TensorFold launcher started the model on port 8082. OpenCode then
used the existing background service, installed provider, normal data directory
and normal agent, without `--standalone` or alternate XDG storage directories.

For safety, a new local verification session had native session-level permissions
denying every action except reading the exact fixture. v2.1.4 appends these rules
after agent permissions and honors explicit denials before saved approvals.
The session completed one structured `read` call, received its tool result and
returned the correct fixture value in **3.54 seconds**. The session was retained.
The model server was stopped afterward; the background OpenCode service stayed up.

A temporary custom agent supplied through an environment config overlay was not
available in the shared service. That failed probe was retained. An unrestricted
default-agent retry was rejected by automatic approval review; it was not run.
The native restricted-session test supplied a safe supported alternative without
altering existing agent definitions, settings or integrations.

For ordinary use, start `bash scripts/serve-nemotron.sh` from this checkout and
select `tensorfold/nemotron-lightning` in OpenCode. Your configured default model,
Bonsai provider and permission settings remain unchanged.

## Preservation and backups

Before/after SHA-256 checksums of every column in every legacy session, message
and part row matched exactly: 4,373 sessions, 92,410 messages and 561,935 parts.
Every legacy session ID exists in V2. The installed OpenCode configuration's
SHA-256 also matched its baseline, preserving Bonsai and all existing settings.

The successful compact SQLite snapshot is:

```text
~/.local/share/opencode/backups/startup-compact-20261113T070309Z/opencode.db
```

It is 13,429,620,736 bytes (12.51 GiB), with owner-only directory/file permissions
and `PRAGMA quick_check` reporting `ok`. `VACUUM INTO` ran against a read-only
source connection: it creates a consistent separate snapshot and does not compact
or modify the live database. A disposable fixture established that behavior first.

The snapshot contains all legacy sessions, messages and parts. It captured
conversion at 4,190 V2 sessions, so a future restore would resume the remaining
native conversion; do not mark its migration complete by hand. It also contains
private application data: keep it outside Git and do not share its contents.

The first online-backup attempt repeatedly restarted as migration transactions
committed. It stopped at its 240-second budget. Its retained output at
`backups/startup-20261113T065904Z/opencode.db` is zero bytes and is **not a backup**.
No backup files were removed.

Local diagnostic evidence lives in
`tests/artifacts/opencode-startup-2026-11-12/`. It includes metadata, content
checksums (without session text), the restricted tool-call transcript, timings,
backup validation and failed attempts. Do not commit generated databases or caches.

## Automated cleanup and disk space

No documented automatic age-based session deletion policy was found for installed
v2.1.4. Its conversation compaction controls model context, while earlier
messages remain stored. `opencode session delete SESSION_ID` explicitly deletes
a session and its children; no sessions were deleted during this recovery.

The roughly 120 GiB released by event cleanup remains as free pages inside the
original database file. SQLite can reuse those pages, but the file does not
automatically shrink. A database compaction can reclaim filesystem space while
retaining logical history; deleting sessions is unnecessary for this particular
space recovery. The live database was not compacted or replaced. That separate
maintenance operation needs an identified quiet window, a validated backup and
authorization for any service stop/restart or file replacement it requires.

Sources: [v2.1.4 migration implementation](https://github.com/anomalyco/opencode/blob/v2.1.4/packages/core/src/database/v1-migration.bun.ts),
[v2.1.4 permission precedence](https://github.com/anomalyco/opencode/blob/v2.1.4/packages/core/src/permission.ts),
[V2 conversation compaction](https://github.com/anomalyco/opencode/blob/v2.1.4/services/www/src/docs/content/compaction.mdx),
[SQLite VACUUM INTO](https://www.sqlite.org/lang_vacuum.html).


## Follow-up cleanup

On November 13, 2026, the user explicitly authorized deleting all OpenCode
sessions and reclaiming space, including a brief service stop/restart, while
preserving settings, credentials, providers, models and the existing backup.
No sessions were active.

The native service was stopped and the database checked for open users. A
transaction cleared both legacy/current sessions and their dependent history
records across 14 tables. Every other database table was fingerprinted and
verified unchanged before commit and after compaction. A disposable fixture
and independent review preceded execution.

The live database shrank from **138,489,708,544 bytes (128.98 GiB)** to
**7,225,344 bytes (6.89 MiB)**, reclaiming **138,482,483,200 bytes**. Deletion
took 20.01 seconds and compaction 1.12 seconds. SQLite integrity and foreign-key
checks passed.

After service restart, the native session API returned zero sessions, all 14
history tables remained empty, both Bonsai and TensorFold Nemotron appeared in
the model list, and the installed configuration hash matched its baseline.
Credentials, saved permissions, accounts, migrations, catalog data, worktrees
and project directories retained their fingerprints. Native CLI verification
refreshed a project's `time_active` timestamp; all other project fields matched
the validated backup. The initial assertion detecting this expected activity
change and its diagnostic were retained rather than hidden.

The validated **12.51 GiB backup still contains the old history** and was kept
as requested. No model files, external snapshots, logs or backup files were
deleted. Diagnostic evidence is in
`tests/artifacts/opencode-cleanup-2026-11-13/`.
