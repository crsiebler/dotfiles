---
name: analyze-review-feedback
description: Evaluates pull-request feedback against code and prioritizes actionable changes.
---

# Analyze Review Feedback

Read [GitHub feedback](references/github.md). Resolve the PR and repository from
explicit input or verified repository metadata; ask when ambiguous. Retrieve
feedback and thread state with pagination, then inspect the affected code and
requirements before accepting suggestions. Supplied feedback can be analyzed
offline, with source coverage stated.

For each item, retain its URL/ID and assess technical correctness, compatibility,
actual usage, architectural fit, impact, and uncertainty. Separate bugs,
improvements, style, documentation, and architecture. Group by file/theme/priority
as requested and deduplicate shared causes without losing comment references.

Return recommended action, supporting evidence, affected area, and relative
effort when supportable. Flag unclear, unnecessary, conflicting, or breaking
requests for clarification rather than agreeing reflexively. This is read-only:
do not implement, reply, resolve threads, or submit a review automatically.
