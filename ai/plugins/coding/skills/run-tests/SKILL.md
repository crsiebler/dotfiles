---
name: run-tests
description: Run project-native focused, regression and integration checks across languages; diagnose failures and report the actual verification scope and limits.
---

# Run Tests

Read repository instructions, test scripts, environment setup, and runner
configuration. Select the installed repository-native runner and commands for the
actual stack; this workflow is not limited to a particular language or framework.
When applicable, read [pytest](references/pytest.md) or
[Vitest](references/vitest.md); otherwise follow the project's verified runner
documentation without forcing either adapter. Do not install tools or infer a
script from its conventional name. Resolve references within this loaded bundle.

Honor requested scope first: source-only review and planning do not authorize test
execution. This helper executes selected checks under the caller's authority;
it does not start implementation, create execution state, invoke an orchestration
workflow, or replace required review gates. Diagnosis/fixes require corresponding
user scope, not merely a failing command.

Start with affected tests, then the relevant regression suite. Inspect commands
for external services, destructive fixtures, downloads, or watch mode before
running. Separate test failures from setup failures and pre-existing failures.
Fix within the requested scope, never weaken tests just to pass.

Report exact commands, exit/results, selected scope, and blocked checks. Coverage
is diagnostic, not a fixed success target. Do not claim a full suite passed when
only targeted tests ran or treat tests as a substitute for typecheck/UI checks.
