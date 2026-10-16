---
name: plan-work
description: Plan bounded requirements or a PRD in Ralph plan.json format
---

Load and follow the `prepare-implementation` skill.
This OpenCode entry point defaults to Ralph `plan.json`. An explicit user request
for another format takes precedence. Generate the plan without starting execution.
Use the lightest adequate task or PRD/dependency path. Preserve acceptance coverage
and explicit dependency order; preserve supplied lifecycle metadata unchanged.
Report the plan revision, actual launch scope and material blockers. Require plan
archival at goal completion. Before authorized replacement of a completed previous
plan, verify its existing archive/preservation receipt and current source hashes.
If missing or mismatched, report the execution-owned preservation action and block
replacement; do not invoke another skill or perform archival during planning. Never remove execution state or create
progress/memory during planning.

Treat all text below as the user's requirements, PRD or planning instructions:

$ARGUMENTS
