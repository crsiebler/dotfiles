# Playwright CLI

Prefer an available CLI for routine checks when no backend or existing session was
specified. Inspect `playwright-cli --help` before using version-dependent commands.
This is the browser automation CLI, not just `playwright test` or `codegen`.
Absence is not permission to download packages through npm/npx or install skills.

Microsoft recommends CLI plus skills for coding-agent context efficiency; this is
not a measured token saving for the current task. Use concise output and selective
reads. See the [CLI guide](https://github.com/microsoft/playwright-cli).

## Chrome and commands

After verifying availability and scoped launch/navigation authorization:

```sh
playwright-cli -s=ui-check open http://localhost:3000 --browser=chrome --headed
playwright-cli -s=ui-check snapshot
playwright-cli -s=ui-check console error
playwright-cli -s=ui-check requests
```

Use fresh refs from the snapshot for interaction. Inspect individual requests with
`request <index>`. Check help for screenshot filenames, viewport changes, snapshot
depth/subtree filters, and artifact output. Keep one project-specific session name
on every command; do not reuse an unrelated `ui-check` session.

An application may configure `.playwright/cli.config.json`:

```json
{
  "browser": {
    "browserName": "chromium",
    "launchOptions": {
      "channel": "chrome",
      "headless": false
    }
  }
}
```

Inspect existing config and overrides before changing it. This example is guidance,
not authorization to modify another project's configuration. `chromium` is the
engine; `chrome` chooses the branded browser. Confirm actual session selection.
Use `--browser=firefox`, `--browser=webkit`, or `--browser=msedge` only for warranted
coverage and when supported locally; follow [browser policy](browser.md).

## Sessions and capture

Profiles normally remain in memory for the session. A fresh Chrome launch does not
inherit the user's normal login. An authorized existing Chrome session may be
attached through an already available extension or CDP endpoint; inspect local
help and connection permissions first. See
[session management](https://github.com/microsoft/playwright-cli/blob/main/skills/playwright-cli/references/session-management.md).

Do not enable remote debugging, edit a personal profile, or export authentication
state implicitly. Let the user authenticate through the selected UI when necessary.
Record whether the browser was launched or attached and when capture began.

Use the actual evidence path returned by the CLI and read only relevant sections.
Do not assume every installed version saves snapshots to files or exposes the same
network command names. Logs show the captured interval, not all browser history.
Console errors alone do not prove there were no uncaught page exceptions.

Use only scoped, authorized session cleanup. Avoid `close-all`, `kill-all`, and
`delete-data`; they can affect unrelated sessions or remove profile state. Detach
from an attached browser when authorized rather than terminating the user's Chrome.
Do not claim the CLI, browser, or installation was tested from help/source checks.
