# Computer Use

Use an available Computer Use/browser integration when the requested existing
session, visible browser behavior, or native UI is important. A skill does not
provide desktop access; discover exposed tools and read their runtime instructions
before acting. Do not presume a named "use computer" skill or a particular API is
installed. If an advertised companion skill applies, resolve it through discovery.

## Select Chrome explicitly

In supported OpenAI desktop integrations, `@Chrome` targets the connected Chrome
browser and `@Browser` targets the separate built-in browser. Follow an explicit
tab/app mention. Otherwise select Google Chrome by the browser identifier exposed
by the runtime, rather than automatic URL-based discovery or the OS default.
[OpenAI browser guidance](https://learn.chatgpt.com/docs/browser)

For example, if the current runtime documents `cua.createBrowserTab`, choose its
`"chrome"` backend and supply its documented options. This is a capability hint,
not permission to call an API absent from the active schema. Do not assume this
runtime exists in Codex CLI, OpenCode, or another computer integration.

Use other exposed browsers only for relevant coverage under the shared
[browser policy](browser.md). Desktop Firefox/Safari access does not establish
Playwright managed-build equivalence. A Chromium-based built-in browser is not
proof of branded Chrome coverage. Record actual browser and session provenance.

## Interaction and diagnostics

Prefer structured DOM/accessibility inspection and element interactions when
available. With visual-only access, use fresh screenshots and supported mouse/key
actions; do not guess stale coordinates. Verify visible outcomes after navigation
and substantial state changes. Capture layout evidence at the required viewport.

Console, network, and DOM inspection depend on the integration. OpenAI Developer
mode can expose full CDP for Chrome and its built-in browser, subject to settings
and approval. Do not enable it or change app/system permissions implicitly.
[Developer mode](https://learn.chatgpt.com/docs/browser#developer-mode)

Screenshots alone do not establish console/network access. Report unavailable
diagnostics, filtered logs, and capture intervals rather than declaring "no errors"
from their absence. Native app controls and browser chrome can require visual
interaction even when page DOM inspection is available.

Batch known actions when supported, but inspect results at meaningful state changes.
Use bounded state reads and targeted screenshots; do not assume a fixed token
ranking against Playwright from the integration's name alone.

Respect site, tab, app, and operating-system authorization. Existing login state is
not authority to inspect unrelated tabs, access credential stores, or submit real
transactions. Request normal UI authentication when needed and preserve the user's
session. Do not restart/terminate apps or change browser security settings to gain
access. See [Computer Use availability and permissions](https://learn.chatgpt.com/docs/computer-use).
