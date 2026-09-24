---
name: develop-code
description: Implement features, diagnose and fix bugs, or refactor code while preserving contracts and verifying behavior. Use for development work, including diagnosis-only requests; not standalone planning, conceptual explanations, or read-only code review.
---

# Develop Code

Establish the requested outcome and authority before edits or commands. Read
applicable project instructions, relevant code, callers and tests, and existing
changes. Preserve user work. Identify required behavior, compatibility, errors,
side effects and material unknowns; do not silently drop requirements to simplify
the solution. Use supplied context first and inspect only affected contracts.

Select the action and read its bundled reference relative to this loaded skill:

| Intent | Method |
| --- | --- |
| Add or intentionally change behavior | [Feature](references/actions/feature.md) |
| Investigate or repair a defect | [Bugfix](references/actions/bugfix.md) |
| Improve structure without changing behavior | [Refactor](references/actions/refactor.md) |

For mixed work, name intentional behavior changes separately from preserved
contracts and apply the corresponding methods. Diagnosis-only requests permit
only the requested investigation; source-only requests prohibit reproduction
execution. Planning-only requests remain planning: do not implement, run checks,
or create execution state. Standalone explanations and assessment belong to their
requested workflows; this skill is not a prerequisite for independent review.

Read [testing strategy](references/testing-strategy.md) to select evidence by
change type. Read [testing anti-patterns](references/testing-anti-patterns.md)
when writing tests, choosing doubles, or adding test utilities. Load only relevant
detail, not every action. Missing required references block the affected method;
report the exact resource rather than claiming it was applied.

Reuse suitable project patterns and make the smallest cohesive change that meets
all requirements. Preserve validation, security, accessibility and data-loss
prevention appropriate to the behavior. Do not add layers, dependencies, or
patterns merely to satisfy a checklist or reduce line count. Ask for material
missing facts or new authority; make routine decisions within the approved scope.

For material interface, responsibility, dependency, persistence, concurrency,
trust-boundary or performance decisions, read
[architecture decisions](references/architecture-decisions.md). Routine local
changes need neither this deeper analysis nor a full ADR. Patterns remain tools
selected for actual constraints, not required outcomes.

Use project-native formatter, lint, typecheck and test commands. Applicable
advertised helpers such as `run-tests`, `format-code`, or `verify-interface` can
assist; resolve them through skill discovery, never sibling filesystem paths.
They do not replace this method or require loading another lifecycle. Disclose
unavailable helpers/checks and their effect on required verification.

Inspect the final diff for scope and compatibility. Report the actual change,
causal or equivalence evidence, commands/results, actual test order and remaining
limitations. A passing test establishes only the behavior it exercises.

This method grants no authority to create/switch branches, stage, commit, push,
post, install, deploy, migrate or perform other restricted operations. Preserve
the caller's execution and review gates. Do not start an execution controller,
create plan/journal/memory state, invoke orchestration, or substitute for a required
native reviewer. Delegation is never automatic and requires applicable authority.
