---
name: develop-with-tests
description: Develops behavior changes with failing regression tests and focused validation.
---

# Develop With Tests

Classify the change before choosing validation:

| Change | Approach |
| --- | --- |
| New behavior or bug fix | Write a failing behavior/regression test first. |
| Behavior-preserving refactor | Run existing tests; add missing characterization tests first. |
| Static docs, metadata, configuration, dependencies | Use relevant schema, lint, typecheck, or build validation. |
| Configuration generators or runtime selection | Test generated meaning and runtime behavior. |
| External integrations | Use a realistic fake or safe integration test at the boundary. |

For behavior: write a focused assertion, run it, and confirm failure is due to
the missing behavior rather than broken setup. Implement the smallest fix,
rerun to green, then refactor and run relevant regressions. Cover important
errors and edge cases without chasing a fixed coverage percentage.

Read [testing anti-patterns](references/testing-anti-patterns.md) when writing or
reviewing tests, choosing test doubles, or adding test utilities.
Prefer real behavior and explicit dependencies; follow project testing patterns.
Do not delete existing work to reenact test-first. If work already exists,
disclose that order and demonstrate the regression test detects the defect
without discarding user changes. If meaningful execution is blocked, state why
and what remains unverified; do not claim a red/green run that did not happen.

Report change type, red/green commands and results, regression checks, and any
reason for using non-test validation. Tests run by `run-tests` are not proof of
requirements that those tests do not exercise.
