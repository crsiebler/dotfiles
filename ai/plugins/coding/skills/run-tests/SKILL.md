---
name: run-tests
description: Runs focused and regression tests with pytest or Vitest and diagnoses failures.
---

# Run Tests

Read repository instructions, test scripts, environment setup, and runner
configuration. Use [pytest](references/pytest.md) or
[Vitest](references/vitest.md). Prefer installed repository commands; do not
install tools or infer a script from its conventional name.

Start with affected tests, then the relevant regression suite. Inspect commands
for external services, destructive fixtures, downloads, or watch mode before
running. Separate test failures from setup failures and pre-existing failures.
Fix within the requested scope, never weaken tests just to pass.

Report exact commands, exit/results, selected scope, and blocked checks. Coverage
is diagnostic, not a fixed success target. Do not claim a full suite passed when
only targeted tests ran or treat tests as a substitute for typecheck/UI checks.
