---
name: assess-work-item
description: Assesses work-item scope, effort, dependencies, risks, and unknowns.
---

# Assess Work Item

Read [assessment contract](references/assessment.md). Identify the work item
from its URL, identifier and platform, or supplied context. Load the
[Jira adapter](references/jira.md) only for Jira. Confirm the target, requirements,
related work, and relevant evidence before estimating complexity or impact.
For other platforms, draft from supplied evidence unless a verified integration
is available; do not assume Jira identifiers or invent platform-specific tools.
Separate evidence, reported constraints, assumptions, and unanswered questions.

Produce the six plain-text fields in the reference. Use specific technical
and delivery implications, not keyword quotas or padded minimum lengths. Include
actionable dependencies and mitigations only where supported.

Default to a draft. Before external posting, preview the full comment, verified
site/issue, and actual exposed tool payload; require explicit approval. Verify
the resulting comment and report its identity/link. Do not implement the item,
transition its status, or change other external state during assessment.
