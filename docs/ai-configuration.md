# AI configuration

OpenCode sources require V2 (2.x or newer). See [V2 configuration](opencode-v2.md)
for native fields, built-in notifications, optional image generation, and
activation checks. The installer rejects V1 before writes and does not upgrade it.

This guide describes the checked-in implementation, not a claim that live
authentication, model access, or every integration has been verified. Installation
and connection setup are separate, explicitly authorized operations.

## Contents

- [Sources and installed layout](#sources-and-installed-layout)
- [Skill dependencies and setup](skill-dependencies.md)
- [Installation and replacement behavior](#installation-and-replacement-behavior)
- [Connecting applications](#connecting-applications)
- [Local Bonsai 2 installation and OpenCode setup](local-bonsai.md)
- [Native agents and workflow review](#native-agents-and-workflow-review)
- [Validation and manual evaluation](#validation-and-manual-evaluation)
- [Troubleshooting and rollback](#troubleshooting-and-rollback)
- [Manual removal of old AI files](remove-old-ai-files.md)

## Sources and installed layout

| Source | Purpose and destination |
| --- | --- |
| `.agents/plugins/marketplace.json` | Checkout-local `craft` marketplace; no remote skill source |
| `ai/plugins/<plugin>/skills/<action>/` | Portable skill bodies, scripts, and references |
| `ai/AGENTS.md` | Single harness-agnostic personal policy; copied byte-for-byte to `AGENTS.md` in both user configuration roots |
| `ai/codex/config.toml` | Managed Codex defaults and MCP connections |
| `ai/opencode/{opencode.json,cli.json}` | OpenCode V2 server configuration and CLI settings with built-in notifications |
| `ai/codex/agents/*.toml` | 5 canonical custom-agent sources; all copied unchanged to Codex, Markdown generated for OpenCode |
| `run-agent-team/references/story-execution.md` and `review-story/references/contract.md` in coding skills | Team delivery and reusable staged-review contract |
| `ai/opencode/agents/*.md` | One native OpenCode-only agent: `sprite-artist`; copied unchanged |
| `ai/opencode/commands/` | `/create-sprite`, `/define-requirements`, `/plan-work`, `/ship`, `/find-agents`, and unchanged `/review-pr` |
| `scripts/install-ai.py`, `scripts/render-agents.py` | Local installer and two-harness agent renderer |
| `ai/plugins/delegating/skills/use-subagents/scripts/subagents` | Skill-bundled discovery helper |

Codex defaults to `$HOME/.codex`; an explicit `CODEX_HOME` must be absolute.
OpenCode defaults to `$HOME/.config/opencode`; an explicit `XDG_CONFIG_HOME`
must be absolute and names the parent config directory, not `opencode` itself.
Codex receives all native source copies under its `agents/` directory and plugins through
native local marketplace registration. OpenCode receives copied skills through
the existing `skills` CLI, plus generated agents, one native agent, and commands.

The root [AGENTS.md](../AGENTS.md) is separate repository-only policy, not installed
personal instructions. The installer reads `ai/AGENTS.md` with `read_bytes()` and
copies it without concatenation or normalization. Application inventories and
setup belong in this guide, not the personal policy.
Edit canonical TOML role bodies, not generated
OpenCode Markdown; edit the one OpenCode-only agent in its native Markdown.
Agent metadata lives in native sources, with generic TOML-to-Markdown rendering;
there are no exclusions or overrides JSON files.

### Five plugins and skill names

| Plugin | Skills |
| --- | --- |
| `coding` | `apply-ai-standards`, `apply-app-standards`, `apply-blockchain-standards`, `apply-database-standards`, `apply-infrastructure-standards`, `apply-integration-standards`, `apply-language-standards`, `apply-web-standards`, `archive-run`, `assess-controls`, `create-mcp-server`, `create-skill`, `develop-code`, `format-code`, `manage-changes`, `map-codebase`, `operate-systems`, `prepare-implementation`, `resolve-review-feedback`, `review-code`, `review-story`, `run-agent-team`, `run-tests`, `verify-interface`, `write-requirements` |
| `reporting` | `assess-work-item`, `plan-product`, `report-progress`, `report-project-status` |
| `researching` | `analyze-data`, `read-docx`, `read-pdf`, `read-pptx`, `read-xlsx`, `research-users`, `search-web` |
| `delegating` | `prepare-handoff`, `use-subagents` |
| `producing` | `create-audio`, `create-docx`, `create-gif`, `create-pdf`, `create-pptx`, `create-sprites`, `create-xlsx`, `design-interface`, `write-content` |

Use the skill identifier actually advertised by the harness; do not guess Codex
namespace syntax or cached installation paths. Resolve bundled resources from
the loaded skill location. Marketplace authentication policy is `ON_USE`, not an
instruction to log in during installation.

Every Craft skill links to its bundled `references/requirements.md`. Read it
before selecting external utilities or running helpers. The
[dependency audit](skill-dependencies.md) inventories all 47 skills and explains
setup, authorization, and availability checks. AI installation copies these
instructions; it does not install Python packages, CLIs, browsers, renderers,
model weights, or provider authentication.

### Coding workflow consolidation

`develop-code` owns feature implementation, diagnosis/fixes and behavior-preserving
refactors, with conditional architecture and testing references. `review-code`
remains independently discoverable for local changes, PRs, components and bounded
audits, with nine conditional review lenses. Helpers select project-native tools.
The three old development bundles are retired without aliases.

The [project guidance template](templates/code-repository-AGENTS.md) is optional:
merge verified project facts and commands into existing guidance; do not install
it globally or replace a project's instructions blindly. The slimmer personal
policy and five custom roles should activate with the updated coding
bundle. Follow [coordinated activation and rollback](remove-old-ai-files.md#consolidated-coding-workflows).
[Verification](coding-workflow-verification.md) distinguishes static checks from
the user-waived live evaluations; source delivery does not establish installed
routing or behavioral quality.

### Custom roles and native execution

The five custom roles are researcher, planner, reviewer, auditor and operator.
Implementation uses the main session or native execution agents: Codex worker or
OpenCode general for delegated work, with matching skills and task contracts.
The existing five plugins contain 47 skills. Select roles by responsibility and
load specialized knowledge from the relevant skill, without aliases or automatic dispatch.
Only auditor retains read-only metadata; reviewer supports scoped verification.
The main session owns coordination. See
[role selection](../ai/plugins/delegating/skills/use-subagents/references/core-roles.md)
for responsibility boundaries and runtime selection. No custom implementation
role or built-in override is defined in source for either harness.
Source changes do not activate installed roles or skills; installation remains
separately authorized.

### UI verification backends

The [verify-interface skill](../ai/plugins/coding/skills/verify-interface/SKILL.md)
defaults to Google Chrome and prefers an available Playwright CLI for routine web
checks, while respecting requested backends and authorized existing sessions.
Its conditional references cover [Playwright CLI](../ai/plugins/coding/skills/verify-interface/references/playwright-cli.md),
[Playwright MCP and project tests](../ai/plugins/coding/skills/verify-interface/references/playwright.md),
and [Computer Use](../ai/plugins/coding/skills/verify-interface/references/use-computer.md).
Shared [browser guidance](../ai/plugins/coding/skills/verify-interface/references/browser.md)
distinguishes Chrome, Chromium, Firefox, WebKit/Safari, Edge, and Brave, with
optional compatibility coverage and console/snapshot/network/CDP limitations.

For accessibility, [verify-interface](../ai/plugins/coding/skills/verify-interface/references/playwright-accessibility.md)
owns rendered journeys, keyboard/focus and assistive-technology observations;
[run-tests](../ai/plugins/coding/skills/run-tests/references/playwright-accessibility.md)
owns project Playwright execution and the axe-core regression pattern through
`@axe-core/playwright`. The generic `reviewer` can execute prepared, authorized
checks while preserving the candidate and workflow-supplied contract. It does
not edit tests, install dependencies or suppress findings. Required checks must
be attributable to the reviewed build; missing tooling or a stale server cannot
produce a pass. Automated violations, inconclusive results and manual coverage
are reported separately; passing axe is not a WCAG conformance claim.

The adapter/engine and browser are conditional project dependencies, documented
in the [dependency inventory](skill-dependencies.md). No accessibility-specific
agent, new plugin, global dependency or MCP server is added. Installation and live
browser verification remain separate from these source guidance changes.

This is source guidance, not a browser installation or connection grant. The AI
installer does not provision Playwright CLI, browsers, extensions, or Computer Use.
Codex source MCP configuration still omits the optional OpenCode browser servers.
Refresh/install the coding bundle only under separate installation authorization;
source validation does not establish live diagnostics or installed discovery.

### Shipping and GitHub assessment

`manage-changes` owns scoped commit/push/PR shipping; GitHub is the implemented
external adapter. It prepares exact write previews before requesting approval
for a bounded sequence and carries that approval forward unless scope changes.
Descriptions summarize final behavior across all commits, including an authorized
archival closeout commit, with actual validation and limitations. No implicit merge.
`assess-work-item` has a dedicated GitHub issue/Projects adapter, selecting adequate
exposed read tools or installed gh. It distinguishes issue/PR/draft project items,
handles pagination/coverage gaps, and defaults to a draft. Posting still requires
a verified comment target and exact scoped approval. No live account access is
established by source validation; source delivery does not install these changes.

### Review feedback consolidation

`resolve-review-feedback` now owns assessment and resolution preparation.
Analysis-only requests return findings; resolution requests verify evidence at
the PR head before preparing exact write previews. Code implementation and
pushes remain separately authorized work. GitHub details live in the bundled
`references/github.md`; `analyze-review-feedback` is retired without an alias.
Follow the [migration steps](remove-old-ai-files.md#combined-review-feedback-skill)
for separately authorized activation and installed-copy cleanup.

### Producing and document skill activation

Production skills create artifact files; researching skills extract source-located
evidence; reporting skills own report content and communication. Use an adequate
native reader for simple reads. `create-skill` supports portable authoring,
evaluation evidence and packaging without requiring native agents or token metrics.
`create-gif` supports supplied/procedural frames without an AI provider and routes
optional pixel artwork through the discovered `create-sprites` workflow.

The eight document bundles are original implementations. Required packages, fonts,
optional renderers and tested versions live in each installed skill's
references/requirements.md and requirements.txt. Python 3.11+ is the source baseline;
[verification](document-skill-verification.md) distinguishes the tested dependency
runtimes from unverified pairings. Dependency setup is separately authorized: AI
installation does not install Python packages, fonts, renderers or image providers.
No general Office editing, OCR, automatic conversion or formula engine is supplied.

1. Preserve customized installed copies and needed backups before activation.
   Inspect the registered local `craft` source and current installed plugin/skill
   inventory; keep this checkout available. Source edits alone do not establish
   that an already-running task loaded the new instructions.
2. With separate installation authorization, choose the documented `make install-codex`,
   `make install-opencode`, or `make install-ai` target. Coordinate `coding`,
   `researching`, and `producing` so the old coding-owned audio/sprite copies do not
   remain discoverable beside their producing replacements.
3. For Codex, use native plugin management and verify the resulting loaded sources.
   CLI 0.153.4's `plugin marketplace upgrade` refreshes Git marketplace snapshots;
   it is not a local-checkout refresh guarantee. If a stale plugin snapshot remains,
   preview native removal/re-addition of the exact affected plugin IDs and obtain
   scoped approval before replacement. Preserve custom copies first. Never delete
   plugin caches manually or remove the whole active marketplace as routine cleanup.
4. For OpenCode, authorized installation copies each local bundle through `skills`.
   Audio/sprite names and command references stay unchanged; their same-named active
   installed paths are not obsolete merely because source ownership changed.
   The installer preserves changed skill assets in its documented backup location.
5. Restart the selected harness and start a new Codex task. Verify seven producing
   skills, create-skill in coding, and the four readers plus search-web in researching,
   without unwanted duplicates. Run the loaded helper's `check` in the intended
   dependency environment; missing packages are a setup gap, not permission to install.
6. Only after verification, review exact obsolete standalone copies using the
   [rollout cleanup procedure](remove-old-ai-files.md#producing-and-document-rollout).
   Cleanup/deletion and native replacement need separate scoped approval. Retain
   needed backups; never treat a matching skill name as deletion authorization.

`create-audio` bundles a model-independent generation workflow, a Stable Audio
3 Small-SFX MLX adapter, and explicit local setup. OpenCode JSON adds
`/create-audio`, which loads the installed
skill using the current chat model. Stable Audio is not listed as a chat model.
Agents invoke `scripts/create_audio.py` relative to the installed skill; no Zsh
alias is installed. Stable Audio infrastructure defaults to `~/Models/local-audio/` or
`LOCAL_AUDIO_MODELS_ROOT`; projects supply prompts, model selection, sampling
settings, output, and cache locations. See the
[audio guide](../ai/plugins/producing/skills/create-audio/references/local-audio.md).
Directory-based skill discovery installs its scripts without an installer
special case. Model provisioning remains separate from AI configuration installation.

`search-web` selects available search, page-fetching, or multi-step research tools
by their exposed schemas. Its core guidance is provider-agnostic; Exa MCP details
are loaded conditionally from `references/exa.md`. Plugin skill discovery is
directory-based, so the rename needs no installer or manifest special case.
For retained installed `use-exa` copies and Codex plugin refresh, follow the
[rename cleanup steps](remove-old-ai-files.md#renamed-web-research-skill).

`map-codebase` creates or updates persistent, source-backed technical documents
when explicitly requested. It defaults to `docs/overview.md` plus cohesive subject
documents directly in `docs/`, reuses existing guides, and adds a concise project
`AGENTS.md` discovery reference. Readers select relevant documents and verify
affected source; links do not establish automatic indexing. Detailed procedures
may move out of `AGENTS.md` only within authorized documentation consolidation,
preserving mandatory rules and concise workflow obligations. Routine refreshes
update affected subjects without rewriting policy or execution state. Read-only
requests return proposed content instead of saving. Directory-based discovery
requires no new command, agent, or installer special case.

The [runtime selection guide](runtime-selection.md) describes the coding plugin
policy loaded by run-agent-team. Base Codex selects Sol 6.1; select another model
directly when needed. Select OpenCode's session model directly as well; no hidden
build/subagent pins apply. Reusable roles omit model and effort settings. Verify account
availability and effective settings after separately authorized activation;
source validation does not prove model access, automatic routing or quality.

## Installation and replacement behavior

From the checkout:

```sh
make validate-ai
# Only with explicit installation authorization, choose one:
make install-codex
make install-opencode
make install-ai
```

Python 3.11+ is required for validation, rendering, and installation; Make defaults
to `python3.11`. Codex installation requires native local marketplace and plugin
add/list/remove support. Prerequisites inspect those commands with `--help`,
including marketplace listing's `--json` and plugin listing's `--marketplace`,
`--json`, and `--available` options, before preparing sources or destinations.
There is no exact Codex release pin. Existing preflight still validates listing
JSON and local source ownership; command help alone does not prove installation
or configuration compatibility. CLI failures remain blockers.
OpenCode installation requires `opencode` 2.x or newer on `PATH`; a version
preflight rejects V1 before installed writes. Upgrade the executable separately.
All AI installation targets require `skills` on `PATH` for standalone retirement.
When retirement is planned, CLI 1.5.24 is required for its tested scoped-removal
contract. Preview does not require or run native CLIs. Missing prerequisites
are blockers: no `npx` bootstrap, login, dependency installation, or binary install
is performed by these targets.

`make check-install-prerequisites` runs the OpenCode/skills CLI checks only,
without source/destination preparation or installation. Broad `make install`
runs this before Zsh extension installation and shell/env/global Git writes,
including under parallel make. The later AI checks still validate sources,
retirement and destination conflicts; passing the early CLI check is not a
guarantee the entire installation will succeed. See [V2 upgrade steps](opencode-v2.md#activation-and-verification).

The installer registers the local checkout with Codex's native plugin interface
and adds `coding@craft`, `reporting@craft`, `researching@craft`,
`delegating@craft`, and `producing@craft`. OpenCode uses local `skills add` copies
rather than symlinks.
The checkout must remain available for subsequent local marketplace refreshes.

### Managed retirement

`make preview-ai-cleanup` previews all targets without writes or native CLI calls;
use `AI_TARGET=opencode` or `AI_TARGET=codex` to narrow it. Native plugin candidates
come from ownership records in preview; actual registrations are checked during
installation. Normal installation performs retirement after replacement installation.

`scripts/ai_retirement.py` owns versioned `.install-ai-skills.json` and
`.install-ai-plugins.json` inventories in the relevant configuration root. Missing
inventories bootstrap conservatively; malformed or foreign-checkout inventories
block rather than being overwritten. Skills are tracked by complete tree hashes,
so removal of a bundle retires its skills while moves between bundles preserve
current names. Inventories record verified standalone copies, not arbitrary files.
Expected skill copies account for the Skills CLI's exclusions (`metadata.json`
entries and `.git`, `__pycache__`, and `__pypackages__` directories). Installed
trees and retirement ownership checks remain exact; extra installed files are
not ignored. Generated source caches therefore do not cause false verification
failures, while customized installed trees remain protected.

Skill cleanup covers the selected private skill root and `$HOME/.agents/skills`.
For `all`, the private root is OpenCode's; Codex-only uses `$CODEX_HOME/skills`.
Shared cleanup affects every harness reading that root. Other private roots,
project-local copies, custom discovery paths, and unrelated skills are preserved.
Only exact previously recorded trees or explicit historical migration fingerprints
qualify. `analyze-review-feedback` has a verified migration fingerprint;
unrecorded `use-exa` versions and older names still need manual reconciliation.
Modified or symlinked candidates are reported and left in place.

Retired trees are copied to `.install-ai-backups/<timestamp>/retired/`, verified,
then removed at their exact paths before scoped `skills remove` reconciles CLI
tracking. This ordering avoids the CLI retaining an obsolete shared directory
because another harness discovers it. Other-agent copies can legitimately retain
CLI tracking. Existing CLI lock metadata is validated and backed up before removal;
an absolute `XDG_STATE_HOME` override is respected. Pending ownership is saved before removal so a failed CLI call can
be retried; a successful exit alone does not prove files were removed.

Codex keeps native Craft plugins and their Desktop marketplace presentation.
Only previously recorded plugin IDs absent from the current marketplace qualify
for native `codex plugin remove`, after checking the registered local source.
The installer preserves source snapshots under `.install-ai-backups/plugin-sources/`
and archives any existing matching native cache subtree before native removal.
It never deletes caches itself or removes the active marketplace. Previously
unrecorded plugin registrations are not inferred to be installer-owned.

Installation is still not transactional: failure may leave completed writes or
archival in place. Preserve inventories and backups, correct the reported blocker,
then rerun. Source updates alone do not execute cleanup. Restart the harness and
verify discovery after installation; run backup cleanup only when rollback is no
longer needed.

Managed JSON/TOML files replace installed files byte-for-byte. This applies to
Codex `config.toml` and OpenCode V2 `opencode.json` and `cli.json`.
The repository is authoritative: installed-only providers, models, profiles,
MCP settings, and custom overrides are removed from these files on installation.
Keep desired settings and permission restrictions in the repository sources before
installing. Environment references remain references; the installer does not
substitute secret values into configuration.

Before managed writes, installation accepts only the source's exact read-tool
exceptions within protected MCP namespaces. It refuses other overlapping OpenCode
allow rules (including inline agent permission/tool overrides), Codex overrides
that bypass write prompts, and expanded research-tool allowlists. Reconcile those
rules manually; errors do not print their values. Source OpenCode namespace rules
retain their order before exact exceptions.
An existing bare/trailing Exa or Context7 namespace deny requires reconciliation
before adding exceptions, because it may be an intentional blanket restriction.
Installed-only Codex tool disables and custom OpenCode denies are not merged into
the replacement; maintain required restrictions in the source. Unsupported Codex
approval values such as `deny` still block installation during preflight.
These checks also cover installed companion configs and Codex profiles, not
arbitrary project configuration; inspect project-level overrides separately.

Destination symlinks and conflicting skill assets are refused to protect files a
CLI directory replacement could lose. Reconcile `opencode.jsonc` manually if
present; the installer will not choose between it and `opencode.json`. Native
marketplace source collisions also require explicit reconciliation rather than
silently repointing a registration.

Source comments, formatting, and line endings are preserved. Changed files receive
adjacent timestamped backups before replacement; identical files are not rewritten.
Review installed files and retain any needed rollback copies outside cleanup
locations. `make clean` removes recognized installer backups for both harnesses,
including adjacent configuration/agent/command backups, timestamped skill and
retirement archives, and hashed plugin source snapshots. It preserves active
files, plugin caches, inventories, and unknown backup names. See the
[cleanup steps](../README.md#removing-backup-files). User-level `AGENTS.md` and same-name shipped agents/commands
are replaced, not prose-merged. Changed OpenCode skill files are backed up under
`.install-ai-backups/<timestamp>/skills/`. Unrelated files and stale assets are
not removed automatically, except verified managed retirements described above.

Writes use per-file atomic replacement, but installation is not a whole-operation
transaction. A later native CLI failure can leave earlier files installed. Native
Codex configuration changes are backed up even if the native command fails.

AI-only targets do not touch shell files, `.env`, global Git settings, or binaries.
Broad `make install` modifies shell files, `.env` and global Git settings and
installs OpenCode configuration. It does not install/upgrade CLI binaries, Codex
configuration or global subagents.

## Connecting applications

Connection definitions are not authenticated sessions. Use the installed
harness's help or current provider documentation for its actual login interface;
do not invent cross-harness CLI syntax. Installation never performs a login.
Approve authentication separately, keep credential stores private, and inspect
actual exposed tool schemas after connection. Tool presence is not authorization
to write external state.

| Connection | Default | Authentication/context |
| --- | --- | --- |
| `github` | Enabled globally | `GITHUB_MCP_TOKEN`; hosted GitHub MCP |
| `exa` | Enabled globally | `EXA_API_KEY`; hosted Exa MCP |
| `context7` | Enabled globally | `CONTEXT7_API_KEY`; hosted Context7 MCP |
| `vercel` | Disabled | Vercel MCP OAuth; hosted Vercel MCP |
| `jira` | Disabled | Atlassian Rovo v2 OAuth; `ATLASSIAN_CLOUD_ID` is site context |
| `postgresql` | Disabled | Project least-privilege database URI and built local Node `mcp-suite` server |
| `jev` | Disabled | `AI_GATEWAY_API_KEY` and built local Node `mcp-suite` evaluation server |
| `docker` | Disabled | Docker MCP Toolkit gateway; configure trusted servers or a profile in Docker Desktop |

AWS and Elastic MCP definitions are intentionally absent from both source configs.
Installation preserves unrelated installed entries, so older definitions may
remain until individually reviewed and removed with approval. See
[manual cleanup](remove-old-ai-files.md#4-review-old-codex-agents-and-configuration).

OpenCode additionally retains disabled optional Chrome DevTools, Playwright, Jam,
ElevenLabs, and Docker MCP Toolkit connections. Their presence does not authorize
starting them or downloading their runtime packages.

### Tool approval policy

| Service | Without tool approval | Requires tool approval |
| --- | --- | --- |
| GitHub | Exact configured repository, commit, issue, PR, search, and review reads | Edits, comments/reactions, pushes, branches, merges, settings and other mutations; unknown tools |
| Exa | Search, advanced search, fetch, and `agent_run` research | Other tools are denied/filtered, not merely prompted |
| Context7 | `resolve-library-id` and `query-docs` | Other tools are denied/filtered |
| Vercel | None | Every tool, including reads |
| Jira/Rovo | Exact documented reads, searches, discovery, and `executeRead` | Writes, destructive operations, and unknown tools |
| PostgreSQL | `check_dangerous_operations_allowed` | `execute_query` and unknown tools |
| Chrome, Playwright, Jam | All tools when the connection is enabled | No MCP tool-level prompts |
| ElevenLabs | None | Every tool, including reads |

GitHub/Jira/PostgreSQL use default `ask` in OpenCode and `prompt` in Codex, with
exact read exceptions (`allow` / `approval_mode = "approve"`). Exa/Context7 use
default deny plus exact allows in OpenCode; Codex filters them with `enabled_tools`
and approves those exact tools. Neither relies on broad `get_*`/`search_*` patterns
or server annotations to automatically approve newly introduced tools.

This policy does not enable disabled servers. Browser/audio connections remain
OpenCode-only; the disabled `docker` connection is available in both harnesses.
The auditor retains its narrower
permissions. Project/runtime overrides can still change effective behavior and
need separate inspection. MCP rules do not control `git push` or `gh` through
shell tools. Existing user-authorization rules for external actions and
`/review-pr --post` remain in force even when a browser tool itself needs no
permission dialog. Research calls may consume service quotas.

Rovo tool discovery varies by tenant and authentication. The exact names cover
the [v2 catalog](https://developer.atlassian.com/cloud/rovo-mcp/guides/supported-tools/)
and directly exposed reads in the
[support catalog](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/).
`executeRead` is the documented read dispatcher; `executeWrite` and
`executeDestructive` still prompt. Reads may include Confluence and connected
Teamwork Graph content. Attachment retrieval can return a download command;
executing that command is a separate operation, not part of the MCP allow rule.

PostgreSQL tool names and behavior were inspected at MCP-suite commit
[`2a2881a`](https://github.com/crsiebler/mcp-suite/blob/2a2881a5986d22349dd9fcec84820cd58656ed61/servers/postgresql/src/tools/index.ts).
There is no separate read-query tool. `execute_query` accepts arbitrary SQL and
can perform writes depending on server configuration; it always asks, even for
`SELECT`. These dotfiles neither classify SQL nor change database privileges.
Upstream tool changes require reviewing and updating the exact exceptions in both
source configs. Static/fake tests do not prove live server behavior.

### GitHub, Exa, Context7, and Vercel

GitHub uses `https://api.githubcopilot.com/mcp/` with only
`repos,issues,pull_requests` toolsets. Use a fine-grained PAT with one resource
owner, selected repositories, minimal permissions, and an appropriate expiry.
One fine-grained token does not span multiple resource owners; plan distinct
approved credentials/configuration for other owners. Organization approval or SSO
requirements may apply. Do not broaden permissions just to remove an error.

OpenCode supplies `Bearer {env:GITHUB_MCP_TOKEN}` with OAuth disabled; Codex uses
`bearer_token_env_var`. Exact read tools skip approval; other calls retain
`github_*: ask` / `default_tools_approval_mode = "prompt"`. Restricted toolsets are
not a read-only guarantee. Never print token values to troubleshoot the installer
preflight.

The `/review-pr` command uses separately authenticated `gh`. Its canonical
objectives, schema, context gathering, and orchestration live in
[`ai/opencode/commands/review-pr.md`](../ai/opencode/commands/review-pr.md).
`--post` must preview the exact GitHub review command or API payload and obtain
explicit confirmation before any review write. MCP write access does not waive it.

Exa uses its hosted endpoint with search, fetch, advanced search, and agent-run
tools; Context7 uses `https://mcp.context7.com/mcp`. The supplied environment keys
are referenced by headers in both harness configurations. Successful source validation proves
neither remote service access nor account quotas.

Vercel uses the official hosted endpoint `https://mcp.vercel.com` and its MCP
OAuth flow; no Vercel token is stored in either source configuration. The server
can manage projects and deployments, so every Vercel tool retains an approval
prompt in both harnesses. Authenticate through the harness after restarting it;
configuration alone does not establish account access or authorize mutations.

### Trusted project opt-in

Keep project integrations disabled in personal defaults. In a trusted project,
review the effective configuration and enable only the needed connection using
the harness's project configuration (`.codex/config.toml` or OpenCode's project
configuration). Preserve approval prompts and least-privilege credentials.
Project configuration itself is not consent to Docker lifecycle, migrations,
cloud mutations, or other sensitive operations.

**Atlassian Rovo:** The connection name is `jira`, and its provider is
`https://mcp.atlassian.com/v2/mcp`. Use harness-supported OAuth with an approved
Atlassian account/site. `ATLASSIAN_CLOUD_ID` identifies the site, not a credential.
Headless token authentication is a separate, explicitly approved setup using the
provider's current supported method; no token header recipe is installed here.
Inspect the exposed Rovo v2 tool schemas before use.

**PostgreSQL:** Both configurations refer to the custom local Node server from
[mcp-suite](https://github.com/crsiebler/mcp-suite), built at
`$HOME/Repositories/mcp-suite/servers/postgresql/dist/servers/postgresql/src/index.js`.
Keep the connection disabled until trusted project opt-in. Node must be available
on the harness's `PATH`, and the built entry point must exist. Follow the upstream
project's setup documentation; this installer does not clone, build, or install
`mcp-suite`, install Node, or verify the server's dependencies.

Codex uses `sh -c` with `exec node` and a quoted `$HOME` path; its `env_vars`
passes `HOME` and `POSTGRESQL_CONNECTION_STRING`. OpenCode invokes `node` directly
with `{env:HOME}` in the entry-point argument and an environment reference for
`POSTGRESQL_CONNECTION_STRING`. Neither configuration puts the URI in argv,
maps it to `DATABASE_URI`, or uses Docker.

Export `POSTGRESQL_CONNECTION_STRING` privately in the launching environment.
The launchers do not preflight missing or empty connection strings; validating
the connection string and enforcing server behavior are the server's
responsibility, not guarantees supplied by these dotfiles. Use a project-specific,
least-privilege database identity, not a superuser or production connection by
default. Preserve approval prompts and never dump environment values or connection
strings into logs. Configuration alone does not establish read-only enforcement.

**Docker MCP Toolkit:** Both configurations expose the Docker MCP Toolkit gateway
as the disabled `docker` stdio connection. Docker Desktop's MCP Toolkit must
be configured with the intended servers or profile before enabling it. The Codex
entry accommodates the gateway's documented startup time with a 60-second
timeout, and all Docker-provided tools continue to require approval in OpenCode
and Codex.
The gateway can manage server lifecycle and credentials for the configured
profile; configuration alone does not authorize Docker lifecycle operations or
access to host resources.

## Native agents and workflow review

There are 5 canonical TOML roles, copied unchanged to Codex and rendered for
OpenCode. The sole native OpenCode-only role is sprite-artist (6 total).
Only auditor retains read-only native settings. reviewer inherits
runtime permissions, performs authorized focused verification and cannot edit
the candidate. Parent overrides and MCP approvals are independent controls.

The staged review procedure belongs to review-story, not a specialized role.
run-agent-team loads its complete contract through discovery and supplies it to
an independent reviewer with candidate identity, acceptance criteria,
pass/session metadata, verification commands and budgets. Ordinary sessions are
sufficient; goal APIs are optional. Planning defaults to PLAN.md in both harnesses.
When the runtime has no custom-role selector, the workflow supplies the full
discovered reviewer instructions to a fresh independent generic agent under the
same grant. It records this binding honestly and preserves pins, permissions,
candidate restrictions and same-session limits. See
[reviewer binding](../ai/plugins/coding/skills/run-agent-team/references/story-execution.md#reviewer-binding).

[Agent workflows](agent-workflows.md) describes bounded review, persistent blockers,
candidate-equivalent testing, state ownership and archival. Installation must
refresh role and skill sources together; a plugin-only refresh leaves stale role
instructions. Restart and verify unique discovery in a new session. See the
[retirement inventory](remove-old-ai-files.md#retired-runner-and-story-role) before
removing any installed copies. Source removal does not authorize global cleanup.

## Validation and manual evaluation

Repository-local commands:

```sh
make validate-ai
python3.11 -m unittest discover -s tests -p '*test*.py'
python3.11 tests/agent_contract_test.py
bash tests/zsh_aliases_test.sh
zsh -n aliases/.aliases zsh/.zshenv zsh/.zshrc
```

There is no standalone repository typecheck target. `validate-ai` checks local
plugin structure, JSON/TOML syntax, and both Python renderer targets without
starting a harness or MCP. Python tests cover installer replacement and backups,
environment sync, discovery, and an isolated native plugin contract. That native
test runs against the installed Codex version and skips only when Codex is missing;
report failures and skips rather than claiming live compatibility. Story review tests check portable contracts and provenance; these do not prove
live agent behavior.

MCP contracts retain explicit expected connection sets, schema projections,
approval rules, and secret-reference checks. PostgreSQL transport tests run a fake
`node` in project-local scratch space with an allowlisted environment and a `HOME`
containing spaces and shell metacharacters. They check argv, path resolution,
connection-string passthrough, exit status, and secret-free output, including a
missing-Node failure. OpenCode's known environment substitutions are modeled in
the test, not exercised through its real configuration loader. No real
`mcp-suite` server or database starts; these tests do not verify server-side
connection validation, database permissions, or live harness integration.

The following are **manual evaluation cases, not recorded successful runs**:

- After authorized installation, restart each harness and verify skill/role
  discovery, intended source checkout, and native
  delegation. Start a new Codex thread after plugin changes.
- Test an approved scoped GitHub read and verify the prompt; draft a PR review
  without posting. Verify `--post` stops at the exact payload confirmation gate.
- Connect Exa and Context7 with an approved minimal request; record service and
  credential errors without secret values.
- Enable each project integration separately and verify account/site or database
  identity using approved non-mutating requests. Confirm other
  project connections remain disabled. Do not test mutation by performing it.
- In an authorized disposable project, evaluate the generic reviewer with
  review-story in inspection-only and execute modes. Verify candidate attribution,
  same-session targeted review, memory validation and failed-check behavior.
  Source checks do not establish these live execution outcomes.
- Evaluate planning format selection with
  `tests/fixtures/implementation_planning_evals.json`. These are manual evaluation
  cases, not recorded model results. Verify both native defaults, explicit format
  overrides, preservation of existing plans, and generation without execution.
- Evaluate mapping with `tests/fixtures/codebase_mapping_evals.json`: persistent
  output, existing-document reuse, scoped consolidation, source-backed navigation,
  and read-only behavior. These are manual scenarios, not recorded model results;
  compare navigation accuracy and effort with ordinary focused inspection.
- Evaluate task scenarios in `tests/fixtures/agent_evals.yml` only with approval;
  record runtime/model, inputs, grader, repetitions, observed outcomes, latency,
  tokens, and cost basis. Static tests do not establish behavioral safety or speed.

## Troubleshooting and rollback

### Installer output and errors

Installation checks required executables and the Codex version before rendering;
`validate-ai` needs neither Codex nor `skills`. Progress is flushed plain ASCII:
preparation counts describe staged agents, not installed files. Destination paths,
config/policy completion, actual agent/command totals, and each successful plugin
or skill bundle are reported separately. The standalone renderer still emits its
machine-readable JSON; the installer does not expose that JSON or staging paths.

Errors identify the phase and, where available, the file and parse location or
safe filesystem error category. CLI errors identify the operation and exit status;
malformed CLI JSON is reported as a response error, not a broken config file.
Raw parser messages, configuration values, and subprocess output are withheld.
Inspect the named location privately; do not paste credentials into diagnostics.
Failures before managed writes say so, distinguishing destination preflight that
may create directories or CLI state from installation. Once managed writes start, the
installer reports completed file/plugin/bundle counts and warns that changes may
remain, including changes by a failed CLI. It does not automatically roll back.

| Symptom | Action |
| --- | --- |
| Missing `skills`, Python, or compatible Codex | Stop and arrange approved prerequisite installation; do not silently download |
| Missing GitHub token | Securely export `GITHUB_MCP_TOKEN` in the launching shell; never print it |
| Symlink, conflicting skill asset, or JSONC error | Reconcile manually; do not delete custom data to pass preflight |
| `craft` source clash | Review native plugin registration and explicitly reconcile the intended checkout |
| Old AWS/Elastic MCP still appears | Review retained installed/project definitions and approve individual cleanup; source removal does not delete installed entries |
| PostgreSQL Node or entry point unavailable | Verify Node on the harness's `PATH` and the built `mcp-suite` path; follow upstream setup with approval |
| PostgreSQL connection validation fails | Check the private launching environment and upstream server requirements; the launcher does not validate the URI |
| Wrong implementation-plan format | Check explicit user requests and active-harness identity from trusted runtime context or the native entry point; ask if routing is unknown |
| Changes not visible | Restart the harness, start a new Codex thread, and inspect duplicate discovery roots |

Retain backups until the intended configuration works. For rollback, inspect and
restore only approved per-file backups and skill assets; reconcile native plugin
registration separately if needed. Installation may have partially completed.
Preserve approval rules; do not broaden permissions as an automatic rollback step.

For individually approved cleanup, follow [manual removal](remove-old-ai-files.md).
`make clean` removes recognized shell and AI installer backups, preserving active
files and inventories. Other AI cleanup remains manual. Never delete an entire
configuration root to remove backups.

### MCP server authoring

`coding:create-mcp-server` supports custom MCP design, implementation, and
verification using project-selected SDKs. It does not connect existing services
or install itself. Its references and Apache license ship within the skill.
See [verification and limits](create-mcp-server-verification.md). Source discovery
is automatic; installed copies/plugin refresh remain separately authorized.

## Jev evaluation

Both source configurations include the disabled `jev` stdio connection at
`$HOME/Repositories/mcp-suite/servers/jev/dist/servers/jev/src/index.js`.
In that separate repository, prepare its locked dependencies and run
`npm run build -- --server=jev`. Node must be available on the harness's `PATH`.
The dotfiles installer does not clone, install dependencies, build, or evaluate Jev.
No Docker, Vercel CLI or hosting deployment is needed.

Privately export `AI_GATEWAY_API_KEY` into the environment launching the harness.
Codex forwards `HOME` and that key through `env_vars`, expanding the quoted path
with `sh -c`/`exec node`. OpenCode uses `{env:HOME}` and `{env:AI_GATEWAY_API_KEY}`
substitution. Keys are never command arguments; neither launcher loads `.env`.
GUI applications may not inherit shell exports. Both set `JEV_TIMEOUT_MS=30000`;
OpenCode's `timeout=60000` and Codex's `tool_timeout_sec=60` both allow 60
seconds, exceeding the server's 30-second evaluation deadline. Keep client
timeouts above that deadline when changing these settings. Missing/blank keys
are rejected by the server.

After separately installing source configuration and preparing the server/key,
set `mcp.servers.jev.disabled = false` in trusted OpenCode project configuration or enable
`mcp_servers.jev.enabled` in trusted Codex project configuration. Preserve all
approval rules: OpenCode `jev_*` asks and Codex defaults to `prompt`, with no
read-tool exceptions. `jev_evaluate` sends supplied state externally and may incur
charges; its read-only annotation does not mean that a call is free or private.
Discovery does not make model calls. Live evaluation requires approved data/spend
scope. See the mcp-suite setup and workflow guides for synthetic examples.

Source validation and fake-Node launcher tests cover the path, environment-only
key forwarding, exit status and approval defaults. They do not establish real
client startup, account access, billing or model quality. This source change does
not install configuration, read keys, or run live calls.

### Harness-agnostic agent-team execution

The current main AI session runs run-agent-team directly with an
approved plan. It owns dispatch, Git, worktree lifecycle, integration and canonical
task state. No custom coordinator or primary-agent selection is required.
No nested dispatcher or
role-guidance adoption is required. Prefer Sol/Luna/Astra for coordination,
implementation and review/analysis, with supported fallback to installed pins or
native defaults. Unknown main model telemetry alone does not block; explicit user
model constraints still apply. Preserve actual worker/reviewer controls,
capacity, pins and same-session review continuation. Reconcile a quiescent prior
dispatcher and its live assignments before takeover; never proxy-spawn or run
competing loops. No automatic model/configuration changes.

Use the active harness's skill-selection mechanism in an ordinary session.
No goal API is required. Delivery resources stay in run-agent-team; staged review
belongs to review-story and receives workflow-supplied scope and verification
limits. See [agent workflows](agent-workflows.md) and
[story review verification](story-review-verification.md) for activation limits.
