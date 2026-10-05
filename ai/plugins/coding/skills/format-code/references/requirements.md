# Requirements

## Required and conditional dependencies

Use the target project's installed formatter/linter and configuration. This
instruction-only skill has no universal dependency. Python references cover Ruff
and configured pre-commit hooks; JavaScript/TypeScript references cover configured
Prettier and ESLint. Husky/lint-staged apply only when already used by the project.
Do not install all of these merely to format a file.

## Installation and checks

Restore declared versions through the project's lockfile and approved package
manager. For an existing npm lockfile, `npm ci` restores declared tools but
replaces `node_modules` and may run lifecycle scripts; review those effects.
Do not use bare `npx` as a missing-tool fallback because it can download code.

For an explicitly approved Python tooling environment, a fresh project-local
environment can install selected versions:

```sh
python3.11 -m venv .venv-format
./.venv-format/bin/python -m pip install 'ruff==<approved-version>'
./.venv-format/bin/ruff --version
```

Add `pre-commit==<approved-version>` only if the configured hooks require it;
`pre-commit install` modifies Git hooks and is a separate action. Replace
placeholders, preserve existing environments, and do not alter project dependency
manifests without authorization. JavaScript tool additions should follow the
project's package manager and approved manifest changes.

See official [Ruff installation](https://docs.astral.sh/ruff/installation/),
[pre-commit setup](https://pre-commit.com/#install),
[Prettier installation](https://prettier.io/docs/install), and
[ESLint setup](https://eslint.org/docs/latest/use/getting-started).
Version/help checks verify availability; they do not prove formatting passes.
