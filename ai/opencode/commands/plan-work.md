---
name: plan-work
description: Convert a PRD to Ralph plan.json format
---

Load and follow the `prepare-implementation` skill.
This OpenCode entry point defaults to Ralph `plan.json`. An explicit user request
for another format takes precedence. Generate the plan without starting execution.
Explain phases and ordered execution stories, bind the associated PRDs' work-run
metadata, and report the exact primary PRD path and missing execution/archival/
closeout authority. Do not archive or create progress/memory during planning.

Treat all text below as the user's PRD source or conversion instructions:

$ARGUMENTS
