# Requirements

## Select one available backend

This instruction-only skill needs an exposed browser capability or installed
automation backend. Do not install every alternative. Default to Google Chrome
when available and authorized; other browsers are targeted coverage choices.
Follow [browser considerations](browser.md) and the selected backend reference.

| Backend | Required when selected | Conditional dependencies |
| --- | --- | --- |
| Playwright CLI | Node.js 18+ and npm, `@playwright/cli`, selected browser | CLI-supported extension/CDP attachment for an existing authorized session |
| Project Playwright tests | Project-compatible Node/package manager and declared Playwright package | Matching browser binaries, configured fixtures/services |
| Project axe scans | Existing Playwright suite and project-local `@axe-core/playwright` | Its resolved `axe-core` engine, matching browser, safe app fixture |
| Playwright MCP | An exposed configured MCP server with its declared runtime and browser | Extension/CDP attachment supported by that server/version |
| Chrome DevTools MCP | Exposed configured server and its documented Node/Chrome requirements | Authorized existing Chrome attachment |
| Computer Use | Enabled computer/browser plugin, supported OS/app, exposed runtime APIs and granted permissions | Chrome support/session selected through that runtime |

Computer Use is not a pip/npm package. Enabling a plugin or installing a CLI does
not expose its APIs automatically to every harness. Consult
[Browser setup](https://learn.chatgpt.com/docs/browser) and
[Computer Use setup](https://learn.chatgpt.com/docs/computer-use) for the applicable
desktop environment; a built-in browser is distinct from Chrome.

## Installation and checks

After approving global multi-project CLI setup, select an explicit version:

```sh
node --version
npm --version
npm install -g '@playwright/cli@<approved-version>'
playwright-cli --version
playwright-cli --help
```

Replace the version placeholder using the [official CLI guide](https://github.com/microsoft/playwright-cli).
A project-local installation is an alternative when its manifest/lockfile changes
are approved. Do not use `install --skills` just to duplicate this skill.
For missing Node, follow the target project's version manager; existing Homebrew
can supply `brew install node` when that version fits
([formula](https://formulae.brew.sh/formula/node)).

Chrome can be installed separately with `brew install --cask google-chrome`
on macOS with Homebrew, or the [vendor installer](https://www.google.com/chrome/)
on supported platforms. Confirm the actual browser/channel, not only its engine.
Project Playwright setup should restore its locked dependencies and download only
the required browser using its installed CLI, for example
`./node_modules/.bin/playwright install chromium` for managed Chromium.
This is not branded Chrome. Browser downloads/native OS dependencies are separate
setup actions; check local help before choosing a browser/channel.

For axe scans, inspect the project's manifest/lockfile and installed package tree
for Playwright, `@axe-core/playwright` and its resolved `axe-core` version. A
separate direct `axe-core` dependency is not automatically needed. Check the
configured browser and app fixture as well as package availability. If absent,
report the missing prerequisite; do not install it. When setup is separately
approved, add the adapter as a project development dependency using the existing
package manager and approved compatible version, updating the lockfile through
that manager. No global package or new MCP server is required for this path.
See [Playwright accessibility setup](https://playwright.dev/docs/accessibility-testing).

For MCP, use [Playwright MCP setup](https://github.com/microsoft/playwright-mcp)
or [Chrome DevTools MCP setup](https://github.com/ChromeDevTools/chrome-devtools-mcp).
Preserve existing server configuration and permissions; confirm exposed schemas.
Never grant remote debugging/profile access implicitly. Help/version checks do
not verify rendering, logs, browser launch, attachment, or network capture.
