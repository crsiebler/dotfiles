---
name: test-runner-pytest
description: Executes tests, analyzes coverage, and debugs test failures in Python repositories using pytest
---

## What I do

- Run the pytest suite (all tests or targeted files/tests)
- Generate and analyze code coverage reports
- Help debug failing tests and explain error outputs
- Advise on common pytest fixtures and test setup patterns
- Assess code quality using coverage and test output

## When to use me

Use this when you need to execute tests, check coverage, or troubleshoot test failures in a Python project using pytest. This includes running all tests, single test files, specific test cases, or debugging targeted failures.

## Procedure

1. Read the repository root `AGENTS.md` and project configuration before selecting a command
2. Activate the repository's environment if required
3. Run all tests through the configured repository command or `pytest`
4. Run tests with coverage: `pytest --cov --cov-report=term-missing`
5. Generate an HTML coverage report when needed: `pytest --cov --cov-report=html`
6. Run a specific test file: `pytest path/to/test_file.py`
7. Run a specific test case: `pytest path/to/test_file.py::test_name`
8. Debug failures by reviewing pytest tracebacks, assertion diffs, and fixture setup
9. Fix code or tests based on issues identified by pytest outputs

## Related Guidelines

- Follow test naming and structure conventions in the project
- Use pytest fixtures, mocks, and setup/teardown patterns when allowed by project guidance
- Ensure lint and pre-commit checks pass before commits
- Prefer repository commands such as Make targets over direct runner commands
