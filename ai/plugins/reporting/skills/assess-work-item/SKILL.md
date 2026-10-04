---
name: assess-work-item
description: Assess scope, effort, dependencies and risks from GitHub issues or Projects, Jira items, or supplied evidence.
---

# Assess Work Item

Read [requirements](references/requirements.md) before selecting external tools or
running helpers. Dependency setup is separately authorized.

Read [assessment contract](references/assessment.md). Identify the work item
from its URL, identifier and platform, or supplied context. Load the
[Jira adapter](references/jira.md) only for Jira. Confirm the target, requirements,
related work, and relevant evidence before estimating complexity or impact.
For GitHub issues or Projects, read the [GitHub adapter](references/github.md).
For a project, identify the bounded item/milestone/filter scope; report a project
synthesis and assess selected items individually when requested. Do not treat
one project status field as evidence that implementation passed checks/review.
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
