# Coding runtime and execution ownership

## Runtime and model selection

- Select one execution workflow per story attempt: this native team workflow
  or the separate serial Ralph runner. Never run both against the same story.
- Reusable roles define expertise, tools, constraints and outputs. Keep model
  and reasoning effort choices in explicit runtime profiles or launch parameters.
- Ordinary work inherits the selected parent/session settings. Inheritance is
  not automatic task-aware routing. Do not silently replace it with global
  subagent defaults or role pins.
- Use an efficient supported profile for narrow tasks only with relevant quality
  evidence. Consider an explicit stronger profile for material ambiguity,
  architecture, difficult debugging, security analysis or substantive failure.
  Honor user choices, runtime support and authorized cost limits; escalation does
  not enlarge a spending grant or waive tools, sandbox or review restrictions.
- Keep a stable selection within an attempt unless a material reason changes it.
  At a material handoff record task class, runtime, requested model/effort,
  selection source/reason, known quota/cost limits and outcome. Mark unobserved
  effective settings or usage unknown; do not invent actual routing or costs.
- Use deterministic tools for file operations and validation. Add no model call
  merely to package a result or evaluate an already deterministic gate.

## Explicit team selection

An authorized run-agent-team invocation uses the current main session. Prefer
`gpt-6.1-sol` for coordination, `gpt-6-luna` for implementation and `gpt-6-astra`
for review, conflict analysis, architecture and cross-domain analysis when the
runtime supports selection within the existing grant. These preferences are not
mandatory model requirements. Use one capability/pin preflight and the
single-dispatcher contract, with this precedence:

1. Honor explicit user model/effort requirements and cost limits. If a required
   selection is unavailable or cannot be verified to the requested standard,
   stop the affected path and report the exact constraint. Do not silently relax
   it. A skill preference or illustrative prompt is not a user requirement.
2. Preserve installed role pins and runtime restrictions. Use the exact required
   native role with its supported model, even when it differs from the preference.
   Never override a fixed pin, change roles or install settings to obtain a model.
3. Where supported and authorized, request the preferred worker/advisor model.
   Otherwise omit overrides and use native inheritance or runtime defaults.
   Explicit model-selection controls are optional unless a user constraint needs
   them. Do not guess model identifiers or unsupported tool arguments.
4. Record requested and observed models, selection source, fallback reason and
   unknown telemetry once in the existing checkpoint. Unknown coordinator model
   telemetry or unavailable preferred models alone does not block execution or
   require renewed approval. Do not repeatedly probe an unchanged model gap.

An available Luna-pinned story-reviewer satisfies the model policy when the user
has not explicitly required another model. It must still be the exact native
story-reviewer and support the required protocol and same-session continuation.
No preference fallback changes review quality criteria, tool restrictions or
consumed passes. This policy does not establish model quality or effective routing.

## Native execution ownership

- Ralph executes stories serially. This team workflow may admit concurrent
  dependency-ready implementation workers when the active harness exposes the
  required native controls. Preserve requirements, acceptance and bounded review/delivery gates.
- Give each implementation worker an explicit absolute task worktree, exact branch,
  approved committed base and owned paths. Inspect actual native cwd/isolation
  controls; verify the assigned root and use assigned paths for files, Git and
  checks. Establish a clean committed baseline;
  never copy or commit user dirty work to prepare it. Task branch/worktree setup
  needs a scoped lifecycle grant and never switches the user's checkout.
- One lead owns integration branch/index, canonical task markers, progress and
  memory. Coordinate shared build/output ownership and host resources using the
  project's mechanism. Freeze the reviewed candidate and conflicting resources;
  unrelated workers in separate worktrees may continue. Hooks are only guardrails.
- Reconcile narrower project instructions before concurrent execution. Required
  native roles/tools and explicit user model constraints must be satisfied. This
  policy creates no runtime capability, installed activation or permission bypass.

The main thread is the dispatcher and retains conflict-resolution writes. Do not
silently switch the main thread. No custom coordinator or nested delegation is
needed.
The exact native story-reviewer remains mandatory at the budget-selected native
gate; selecting Astra never substitutes a generic reviewer or adds an extra pass.
Respect existing advisor/review/remediation limits. On resumption, reconcile the
existing candidate, checks, reviewer session and consumed passes. A resolved
model-policy blocker does not invalidate an otherwise valid passing review or
authorize another review. Complete pending finalization only after verifying its
candidate/evidence and existing commit authority; preserve unrelated blockers.
