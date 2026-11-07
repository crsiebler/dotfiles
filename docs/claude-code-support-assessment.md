# Claude Code support assessment

Research date: 2026-10-20. Source baseline:
`c6c48a64e83697ddf079578a54ad5594bc525457` on `main`; the worktree was clean
before these planning documents. Implementation checklist: [PLAN.md](../PLAN.md).
Role and review references refreshed 2026-11-07 against
`9e79cd13d6dd9edfd6e5c6ffd4835036714530f1`.

Claude Code support is feasible without forking the 31 skills. The five Craft
bundles already have the appropriate skill directory structure. Marketplace
packaging is a small addition; preserving installation ownership, MCP approval
behavior, restricted agents, and delivery/review contracts is the larger job.

This assessment covers repository sources and official Claude documentation.
It is not an exhaustive security audit of every helper or specialist prompt.
Claude was not found on this session's PATH. No installed Claude configuration,
credentials, MCP connection, model, or native Claude workflow was inspected or
executed. No installer, test suite, dependency setup, or cleanup was run.
The existing Conda `dotfiles` interpreter was available for static inventory.

## Recommended architecture

Keep `ai/plugins/*/skills/` as the shared source. Add Claude-specific manifests
beside Codex manifests, with a separate root marketplace index. Keep personal
settings, MCP registrations, and generated user agents outside the skill plugins.
This lets someone install the marketplace without adopting personal permissions,
starting servers, or receiving the five canonical roles.

Proposed additions, not files created by this research:

```text
.claude-plugin/marketplace.json
ai/plugins/{coding,reporting,researching,delegating,producing}/
  .claude-plugin/plugin.json
  .codex-plugin/plugin.json                 # retained
  skills/                                  # shared
ai/claude/
  settings.json                            # source of owned setting entries
  mcp/global.json                          # GitHub, Exa, Context7 templates
  mcp/optional/*.json                       # explicit project opt-in templates
  commands/                                # selected Claude-native shortcuts
  hooks/                                   # only approved compatibility guards
scripts/install-claude.py                   # isolated Claude lifecycle adapter
```

Continue authoring roles in `ai/codex/agents/*.toml`; extend the renderer with a
Claude target. Install generated definitions in the selected Claude user root's
`agents/`. Do not move canonical roles or ship a second hand-maintained collection.

Add `make install-claude` and `install-ai.py claude` dispatch. Initially retain
the current `all`/`make install-ai` behavior for Codex and OpenCode; adding a new
harness must not silently enlarge existing installation grants. Do not add Claude
to the shell-install target. A Claude-only path should require Claude, not the
`skills` CLI used for existing managed-copy retirement.

## Marketplace and skill compatibility

