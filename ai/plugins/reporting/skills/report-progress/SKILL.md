---
name: report-progress
description: Drafts evidence-backed daily work-item updates with remaining work and ETA.
---

# Report Progress

Read [requirements](references/requirements.md) before selecting external tools or
running helpers. Dependency setup is separately authorized.

Read [daily update contract](references/daily-update.md). Identify the work item
from its URL, identifier and platform, or supplied context. Load the
[Jira adapter](references/jira.md) only for Jira. Gather relevant work-item and,
for software work, Git/PR evidence before drafting. Other platforms may use
supplied evidence for a draft; do not invent an unsupported posting integration.
If a source is unavailable, label the gap. Do not post when the destination or
supporting context is uncertain.

Preserve exactly these labels and order: `Date:`, `What I completed:`,
`What’s next:`, `Blockers:`, `ETA:`. Separate uncommitted, committed, merged,
tested, and deployed work. Estimate remaining engineering effort only when
supportable; include `Excludes QA testing.` without inventing an ETA.

Default to draft. Before an external post, show the issue/site, full comment,
and exact exposed tool name and payload. Reuse existing authorization for the same
target and content when the user explicitly approved posting them; otherwise ask
for approval of the prepared result. Carry that grant through continuation.
A changed destination, body, or effect needs a new preview and approval; mechanical
encoding alone does not. Verify the returned comment identity and report its link
when available. Do not transition issues, change code, merge, or deploy.
