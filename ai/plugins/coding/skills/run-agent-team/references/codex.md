# Codex session entry

Invoke the discovered run-agent-team skill in the current main session with the
approved plan and actual execution scope. A normal request is sufficient; /goal
is optional. The command alone does not select this skill or grant authority;
a user-supplied objective to implement an approved plan authorizes its initial
and subsequent scoped local commits without a separate commit confirmation.

Example after selecting the skill:

> Execute the approved PLAN.md using run-agent-team. This main session owns
> orchestration. Target up to four concurrent implementation workers within actual
> runtime/resource capacity, reserving review capacity for reviewer with the
> complete review-story contract. Preserve pending work and report missing
> worktree authority or capability.

For unattended execution, use the approved readiness record and
[autonomous execution scope](story-execution.md#autonomous-execution-scope).
Complete scoped automated checks and bounded agent review without adding manual
QA, human confirmation of test results, or release gates. Required human or
runtime approval conflicts must be resolved before affected implementation, not
deferred to final delivery. This does not require a separate background runner.

This example is not an execution grant. Actual scope identifies the integration
branch/root and task-worktree lifecycle. When the user actually requests this
plan implementation, its scoped initial, story and local closeout commits are
authorized; narrower no-commit instructions override. Archival/removal still
needs its applicable scope. No push, post,
installation or deployment follows implicitly. The main session owns dispatch,
integration and canonical state. Use actual native controls; do not create a
controller or emulate a goal lifecycle to continue an ordinary request.