Claude uses `.claude-plugin/marketplace.json`, with `name`, `owner`, and `plugins`.
For this repository each entry can use a relative string such as
`"source": "./ai/plugins/coding"`. The Codex index instead uses a local-source
object and Codex-specific policy/interface fields. Translate metadata rather
than copying that index. [Marketplace creation](https://code.claude.com/docs/en/plugin-marketplaces)

Relative paths resolve against the repository root. Register the directory or
Git repository, not a raw marketplace JSON URL that lacks the sibling plugin
files. [Marketplace source reference](https://code.claude.com/docs/en/plugins/marketplace-reference)

Each plugin should have an explicit Claude manifest carrying its existing name,
version, description and author metadata. Claude loads `skills/` at the plugin
root; scripts and references remain inside their existing bundles. Avoid
out-of-plugin symlinks or resource paths. Plugin-root substitutions in Markdown
are not a promise that the variable exists in an arbitrary Bash subprocess.
[Plugin manifest reference](https://code.claude.com/docs/en/plugins-reference)

Claude recognizes the Agent Skills layout and supports plugin-qualified skill
invocation, for example `/coding:develop-code`. Keep the portable frontmatter
minimal. Add Claude-only invocation/tool settings only where their semantics
are needed and tested; an `allowed-tools` declaration can change permissions.
[Skills documentation](https://code.claude.com/docs/en/skills)

The inventory below accounts for all 31 skills. “Reusable” means a source-level
assessment, not a successful Claude runtime test.

| Skills | Assessment and required work |
| --- | --- |
| `develop-code`, `review-code`, `format-code`, `run-tests`, `map-codebase` | Reusable workflows. Verify Claude activation, scope boundaries, and project-native tool selection. |
| `manage-changes`, `resolve-review-feedback` | Reusable with available Git/gh or MCP tools. Exercise exact write previews and retained authorization; tool names must come from discovery. |
| `write-requirements`, `prepare-implementation` | Add an explicit trusted Claude routing case, recommending Markdown `PLAN.md`. Current planning defaults cover Codex/OpenCode and otherwise ask. Keep planning independent of execution. |
| `run-agent-team` | Conditional. Add a Claude capability reference only after native worker, reviewer, worktree and continuation behavior is demonstrated. Existing GPT model preferences already permit supported inheritance; do not translate them to invented Claude equivalents. |
| `archive-run` | Reusable Python/Git/POSIX helper. Its reference explicitly defines `CodexGoalMarkdown` as a format identifier independent of harness. Preserve schema names and existing evidence checks. |
| `create-skill`, `create-mcp-server` | Portable authoring is reusable. Optional upstream Claude evaluation adapters were deliberately omitted from `create-skill`; do not reinstall them merely to add Claude support. |
| `verify-interface` | Reusable with one available browser backend. Browser/tool installation and connection remain separate. OpenCode browser registrations do not expose Claude tools automatically. |
| `assess-work-item`, `report-progress`, `report-project-status` | Reusable evidence/communication workflows once their selected GitHub/Jira adapter is available. Drafting does not authorize posting. |
| `search-web` | Reusable through exposed Claude research tools or configured Exa. Preserve conditional provider guidance. |
| `read-docx`, `read-pptx`, `read-xlsx`, `read-pdf` | Reusable bundled Python readers with existing dependencies and extraction limits. Verify execution from an installed bundle. |
| `create-docx`, `create-pptx`, `create-xlsx`, `create-pdf`, `create-gif` | Reusable Python helpers. Keep output in the active project and preserve rendering, fonts, recalculation and visual-inspection limitations. |
| `create-audio` | Reusable CLI/backend separation. Existing Apple Silicon MLX runtime, weights and request files remain prerequisites; Claude installation provisions none of them. |
| `create-sprites` | Planning and supplied-asset integration are viable. The documented `gpt_imagegen` backend is explicitly OpenCode-only; generation needs a separately chosen, authorized and verified adapter. |
| `use-subagents` | Extend helper `--harness` choices and root lookup for Claude. Current implementation supports only Codex/OpenCode. Keep static discovery distinct from callable native roles. |

Source evidence: [skill dependency inventory](skill-dependencies.md),
[planning skill](../ai/plugins/coding/skills/prepare-implementation/SKILL.md),
[discovery helper](../ai/plugins/delegating/skills/use-subagents/scripts/subagents.py),
[sprite boundary](../ai/plugins/producing/skills/create-sprites/SKILL.md),
[Claude evaluation adapter limits](../ai/plugins/coding/skills/create-skill/references/claude-adapters.md),
and [archival format contract](../ai/plugins/coding/skills/archive-run/references/completed-run-archive.md).

## Configuration and policy

The current installer supports `all`, `codex`, `opencode`, and `validate` only.
It replaces the explicitly managed Codex/OpenCode configuration files byte for
byte, backs up changed files, validates destinations, renders roles, and reconciles
owned retired assets. Reuse those safeguards, not its two-target assumptions.
[Installer](../scripts/install-ai.py)

Claude separates user/project settings from local/user MCP state. Default settings
live in `~/.claude/settings.json`; local/project settings have different scopes.
Arrays can merge across settings layers, so validation must examine effective
permissions as well as a generated fragment.
[Settings and precedence](https://code.claude.com/docs/en/settings)

Recommended ownership decisions:

- Preserve `ai/AGENTS.md` as the single personal-policy source and install its
  exact bytes as Claude's user-level `CLAUDE.md`.
- Reconcile only explicitly owned Claude settings entries. Preserve unrelated
  keys, user restrictions, other hooks and CLI-managed plugin state. Record
  previous owned values and stop on conflicting edits. This is a documented
  Claude-specific ownership policy, not a change to Codex/OpenCode replacement.
- Use native commands for scoped MCP/plugin registration. Do not replace
  `~/.claude.json` or hand-edit native plugin catalogs/caches. Preview targets,
  protect backups, and verify unrelated state survives.
- Respect an absolute `CLAUDE_CONFIG_DIR`; verify actual native state paths in an
  isolated fixture rather than assuming every file lives inside that directory.
  [Configuration directory](https://code.claude.com/docs/en/env-vars)
- Leave model selection inherited/user-selected. Existing GPT profiles and the
  OpenCode Bonsai provider are not portable model configuration. Anthropic does
  not support routing Claude Code to non-Claude models through a gateway.
  [Gateway support](https://code.claude.com/docs/en/llm-gateway)

Current Claude can read project `AGENTS.md` starting with v2.1.277, but default
loading changes when an ancestor/project `CLAUDE.md` or `CLAUDE.local.md` exists.
For this repository, propose a small root `CLAUDE.md` containing `@AGENTS.md` for
predictable compatibility, without duplicating policy. Test instruction loading
and nested instructions. Do not add import hooks or run `/init` over the policy.
[Instruction loading](https://code.claude.com/docs/en/memory)

The Codex `workspace-write` sandbox is not a settings value Claude can inherit.
Claude's Bash sandbox does not also sandbox file tools, hooks or MCP servers.
Specify and test shell permissions, filesystem/network boundaries and MCP approval
separately. Do not claim cross-harness sandbox equivalence.
[Sandbox scope](https://code.claude.com/docs/en/sandboxing)

## MCP inventory and migration

The checked-in configurations contain eight Codex connections and twelve OpenCode
connections. Only GitHub, Exa and Context7 are enabled globally. These are client
definitions; the project does not contain most server implementations. In
particular, PostgreSQL and Jev point to a separate built `mcp-suite` checkout.
[Codex definitions](../ai/codex/config.toml),
[OpenCode definitions](../ai/opencode/opencode.json),
[independent contract fixtures](../tests/mcp_configuration_test.py).

| Server | Claude transport/configuration recommendation | Retained scope and permission intent |
| --- | --- | --- |
| GitHub | HTTP; existing URL/toolsets; `GITHUB_MCP_TOKEN` reference in Authorization header | User registration; exact read exceptions, all other tools ask |
| Exa | HTTP; existing four-tool endpoint; `EXA_API_KEY` reference | User registration; four approved research tools only |
| Context7 | HTTP; existing endpoint; `CONTEXT7_API_KEY` header reference | User registration; two approved research tools only |
| Vercel | HTTP; existing endpoint; separately configured OAuth | Explicit trusted-project opt-in; every tool asks |
| Jira / Rovo | HTTP; retain logical name `jira` and v2 endpoint | Project opt-in; retain exact read names; writes/new tools ask |
| PostgreSQL | stdio `node`; existing built entry point and `POSTGRESQL_CONNECTION_STRING` reference | Project opt-in; only safety-status read exempt; `execute_query` always asks |
| Jev | stdio `node`; existing built entry point, `AI_GATEWAY_API_KEY`, `JEV_TIMEOUT_MS=30000` | Project opt-in; every call asks; verify client timeout separately |
| Docker gateway | stdio `docker mcp gateway run` | Project opt-in after separate profile/lifecycle authorization; every tool asks |
| Chrome DevTools | Existing Node package through stdio if separately provisioned | Optional project template; preserve OpenCode's enabled-server allow intent only with explicit activation scope |
| Playwright | Existing Node package through stdio if separately provisioned | Same opt-in boundary; do not run downloading `npx` as a validation step |
| Jam | HTTP; existing endpoint | Optional project template; document existing enabled-server allow intent |
| ElevenLabs | stdio `uvx elevenlabs-mcp`; existing key reference and file output setting | Project opt-in; every call asks; no implicit dependency download |

Keep AWS and Elastic absent. Do not activate optional servers just because the
templates exist. Docker is in current source even though some high-level prose
lists fewer optional connections; use the executable definitions and tests.

Claude supports HTTP/stdio definitions and `${VAR}` expansion in MCP configuration.
Local/user MCP registrations normally live in `~/.claude.json`; shared project
registrations use `.mcp.json`. Plugin-bundled servers receive different tool
names. Keep personal connections outside the five skill plugins to preserve
logical names and independent activation. Project MCP approval is not a reliable
opt-in gate for noninteractive runs, so leave optional templates unregistered
until authorized. [MCP configuration](https://code.claude.com/docs/en/mcp)

Never expand secrets into generated files, shell arguments or logs. Validate
required variable presence without printing values; use fake values in fixtures.
Do not source personal environment files during installation checks. Translating
the client definitions does not establish server compatibility or authentication.

### Permission translation is the main correctness risk

OpenCode's current tests implement last-matching-rule semantics. Claude evaluates
deny before ask before allow; a specific read allow does not override a broader
ask/deny. Therefore copying `github_*: ask` plus read exceptions loses those
exceptions, and copying Exa's deny-all plus narrow allows blocks research too.
[Claude permissions](https://code.claude.com/docs/en/permissions),
[existing permission tests](../tests/mcp_permissions_test.py).

Proposed behavior is exact read allows plus a small Claude-specific guard that
leaves approved reads to normal permission evaluation, asks for unknown/write
tools on mixed servers, and denies unlisted Exa/Context7 tools. Servers that always
ask can use server-wide ask rules. The guard must never override stricter user or
managed decisions. Do not approximate the contract with a broad MCP allow.

This is a proposed authorization-control addition, not authorized implementation
under the current prohibition on modifying authorization logic. Resolve that
policy boundary explicitly before implementing it; otherwise keep the affected
MCP migration blocked rather than silently relax its behavior.

If approved, require failure to block the call for missing, crashed, malformed or
timed-out guards. Current documentation provides `onFailure: "block"` starting
with v2.1.295. Treat that as a candidate minimum for guarded integration, subject
to native verification. Never label an untested hook fail-closed.
[Hook failure behavior](https://code.claude.com/docs/en/hooks)

## Agents and execution workflows

The maintained canonical TOML collection has five roles: `researcher`, `planner`,
`reviewer`, `auditor` and `operator`. All omit model/provider/effort pins.
Only `auditor` has `sandbox_mode = "read-only"`. It prohibits tests, builds,
active scans, edits, operational changes, delegation and external posts.
The other four roles inherit runtime permissions. The generic `reviewer` preserves
its candidate and may perform authorized focused verification. Explicit inspection-only
requests prohibit tests, builds and browser actions.
[Native role contract](agent-authoring.md)

Extend [render-agents.py](../scripts/render-agents.py) deliberately: preserve role
text, validate Claude names/frontmatter, inherit model selection, reject unknown
or nonportable fields, and retain atomic per-file writes and collision checks.
Reject unsupported future Codex model/sandbox fields. Start the Claude
`auditor` with only Read/Grep/Glob and document the difference from Codex's
read-only shell inspection. Preserve the other roles' supported runtime
inheritance and each role's task boundaries.

Claude supports tool allowlists on subagents; denying Write/Edit alone still
leaves Bash and MCP routes. Plugin agents also ignore several control fields,
including `permissionMode` and hooks, which favors user-agent installation for
this collection. Custom agents can resume with retained history; current docs
describe `SendMessage`, not an assumption about an old `Agent(resume=...)` API.
[Subagent contracts](https://code.claude.com/docs/en/sub-agents)

For independent staged review, supply the generic `reviewer` with the complete
discovered `review-story` contract, candidate identity, verification scope and
pass/session budgets. Use native role selection when supported. Otherwise supply
the complete discovered reviewer instructions and review contract to a fresh
independent generic agent and record that binding. Qualify permitted evidence
access and same-session targeted continuation before advertising Claude team
delivery. Assess any new guard against the authorization-policy boundary above.

Routine stories use focused checks and lightweight staged self-review.
High-risk stories and explicit early gates receive independent staged review.
One independent review of the integrated candidate gates final local delivery
or shipping. Preserve the workflow's candidate/base/scope evidence, review
budgets and blockers.
[Team delivery contract](../ai/plugins/coding/skills/run-agent-team/SKILL.md)

Prefer ordinary native subagents for the existing main-session dispatcher model.
Claude agent teams remain experimental and disabled by default, with resumption
and coordination limitations; they are not required for marketplace support.
[Agent teams](https://code.claude.com/docs/en/agent-teams)

Keep the single native OpenCode role, `sprite-artist`, OpenCode-only. The main
session owns dispatch, integration and canonical state. Preserve the workflow's
bounded `memory.json`, append-only `progress.md`, review budgets and resumption
rules when qualifying native Claude execution.

## Scripts, commands and other tools

| Component | Assessment / proposed action |
| --- | --- |
| `scripts/install-ai.py` | Add explicit Claude dispatch/validation; isolate native CLI parsing and state ownership in a Claude adapter. Existing installs must remain unchanged. |
| `scripts/render-agents.py` | Add third target and independent native field tests; do not weaken existing rejection behavior. |
| `scripts/ai_retirement.py` | Existing plugin lifecycle is Codex-specific. Add separate Claude ownership records; do not reuse its Codex CLI/schema assumptions or retire shared skills on Claude-only install. |
| `scripts/clean-install-backups.py` | Recognize only verified Claude installer backup patterns. Preserve active state, native caches, conversations, credentials and custom backups. Add preview coverage before enabling removals. |
| Bundled `subagents` / `subagents.py` | Add explicit Claude global/project discovery. Resolve root overrides and duplicates. Do not scrape plugin caches as a proxy for live role discovery. |
| Document/GIF/audio/skill/archive helpers | Retain implementations and dependency ownership. Test resource access from installed/cached layouts with outputs in project fixtures. No framework rewrite is indicated. |
| `/define-requirements`, `/plan-work`, `/ship`, `/find-agents` | Provide thin Claude shortcuts if preserving this interface is desired. Claude plan-work should choose Markdown; find-agents uses the Claude discovery target. Translate positional arguments deliberately. |
| `/review-pr` | Canonical contract remains `ai/opencode/commands/review-pr.md`. A Claude adapter must preserve exact-payload approval and finding schema. Generate from the canonical contract or package its content deliberately; never introduce an untracked second authority. Rewrite/verify shell expansion and argument handling for Claude. |
| `/create-audio`, `/create-sprite` | Prefer namespaced shared skills where sufficient. Preserve sprite provider limits and the OpenCode-only sprite role boundary. Translate native role metadata deliberately. |
| OpenCode notifier | JavaScript plugin/config is not a Claude plugin. Optional Claude Notification/Stop hooks can reproduce selected events later; preserve privacy and avoid permission auto-approval or restart loops. |
| OpenCode `opencode-gpt-imagegen` | Not directly portable. A separately supported image backend and its billing/consent contract are needed for Claude sprite generation. |
| `lsp: true`, `tui.json` | OpenCode UI/LSP configuration is not transferable. Configure Claude equivalents only for a demonstrated requirement; no blanket translation. |
| `scripts/install-zsh-extensions.py`, `scripts/sync-env.py`, Zsh/aliases/Git setup | No core Claude changes needed. Keep shell installation, environment synchronization, global Git and sudo separate from AI support. |
| `mlx-bonsai`, GPT profile files | Retain for their existing runtimes. No local-model service restart, model download or gateway conversion belongs to this plan. |

## Delivery boundaries and effort

Recommended milestones:

1. Marketplace compatibility: five packages, 31 discoverable skills, portable
   resource loading, explicit unsupported-capability messages.
2. Personal integration: separately authorized installer, policy/settings, MCP
   contracts, agent rendering/discovery, selected command adapters and rollback.
3. Workflow qualification: demonstrated Claude staged review and team delivery;
   otherwise leave that capability explicitly unavailable.

Planning estimate for one engineer familiar with the project: 1–2 working days
for marketplace packaging/validation; another 5–9 for personal integration and
fixtures; another 3–6 for native review/team qualification. These are estimates,
not measurements. CLI availability, authorization-control design, authentication,
and live evaluation scheduling can extend elapsed time. Sprite generation and
notifier parity are optional follow-ups, not included in those estimates.

The [plan](../PLAN.md) assigns integrated acceptance, regression coverage and
explicit dependencies. Current research establishes source feasibility only.
Settings-reference retrieval was unavailable through the browser tool; the
settings/scoping, MCP, permission and feature-specific pages were accessible.
Select and record an actual Claude release during implementation, check its CLI
and schemas, and record observed behavior before claiming supported integration.
