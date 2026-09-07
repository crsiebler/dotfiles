# Initial work-item assessment

Identify the work item and source platform. Confirm existence and access through
the connected integration before posting. Identifier shape alone does not prove
existence or select a site. Supplied context is sufficient for a provisional
draft; ask if ambiguity materially changes the assessment or posting target.

Read summary, description, acceptance criteria, links, relevant comments, status,
and dependencies. For software work, inspect relevant implementation, callers,
integration contracts, tests, and related PR/commit evidence. For other work,
use the applicable documents, processes, and constraints. Evaluate
plausible implementation approaches and compatibility constraints without
starting implementation. Retrieve only material context, not an exhaustive
codebase inventory.

Use exactly these labels, one `Field: Content` line each, with no Markdown
decoration or bullets in the comment:

```text
Risk & Impact Analysis: <technical and business/user implications>
Dependencies: <specific dependencies and required next steps>
Potentially Impacted Areas: <systems, modules, interfaces, or user flows>
Effort Estimate: <estimated effort or range, assumptions, and uncertainty>
Known Risks: <evidenced risks, likely impact, and supported mitigation>
Unknowns / Assumptions: <open questions, explicit assumptions, exclusions>
```

## Content checks

- Risk/impact covers both technical effects and relevant user/delivery effects;
  do not add irrelevant security, budget, or ROI keywords merely to fill a field.
- Dependencies identify actual tickets, PRs, APIs, environments, or team actions.
  Mention owners only when known; do not invent contact information.
- Impacted areas name concrete modules, services, or flows backed by inspection.
- Effort uses evidence-backed engineering time or the team's estimation units;
  state exclusions and uncertainty. Do not invent a delivery date, assume team
  capacity, or provide false precision. If not estimable, name the missing input.
- Known risks distinguish fact from possibility; assess severity/probability
  only when supportable and propose a relevant mitigation or validation step.
- Unknowns identify missing requirements, data characteristics, integration
  behavior, or scope boundaries rather than generic caveats.
- Check fields do not contradict each other. Dependencies should match affected
  areas; summary risks should agree with detailed risks and stated assumptions.

No minimum character counts or keyword scoring. “None identified from available
evidence” or a specific missing-source statement is better than fabricated detail.
If a source fails, explain what cannot be established and provide a provisional
draft using supplied context. Do not post without a verified issue target.

Before posting, validate exact fields and scrub sensitive information. Preview
the readable comment and exact active tool payload, then require explicit
approval. Re-preview any change. Verify the write result and avoid duplicate
comments after ambiguous timeouts. Do not perform unrelated ticket mutations.
