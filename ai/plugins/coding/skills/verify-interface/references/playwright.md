# Playwright MCP and project automation

Use an exposed Playwright MCP connection for interactive exploration, or existing
project Playwright scripts/tests for repeatable flows. Respect the requested
backend and session. Established tests with concise results can avoid repeated
manual exploration; a test pass covers only its exercised assertions.

## MCP

Inspect actual namespaces, schemas, connection settings, and session identity.
Snapshot, interaction, console, and network tools are not interchangeable with
Chrome DevTools or CLI commands. Discover exact names rather than copying guessed
`browser_*` calls. Ref identifiers belong to the current snapshot and session.

The server's `--browser chrome` selects Google Chrome; `firefox`, `webkit`, and
`msedge` select other supported targets. Its extension/CDP modes can attach to an
existing Chromium session. Configuration changes, connection enabling, runtime
installation, and browser restarts remain separately scoped operations.
[MCP configuration](https://github.com/microsoft/playwright-mcp#configuration)

Request bounded snapshots and relevant console/network results when the exposed
schema supports them. Use screenshots for layout. Tool availability does not prove
capture completeness, and a connected session may predate diagnostics collection.
MCP schema/snapshot overhead can exceed CLI overhead, but no universal token ratio
is established. Reuse the session when appropriate; do not switch tools just to
optimize an unmeasured cost at the expense of relevant evidence.

## Library and tests

Inspect the project's runner, dependency version, configured projects, fixtures,
reporter, and side effects before running it. Use an existing installed executable
or project command; do not trigger npx downloads, add dependencies, generate a new
suite, or rewrite a browser matrix as an incidental verification step.

For an authorized launch, the JavaScript library selects Chrome with:

```javascript
const browser = await chromium.launch({ channel: 'chrome' });
```

In Playwright Test, select an existing project whose `use.channel` is `chrome`;
a project named "Chrome" or the `Desktop Chrome` device preset alone does not
establish the channel. Default test execution can run every configured project,
so select affected coverage using the actual runner options.
[Browser channels and projects](https://playwright.dev/docs/browsers)

Register console, `pageerror`, request/response, and request-failure listeners before
reproduction when writing authorized diagnostic code. Inspect HTTP error statuses
as well as transport failures. Use ARIA snapshots for semantics and screenshots for
layout. Summarize relevant failures without exposing credentials or response bodies.
[Console API](https://playwright.dev/docs/api/class-consolemessage),
[network events](https://playwright.dev/docs/network), and
[snapshot testing](https://playwright.dev/docs/aria-snapshots)

## Cross-browser limits

Apply the shared [browser considerations](browser.md). Normal Playwright APIs cover
console, snapshots, screenshots, and network categories across supported engines;
wrappers may expose a subset. Browser-specific text, semantics, rendering, and
network behavior can differ, so compare outcomes rather than expecting equal logs.

CDP attachment works only with Chromium-based browsers and has lower fidelity than
a native Playwright protocol connection. Full CDP inspection is not portable to
Firefox or WebKit. Chrome DevTools tools are an optional Chromium diagnostic
surface, not evidence of universal backend parity.
[CDP limitations](https://playwright.dev/docs/api/class-browsertype#browser-type-connect-over-cdp)
