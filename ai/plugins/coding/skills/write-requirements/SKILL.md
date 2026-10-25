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

## Acceptance for autonomous implementation

Default to implemented outcomes with agent-executable, noninteractive verification
and required independent agent review. Do not add manual QA, human confirmation
of test results, stakeholder sign-off, or routine deployment verification to the
PRD. Include deployment or deployment checks only when explicitly requested and
automatable within the intended authorized environment.

Keep behavioral acceptance observable and automation-compatible. Planning owns
the exact commands, fixtures, automation dependencies and readiness evidence;
requirements drafting neither runs checks nor requires tests to exist already.
New test automation may be scoped implementation work. Automated tests do not
replace the product outcome they verify, and a green check is not evidence of an
unexecuted deployment or manual acceptance.

If supplied requirements explicitly demand human acceptance or another
non-automatable operation, preserve the source requirement and surface the
conflict for upfront scope or method resolution. Do not silently remove it,
approve it yourself, or add it as a manual execution/closeout checkbox. Optional
human follow-up stays outside implementation completion. Record unresolved
conflicts as open questions for planning; do not label them approved autonomous
acceptance or create a second readiness tracker. Reuse existing user resolutions.

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
Carry existing exact-path archival/replacement approval forward when unchanged;
do not request it again merely because another skill or turn handles the save.
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
