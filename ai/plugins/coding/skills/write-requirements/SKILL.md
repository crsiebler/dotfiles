---
name: write-requirements
description: Define scoped outcomes and verifiable acceptance for bounded tasks or larger PRDs.
---

# Write Requirements

Read [requirements](references/requirements.md) before selecting external tools or
running helpers. Dependency setup is separately authorized.

Use supplied task details first. Gather missing supplemental project information
and relevant external research through available authorized sources when necessary;
record source evidence and uncertainty without starting implementation.

Read [requirements formats](references/prd-format.md) for structure and examples.
Use a concise bounded-task brief for small, clear work; use the fuller PRD when
multiple outcomes, dependencies, unresolved decisions, or stakeholder coordination
need it, or the user requests one. Both preserve all requirements and acceptance
coverage. Establish
the problem, users, boundaries, dependencies, and observable acceptance criteria.
Ask only material unanswered questions; do not invent goals or fixed metrics.
Keep optional specialist hints as exact configured `@agent-name` values, not
mandatory delegation. Include typecheck, meaningful tests, and browser criteria
where applicable. Do not start implementation.

Keep requirements at the outcome level: problem, users, scope/exclusions,
observable acceptance, constraints/dependencies, assumptions and open questions.
Requirements do not create the execution story list, dependency matrix or select
worker models. Those are downstream planning/execution concerns. Do not create work-run blocks or runner settings
while authoring requirements. Preserve existing metadata unchanged on scoped
revisions; report conflicts for planning reconciliation. A saved PRD is optional
for a bounded task whose approved requirements can be carried directly into its
plan. Requirements grant no execution, commit, archival or external-write authority.

Return a draft unless saving was requested. Default proposed path:
`tasks/prd-[feature-name].md`. Check the target before saving. For replacement,
preview the exact archive destination and replacement, require explicit approval
to archive the existing PRD, and verify its contents are preserved before writing.
Never overwrite an archive; on refusal or failure leave the PRD unchanged and
return the draft. A new-PRD request alone is not replacement approval. Explicit
same-PRD revisions update only approved requirements in place. Report assumptions and
open questions rather than presenting them as approved requirements.

PRDs contain approved requirements and open questions, not implementation
checkpoints. Approved requirement changes update the PRD and are cross-referenced
from worktree-root `progress.md` once execution begins. Implementation
outcomes belong in that journal, not growing PRD narratives. Drafting neither
requires nor creates the journal and must not archive task sources, memory, or
execution journals as a side effect. See the reference's preservation guard.
