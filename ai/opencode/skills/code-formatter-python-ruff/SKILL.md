---
name: code-formatter-python-ruff
description: Formats Python code with Ruff, applies lint fixes, and runs pre-commit hooks for quality checks
---

## What I do

- Format Python code using Ruff (`ruff format`)
- Lint and auto-fix issues using Ruff (`ruff check --fix`)
- Run pre-commit hooks to enforce formatting and lint checks on staged files
- Validate code style and formatting compliance

## When to use me

Use this skill for formatting and linting before every commit, after large code changes, or when preparing a PR/build in Python repositories that use Ruff.

## Procedure

1. Activate the repository's environment if required
2. Format code: `ruff format .`
3. Lint and apply safe fixes: `ruff check . --fix`
4. Apply unsafe fixes only with explicit approval: `ruff check . --fix --unsafe-fixes`
5. Run pre-commit hooks if configured: `pre-commit run --all-files`
6. Fix any issues reported by Ruff or pre-commit

## Related Guidelines

- Follow the repository root `AGENTS.md` code style guidelines
- Ensure all code passes Ruff and pre-commit checks before commit or PR
- `pyproject.toml` or `.ruff.toml` configuration is authoritative
- Mandatory pre-commit/CI checks must succeed for quality
