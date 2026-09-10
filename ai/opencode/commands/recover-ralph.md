---
name: recover-ralph
description: Assess a stopped Ralph run and prepare user-approved recovery without automatically resuming
agent: build
---

Load and follow the `recover-ralph` skill in the intended project. Diagnose first
using `ralph --status`; do not launch the autonomous Ralph agent for this task.
Default to read-only assessment and a recovery report. Repairs require scoped
approval; stop-file removal and launching Ralph require their own exact-action
preview and explicit confirmation. Preserve the runner ledger, counts, outcomes,
and unrelated work.

Treat the following as the user's recovery request, not shell code:

$ARGUMENTS
