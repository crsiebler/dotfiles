---
name: archive-run
description: Preserve a completed plan or archive a verified delivered run using the bundled deterministic Python helper. Use for explicit authorized run closeout or preservation; not planning, story execution, review, team dispatch or runner recovery.
---

# Archive Run

Read [requirements](references/requirements.md) and the complete
[archival API contract](references/completed-run-archive.md). Resolve
scripts/archive_run.py relative to this advertised installed bundle. Its CLI owns
selection, integrity checks, copy/receipt verification and authorized active-copy
removal. Do not reproduce those operations with model-written shell commands.

Use --dry-run for requested read-only validation. Carry actual archival authority
forward; request only genuinely missing exact-path scope. Normal operation is
not authorized by loading this capability. Quiesce writers and honor runner
controls; report actual JSON outcome and preserve sources/partial outputs on
failure. Never retry partial cleanup automatically or fabricate delivery records.

This package shares executable functionality only. Each invoking workflow owns
its lifecycle, review, progress and completion rules. No executor, reviewer,
model selection or team workflow is started here. Archival metadata enrollment
belongs to authorized execution before its first checkpoint, never planning.
