---
name: refactor-code
description: Restructures code while preserving behavior and architectural boundaries.
---

# Refactor Code

Read the affected implementation, callers, tests, and repository conventions.
Identify the concrete maintenance problem and the behavior that must remain
unchanged. Prefer existing patterns over imposing Strategy, CQRS, or layers.

Establish a passing baseline. Add characterization tests before edits where
important behavior lacks coverage; use `develop-with-tests` for intended
behavior changes. Refactor in small steps, retaining public contracts and
dependency boundaries. Use explicit dependencies where useful, not a mandatory
rewrite of object creation. Do not assume a particular domain directory.

Run focused tests after each meaningful change, then the relevant regression
suite, formatting, lint, and typecheck. Inspect the final diff for unintended
behavior or scope changes. Report validation and compatibility risks. Do not
commit or perform external operations without authorization.
