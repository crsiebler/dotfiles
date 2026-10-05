---
name: verify-interface
description: Verifies rendered UI behavior, accessibility, and browser errors.
---

# Verify Interface

Read [requirements](references/requirements.md) before selecting external tools or
running helpers. Dependency setup is separately authorized.

Read [browser guidance](references/browser.md). Identify the affected flow,
URL, expected behavior, viewport, and safe test data. Default to Google Chrome;
use other browsers for explicit requirements, browser-specific reproduction, or
relevant compatibility coverage. Report the browser/channel actually verified.

Respect a requested backend or authorized existing session. Otherwise prefer an
available Playwright CLI for routine web checks. Read only the selected reference:

| Backend | Reference and selection reason |
| --- | --- |
| Playwright CLI | [CLI](references/playwright-cli.md): concise commands and selective evidence reads |
| Playwright MCP or library/tests | [Playwright](references/playwright.md): exposed MCP tools or established project automation |
| Computer Use | [Computer Use](references/use-computer.md): connected browser session or native UI interaction |

Inspect actual tool schemas or installed command help; these interfaces are not
interchangeable. Missing tooling does not authorize installation or enabling a
connection. Choose another available, authorized backend when suitable and report
the change; never bypass a denied action by switching tools.

Navigate and exercise the real interface. Use accessibility/DOM snapshots for
structure, screenshots for layout, and console/network evidence for failures.
Check relevant keyboard, focus, loading, empty, error, and responsive states.
Report steps, expected/observed results, evidence, and gaps. If browser tooling
is absent, state verification is blocked; source inspection is not a browser pass.

Use a user-provided authenticated session when needed; never ask for passwords
or tokens in chat. Preview and explicitly approve externally posting, destructive,
or other state-changing interactions before performing them.
