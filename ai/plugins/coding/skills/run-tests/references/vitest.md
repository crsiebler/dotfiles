# Vitest execution

Read package scripts, lockfile/runtime pins, Vitest configuration, setup files,
workspaces/projects, and environment selection. Prefer the configured test or
CI script. Verify argument forwarding before narrowing a script to one test.

With an installed local Vitest binary, command shapes are:

```sh
vitest run path/to/file.test.ts
vitest run path/to/file.test.ts -t 'specific behavior'
vitest run
vitest run --coverage
```

Use non-watch execution for bounded validation. Coverage requires the project's
configured provider; do not download it implicitly. Inspect stack traces,
assertion diffs, unhandled rejections, timers, and setup/teardown. Ensure doubles
are restored and async work is awaited rather than masking flakes with retries.

In Bun-managed projects, `bun run test` and `bun run test:ci` are valid only when
those scripts exist and invoke Vitest as intended. `bun test` is a different
runner, not a shortcut. Run typechecking separately via the repository's actual
script; passing Vitest does not establish TypeScript correctness.
