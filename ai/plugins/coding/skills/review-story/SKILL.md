---
name: review-story
description: Review one staged story using a workflow-supplied candidate, acceptance criteria, verification scope and bounded review session. Use for a requested story delivery gate with a generic reviewer; not ordinary PR review or implementation.
---

# Review Story

Read [requirements](references/requirements.md) and the complete
[review contract](references/contract.md). This skill owns the staged-story schema
and procedure; reviewer supplies independent review judgment. It works in a
normal session and does not require a goal controller or a dedicated story agent.

The invoking workflow loads this skill through actual discovery and embeds the
complete contract plus its concrete review packet in each generic reviewer call.
Do not guess sibling/cache paths or rely on inherited context. The packet supplies
candidate identity, scope, verification mode/commands, resource and time limits,
pass type, story/attempt identity, and previous findings for a targeted pass.
Missing required inputs block review rather than expanding the reviewer's authority.

Review and scoped verification belong to the same reviewer. Inspection-only
requests stay inspection-only. Never edit the candidate or repair findings.
Return exactly the contract's JSON; record actual checks and their provenance.
One initial and at most one targeted pass share the same actual reviewer session
per story attempt. The workflow owns dispatch, remediation, persistence, final
blocker reconciliation, commits and delivery; this skill creates no execution state
and never dispatches agents itself. Use the same contract for budget-authorized
self-review, without claiming independent review.
