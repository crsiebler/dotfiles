---
name: write-requirements
description: Writes scoped PRDs with verifiable stories and acceptance criteria.
---

# Write Requirements

Read [requirements](references/requirements.md) before selecting external tools or
running helpers. Dependency setup is separately authorized.

Read [PRD format](references/prd-format.md) for structure and examples. Establish
the problem, users, boundaries, dependencies, and observable acceptance criteria.
Ask only material unanswered questions; do not invent goals or fixed metrics.
Keep optional specialist hints as exact configured `@agent-name` values, not
mandatory delegation. Include typecheck, meaningful tests, and browser criteria
where applicable. Do not start implementation.

Keep requirements at the outcome level; prepare-implementation owns the detailed
phase plan and execution-story breakdown. When saving a new PRD, include the
reference's machine-readable work-run metadata, a stable run ID and its explicit
PRD inventory. Adapter/task_source may be null until implementation planning binds
them. PRDs join the flat completed-run archive; metadata grants no execution,
archival/removal, commit or external-write authority.

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
