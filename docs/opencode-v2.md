# OpenCode V2 configuration

Repository sources target OpenCode 2.x or newer. Configuration installation is
separate from upgrading the executable and from provider authentication. The
October 24, 2026 source migration did not change installed user configuration.

## Source contracts

| Source | V2 behavior |
| --- | --- |
| `ai/opencode/opencode.json` | `commands`, `agents`, `providers`, `plugins`, ordered `permissions`, and `mcp.servers` |
| `ai/opencode/cli.json` | Global CLI theme and built-in attention notifications/sounds |
| `scripts/render-agents.py` | Five generic Markdown roles; ordered permissions and optional `provider/model#effort` selections |
| `ai/opencode/agents/sprite-artist.md` | Native image-provider adapter; asks for image calls, shell execution, and external-directory access |

MCP server names, commands, environment references and approval exceptions are
preserved. `disabled` is the inverse of the former `enabled`; the Jev timeout
sets both catalog and execution to 60,000 ms. Namespace rules precede exact read
exceptions. Unknown/write tools still ask, and unapproved Exa/Context7 tools
remain denied. Reviewer permissions remain inherited; auditor starts with
deny-all and permits only read/glob/grep. Installer reconciliation recognizes
both old and new permission syntax, including agent overrides.

The session model remains Astra. Luna is selected only for `agents.title.model`,
V2's replacement for `small_model`. Generic roles have no model pins. Explicit
renderer effort overrides require a model and use its named variant; available
variants still need native verification. Effort-only OpenCode output fails
before writing rather than producing ignored per-agent request options.

Bonsai keeps its local endpoint, context/output limits, timeout settings and
`reasoning_content` compatibility field. The legacy reasoning/temperature
booleans are omitted because V2 ignores them. See [Bonsai](local-bonsai.md) for
server defaults and the pending streaming/tool-result check. `lsp: true` is
also removed: V2 currently does not run language servers or produce LSP
diagnostics. Use project lint, typecheck and compiler commands for verification.

## Built-in notifications

`cli.json` enables `attention.notifications` and `attention.sound`, with volume
0.4 and the `opencode.default` sound pack. Notifications normally appear when
the terminal is unfocused. Actual delivery depends on the terminal and OS
notification settings; the former notifier's per-event messages and focus
options are not translated into unsupported fields. The built-in
`opencode.notifications` plugin stays enabled by default. There is no external
notifier package in the server `plugins` array.

## Optional image generation

[opencode-img@0.2.0](https://github.com/mattsafaii/opencode-img) is the identified
V2 option: its source imports `Plugin` from `@opencode/plugin`, declares
`^2.0.10`, and registers `gpt_imagegen` through `Plugin.define`. It supports
generation and reference-image editing with provider API credentials. This
is source-level compatibility evidence, not a live test or endorsement.

The plugin is deliberately optional. After separately authorizing provider
setup and its API billing, add the pinned package to the existing V2 `plugins`
array, preserving other entries:

```json
{"plugins": ["opencode-img@0.2.0"]}
```

OpenAI calls require an API key and separate API billing; a ChatGPT OAuth
subscription is not sufficient. Review upstream setup for other providers.
OpenCode fetches configured packages on startup. Do not print credentials or
install dependencies merely to validate source configuration. Inspect the
exposed tool schema, preview the batch/cost, and obtain generation approval as
required by `create-sprites`. Without a provider, `/create-sprite --plan-only`
and integration of supplied images remain available.

The retired `opencode-gpt-imagegen` uses the V1 plugin API. It is not carried
forward. The subscription-based `opencode-imagen` alternative advertises V2
but pins an older `0.0.0-next-17444` SDK; it has not been established compatible
with the current stable V2 SDK and is not configured here.

## Activation and verification

1. Preserve installed customizations and needed rollback files. V1 and V2 share
   configuration locations; do not run V1 against these native V2 sources.
2. Upgrade the executable separately following the official V2 instructions.
   The repository installer requires `opencode --version` to report 2.x or newer
   and stops before installed writes if it reports V1 or an unknown format.
   For an existing curl installation, the official V2 installer replaces the V1
   binary: `curl -fsSL https://opencode.ai/v2/install | bash`. Follow the
   [migration instructions](https://opencode.ai/v2/docs/migrate-v1) for other
   installation methods. Refresh the shell command cache (`hash -r`), then check
   `command -v opencode` and `opencode --version`; an older PATH entry may still
   select V1. Do not use configuration installation to upgrade a binary.
   `make check-install-prerequisites` checks the required CLIs without preparing
   sources/destinations or installing. Broad `make install` runs this check before
   Zsh extensions or shell/env/global Git writes, even with parallel make. Later
   AI source/destination checks still run separately; this is not rollback of
   changes from an earlier failed installation.
3. Separately authorize `make install-opencode` (or `make install-ai`). It backs
   up changed files and copies managed source bytes. Validation and cleanup
   preview require no OpenCode binary and make no installed changes.
4. Restart OpenCode and verify role/command discovery, title/session model
   selection, exact MCP read exceptions, write/unknown-tool prompts, auditor
   restrictions, and an unfocused-terminal notification. Verify Bonsai and any
   selected image provider with bounded authorized calls separately.
5. Retain rollback copies before `make clean`. Cleanup recognizes timestamped
   `cli.json` backups plus legacy `tui.json` and notifier backups. It preserves
   active legacy files; review their exact paths separately before removal.

Automated checks use repository-local fixtures for renderer output, installer
version/token/conflict preflight, byte-preserving installation and cleanup,
MCP permission behavior, and native V2 field projections. The installed CLI was
1.18.34 during migration; native V2 loading, notifications and image generation
were not exercised. No global installation is used as a test.

Sources: [official migration guide](https://opencode.ai/v2/docs/migrate-v1),
[CLI settings](https://opencode.ai/v2/docs/cli/config),
[CLI schema](https://opencode.ai/v2/cli.json),
[provider schema source](https://github.com/anomalyco/opencode/blob/dev/packages/schema/src/config/provider.ts),
[image plugin source](https://github.com/mattsafaii/opencode-img/blob/master/src/index.ts).
