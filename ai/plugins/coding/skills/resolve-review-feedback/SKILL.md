---
name: resolve-review-feedback
description: Verifies addressed review feedback and prepares approved thread resolutions.
---

# Resolve Review Feedback

Read [resolution protocol](references/github.md) before any operation. Resolve
the PR, current head, comments, and thread IDs. Compare each concern with actual
code and tests at the PR head; file changes or commit keywords alone are not
proof of a fix. Leave uncertain or unpushed fixes unresolved.

Default to dry-run. Show each proposed reply, evidence/commit, target comment and
thread, and the exact write commands/payloads. Require explicit approval after
the preview for **all** replies, resolutions, edits, deletions, and reposts.
`auto_resolve` or a posting request never bypasses confirmation. Changed targets
or content require a new preview.

After approved writes, verify returned reply IDs and exact `in_reply_to_id`,
then verify thread resolution. Stop the affected workflow on uncertainty; do
not duplicate writes after timeouts. Report posted/resolved/skipped/failed items
from observed results, not intended actions. Never modify code or push as an
incidental part of resolving feedback.
