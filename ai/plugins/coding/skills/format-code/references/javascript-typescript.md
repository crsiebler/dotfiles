# JavaScript and TypeScript formatting

Read `package.json` scripts, lockfiles, runtime pins, Prettier/ESLint configs,
and any Husky/lint-staged configuration. Use the established package manager
and locally installed binaries. Do not assume Bun or fetch tools through an
on-demand runner when dependencies are absent.

Typical local binary command shapes:

```sh
prettier --check path/to/file.ts
prettier --write path/to/file.ts
eslint path/to/file.ts
eslint --fix path/to/file.ts
```

Prefer configured scripts where they support the required scope. Check argument
forwarding and script bodies before execution; a script named `lint` may write.
Preserve formatter plugins and project rules. Review changes after automatic
fixes and rerun checks. Do not change lint rules to suppress valid failures.

Husky/lint-staged only run if configured; do not promise they exist. Do not
commit just to trigger them. For Bun projects using Vitest, `bun run test` or
`bun run test:ci` runs the named script only if defined. **Do not use `bun test`
as a Vitest substitute**: it runs Bun's separate test runner. Consult `run-tests`
for test execution and run the actual project typecheck script separately.
