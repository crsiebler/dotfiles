# Requirements

## Required and conditional dependencies

Use the target project's test runner, declared environment, and version pins.
No universal runner/package is required by this instruction-only skill. Python's
`unittest` is standard library; pytest and pytest-cov apply only to configured
pytest projects/coverage requests. Vitest applies to configured JavaScript/TypeScript
projects; coverage providers, jsdom, or happy-dom depend on the actual configuration.
A Bun test project is not automatically a Vitest project.

Browser accessibility checks conditionally need the project's Playwright Test
runner (`@playwright/test`), `@axe-core/playwright`, its resolved `axe-core` engine,
a matching installed browser and an authorized app fixture. Inspect manifest,
lockfile, installed versions and selected Playwright projects; a CLI/MCP tool or
jsdom alone does not satisfy these dependencies. No universal accessibility
package, global installation or new MCP server is required for other test suites.

## Installation and checks

Restore declared dependencies using the project lockfile after setup approval.
For npm projects, `npm ci` restores tools, replaces `node_modules`, and can
run lifecycle scripts; review those effects. Do not download through bare `npx`
when a runner is absent.

For a separately approved new Python test environment:

```sh
python3.11 -m venv .venv-tests
./.venv-tests/bin/python -m pip install 'pytest==<approved-version>'
./.venv-tests/bin/python -m pytest --version
```

Replace the placeholder; preserve existing environments. Add coverage packages
only when required and approved. For Vitest additions, follow the project's package
manager and authorize manifest changes before installing its selected version.
See [pytest setup](https://docs.pytest.org/en/stable/getting-started.html),
[Vitest setup](https://vitest.dev/guide/), and
[npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci).

For separately approved Playwright accessibility setup, use the project's package
manager to add the approved compatible adapter as a development dependency and
update its lockfile. Do not add a direct `axe-core` dependency merely because the
adapter uses it. Browser downloads, app/service startup and fixture setup need
their own applicable authority. Missing setup blocks execution; reviewers hand
setup back to the caller rather than installing or changing the suite.
See [Playwright accessibility setup](https://playwright.dev/docs/accessibility-testing)
and [the execution reference](playwright-accessibility.md).

Database fixtures, browsers, Docker, and services remain project-specific
conditional dependencies with their own permissions. Runner availability is not
a passing test result; report missing checks accurately.
