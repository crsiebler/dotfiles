# Python formatting and lint

Read `pyproject.toml`, `.ruff.toml`/`ruff.toml`, configured task commands, and
pre-commit configuration. Use the existing virtual environment or project runner.
Do not create an environment or download packages without authorization.

When Ruff is configured and installed, command shapes for selected paths are:

```sh
ruff format --check path/to/module.py
ruff check path/to/module.py
ruff format path/to/module.py
ruff check --fix path/to/module.py
```

Use actual paths, not the placeholder. Safe fixes still require diff review.
`--unsafe-fixes` requires explicit approval and appropriate behavior tests.
Use `pre-commit run --files <paths>` for scoped configured hooks; use
`pre-commit run --all-files` only when full-repository validation is appropriate.
Hooks can mutate files or initialize environments: inspect configuration first
and stop if they require unauthorized downloads or external effects. Never skip
mandatory hooks. Follow the repository's formatter if it is not Ruff.
