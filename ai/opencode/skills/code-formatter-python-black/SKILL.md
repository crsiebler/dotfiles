---
name: code-formatter-python-black
description: Formats Python code with Black and isort and runs pre-commit hooks for quality checks
---

## What I do

- Format Python code with Black
- Sort imports with isort
- Run pre-commit hooks for quality checks
- Validate code style compliance

## When to use me

Use this skill when formatting code, checking formatting, or running linting checks in Python repositories that use Black and isort. This includes before commits, after major changes, or when setting up the development environment.

## Procedure

1. Activate the repository's environment if required
2. Read the repository configuration to determine the source and test paths
3. Format code: `black <paths>`
4. Sort imports: `isort <paths>`
5. Run pre-commit checks if configured: `pre-commit run --all-files`
6. Fix any linting issues identified

## Related Guidelines

- Follow code style guidelines from the repository root `AGENTS.md`
- Use the Black line length configured by the repository
- Apply isort with the repository's configured profile
- Ensure mandatory pre-commit checks pass
