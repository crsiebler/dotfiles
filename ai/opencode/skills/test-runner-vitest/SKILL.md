---
name: test-runner-vitest
description: Executes tests, analyzes coverage, and debugs test failures in JavaScript and TypeScript repositories using Vitest
---

## What I do

- Run the Vitest test suite (all or individual files)
- Generate and analyze code coverage reports
- Help debug failing tests and explain error outputs
- Advise on common test/data setup patterns for JavaScript and TypeScript
- Assess code quality using coverage and test output

## When to use me

Use this when you need to execute tests, check coverage, or troubleshoot test failures in a JavaScript/TypeScript project using Vitest. This includes running all tests, single test files, or debugging specific test issues.

## Procedure

1. Read the repository root `AGENTS.md` and package scripts before selecting a command
2. Ensure the correct runtime version is active if required by the project
3. Run all tests through the configured repository script
4. Run tests with coverage through the configured script or `vitest run --coverage`
5. Run a specific test file with `vitest run path/to/file.test.ts`
6. Debug failures by reviewing Vitest error messages and stack traces
7. Fix code or tests based on issues identified by Vitest outputs

## Related Guidelines

- Follow test naming and structure conventions in the project
- Use mocks, test doubles, and setup/teardown in Vitest when allowed by project guidance
- Ensure pre-commit checks pass before commits
- Prefer repository scripts over direct runner commands
