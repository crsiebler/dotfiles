# dotfiles

A collection of configuration files for storing user preferences and preserving the state of a utility. Support for Zsh only.

## Setup and documentation

- [Repository overview and source map](docs/overview.md)
- [AI configuration, connections, and validation](docs/ai-configuration.md)
- [Manual removal of old AI files](docs/remove-old-ai-files.md)
- [Native agent authoring and rendering](docs/agent-authoring.md)
- [Agent workflows and staged review](docs/agent-workflows.md)
- [Repository contributor instructions](AGENTS.md)

### Requirements

- Shell setup: Zsh, Oh My Zsh, standard Unix tools, and `python3` for environment synchronization.
- AI installer: Python 3.11+ (`PYTHON` defaults to `python3.11`).
- Codex installation: a CLI supporting native local plugin marketplaces,
  plugin add/list/remove, and the listing flags used by the installer.
  Prerequisites check capabilities rather than pinning a release number.
- AI installation/skill retirement: the `skills` CLI already on `PATH`; retirement
  requires tested version 1.5.24. OpenCode 2.x or newer is required before
  installing its native V2 configuration; the installer does not upgrade it.
- Source validation and agent rendering: Python 3.11+. Archival requires POSIX file locks and Git.

The AI installer does not download missing tools. If `skills` is missing, arrange
an explicitly approved installation; there is no silent `npx` fallback.

### Choose an installation scope

Run validation from this checkout without credentials. Before choosing one of the
installation targets, review the [installation guide](docs/ai-configuration.md#installation-and-replacement-behavior),
authorize installation, and securely export the required `GITHUB_MCP_TOKEN`:

```sh
make validate-ai       # Local source validation only; no harness or MCP starts
make install-codex     # Codex configuration, local plugins, native roles
make install-opencode  # OpenCode configuration, copied skills, agents, commands
make install-ai        # Both AI harnesses; no shell/env/git setup or binaries
make preview-ai-cleanup # Read-only retirement preview; AI_TARGET=opencode or codex
```

The five checkout-local `craft` plugins are `coding`, `reporting`, `researching`,
`delegating`, and `producing`. Skill ownership is:

| Purpose | Plugin and skills |
| --- | --- |
| Creative assets and document files | `producing`: `create-audio`, `create-sprites`, `create-gif`, `create-docx`, `create-pptx`, `create-xlsx`, `create-pdf` |
| Skill and MCP server authoring | `coding`: `create-skill`, `create-mcp-server`, alongside the existing development workflows |
| Research and document evidence | `researching`: `search-web`, `read-docx`, `read-pptx`, `read-xlsx`, `read-pdf` |
| Report content and communication | `reporting`: existing assessment/progress/status workflows |

Use a native tool when it adequately handles a simple document read. Production
skills create files; researching extracts evidence; reporting owns synthesis and
communication. Each new skill has its own Python requirements and validation guide.

All 47 Craft skills link to a bundled `references/requirements.md` describing
required/optional utilities, installation steps, and availability checks.
See the [skill dependency audit and inventory](docs/skill-dependencies.md).
Source updates require an authorized plugin refresh or skill installation before
agents discover them.

Dependency setup is separately authorized and is never part of AI installation.
See [verification and tested runtimes](docs/document-skill-verification.md) and
[coordinated activation](docs/ai-configuration.md#producing-and-document-skill-activation).
`search-web` retains conditional Exa MCP guidance.
`create-mcp-server` adapts the Apache-2.0 mcp-builder guidance for project-scoped
MCP development. It is instruction-only; see [verification](docs/create-mcp-server-verification.md).
The single harness-agnostic personal policy, [`ai/AGENTS.md`](ai/AGENTS.md), is
copied byte-for-byte to both user-level `AGENTS.md` destinations. Root
[`AGENTS.md`](AGENTS.md) remains separate, repository-only guidance.
GitHub, Exa, and Context7 are globally enabled; Vercel, Jira/Rovo, PostgreSQL, and Jev remain off.
AWS and Elastic MCP definitions are intentionally absent from both source configs.
See the guide for credentials, project opt-in, profiles, and replacement behavior.
AI installation replaces managed JSON/TOML files exactly from the repository,
including Codex configuration and OpenCode companion files. Installed-only settings
are removed; move desired settings into the sources first. Changed files receive
timestamped backups. Verify installed files, retain backups for rollback, and
run `make clean` when installer backups are no longer needed.

For the broader shell setup, `make install` first checks the OpenCode V2 and
`skills` CLI prerequisites, before any installation steps (including with `-j`).
It then installs missing custom Zsh plugins and the configured theme, copies shell/alias files, creates or
synchronizes `$HOME/.env`, sets the global Git excludes file, calls
`install-opencode`. It does **not** install Codex
or a global `subagents`, and never upgrades the OpenCode binary. Run
`make check-install-prerequisites` to check CLI prerequisites alone. This is not
the full AI source/destination/conflict preflight: later failures can still occur
after shell/env/git changes. Not every overwritten shell
file or binary is backed up.

### Custom Zsh plugins and theme

With Oh My Zsh already installed, `make install` clones these missing extensions
from their verified upstream repositories before replacing `.zshrc`:

| Extension | Repository |
| --- | --- |
| `opencode` | [crsiebler/omz-plugin-opencode](https://github.com/crsiebler/omz-plugin-opencode) |
| `gh` | [crsiebler/omz-plugin-gh](https://github.com/crsiebler/omz-plugin-gh) |
| `bun` | [ntnyq/omz-plugin-bun](https://github.com/ntnyq/omz-plugin-bun) |
| `you-should-use` | [MichaelAquilina/zsh-you-should-use](https://github.com/MichaelAquilina/zsh-you-should-use) |
| `zsh-autosuggestions` | [zsh-users/zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions) |
| `zsh-syntax-highlighting` | [zsh-users/zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting) |
| Powerlevel10k | [romkatv/powerlevel10k](https://github.com/romkatv/powerlevel10k) |

To install only these extensions, without shell copies or AI installation:

```sh
make PYTHON=python3 install-zsh-extensions
```

The installer respects exported `ZSH` and `ZSH_CUSTOM`; defaults are
`$HOME/.oh-my-zsh` and `$ZSH/custom`. Keep any custom values exported when starting
new shells too. Git and network access are required for missing extensions.
Fresh clones use the upstream default branch; subsequent installs never pull,
reset, or replace existing extensions, including custom non-Git copies. Existing
entry files must be readable; invalid directories or symlinks stop installation
for manual reconciliation. Failed clones are not installed; completed extensions
remain if a later one fails. Existing origins are not changed or required to match.

This does not install Oh My Zsh itself or the `opencode`, `gh`, `bun`, or Railway
applications. Railway configuration is left untouched. The AI-only targets do
not install Zsh extensions. Review existing copies and retain any needed backups
before separately approved manual updates or removal; `make clean` does not touch
plugins or themes. Open a new terminal after installation to load the extensions.

For a new environment, copy `env/.env.example` to `$HOME/.env` only if that file
does not already exist, then fill in values privately. For existing environments,
merge missing keys without overwriting secrets. Load the exports in the shell
launching the installer and harness; AI-only targets do not source or sync `.env`.
After shell installation, open a new terminal or run `source ~/.zshrc`.
After AI installation, restart the harness and start a new Codex thread.

## Related Project

[mcp-suite](https://github.com/crsiebler/mcp-suite) supplies the custom local Node
PostgreSQL MCP server referenced by both harness configurations at
`$HOME/Repositories/mcp-suite/servers/postgresql/dist/servers/postgresql/src/index.js`.
It is disabled by default and requires trusted project opt-in plus a privately
exported `POSTGRESQL_CONNECTION_STRING`. Follow the upstream setup documentation
to prepare Node and the built server; the dotfiles installer does not clone,
build, or install `mcp-suite`. See the [connection guide](docs/ai-configuration.md#trusted-project-opt-in)
for transport details and server-validation responsibilities.

The local Jev MCP uses
`$HOME/Repositories/mcp-suite/servers/jev/dist/servers/jev/src/index.js` and
`AI_GATEWAY_API_KEY`. It is disabled by default and prompts for every evaluation,
which sends supplied data through Vercel AI Gateway and may incur charges.
Build it in `mcp-suite` before project opt-in; see the
[Jev connection guide](docs/ai-configuration.md#jev-evaluation).

## OpenCode PR Review Command

This repository includes a manual `/review-pr` OpenCode command that reviews GitHub pull requests using OpenCode's configured provider/model layer. It does not make direct OpenAI API calls.

### Setup

After running `make install-opencode` (also included in `make install`):

- `/review-pr` command: `~/.config/opencode/commands/review-pr.md`

### Requirements

- OpenCode configured with a working provider/model
- GitHub CLI (`gh`) authenticated separately; inspect installed help for the
  login flow and verify with `gh auth status`. The command's `gh` path does not
  require a token environment variable, but the globally enabled GitHub MCP
  separately requires `GITHUB_MCP_TOKEN` during AI installation and at runtime.
- A git branch with an associated GitHub pull request, or an explicit PR selector

### Usage

```bash
# Detect the PR for the current branch
/review-pr

# Review a specific PR number
/review-pr 123

# Review a specific PR URL
/review-pr https://github.com/owner/repo/pull/123

# Prepare a review for posting after explicit confirmation
/review-pr --post
```

By default, `/review-pr` generates a local review report only. When `--post` is provided, it previews the PR URL, review event, consolidated body, inline comment count, and exact `gh` command or API payload, then requires explicit confirmation before posting anything to GitHub.

## Local Coding Model

Bonsai 2 MLX is the sole configured local coding provider. See the
[setup and verification guide](docs/local-bonsai.md) for the isolated runtime,
64K starting context and `mlx-bonsai` Zsh shortcut. Select the base configuration's
Bonsai provider through OpenCode's `/models` menu; no extra profile is required.
Provisioning is separate from
dotfiles installation. For cleanup, inspect exact old model paths, stop their
users, remove only selected coding caches, and retain rollback configuration
until verification. Preserve audio weights and shared environments.

## Audio Generation

Agents use the shared `create-audio` skill and its bundled `create_audio.py`
entry point. OpenCode also exposes `/create-audio` to load the skill. There is
no shell alias or audio chat-provider entry. The first backend implements Stable
Audio 3 Small-SFX through MLX on Apple Silicon; backend-specific validation and
execution are separate from request data, artifact storage, and orchestration.
Generation preferences and prompts come from a project-owned JSON request.
Stable Audio models default to `~/Models/local-audio/`; no game-specific directory or
prompt is built into the tool. This is a file-generating runtime, not an MLX-LM
chat-model entry.

See the [audio request and setup guide](ai/plugins/producing/skills/create-audio/references/local-audio.md).
AI installation copies the skill but does not provision models.
Setup is separate and can copy verified existing weights into a fresh
generic runtime without changing the original installation. Use the existing
sprite skill and this audio skill from project adapters while keeping artistic
direction, output policies, and engine integration in the project.

## Sprite Generation

This repository includes a `/create-sprite` OpenCode command for generating
pixel-art sprite sheets through an optional OpenCode V2 image API plugin and integrating approved
assets into projects when requested, including Godot 4. Asset-only work needs
neither a Godot project nor binary; Godot guidance is loaded only for Godot
requests or relevant project context.

The workflow installs:

- `sprite-artist`, the specialized generation and integration agent
- `create-sprites`, the reusable asset planning and prompt skill
- `/create-sprite`, the command entry point

### Requirements

The portable skill can use an actually available native image-generation tool;
inspect its schema rather than infer availability from the harness name. The
OpenCode command uses an explicitly configured V2 image provider.
[opencode-img@0.2.0](https://github.com/mattsafaii/opencode-img) uses the V2
plugin API and exposes `gpt_imagegen`. It requires a provider API key with
separate API billing; ChatGPT subscription access is insufficient. It is
documented as an option and is not enabled or installed by this change.
Compatibility was assessed from source, without a live image request.

Existing batch authorization carries forward within its provider, cost, and call
limits. Ask only for missing scope or additional spending; plan-only requests
generate nothing and change no files. See [workflow approval scope](docs/agent-workflows.md#approval-scope-across-workflows)
for continuation, reviewer verification, and posting boundaries.

Godot 4 and an active `project.godot` are required only for Godot integration.
Asset-only generation and planning do not require Godot.

See [OpenCode V2 configuration](docs/opencode-v2.md) for native settings,
built-in notifications, optional plugin setup, and activation checks.

### Usage

```text
/create-sprite create a four-direction forest ranger with idle and walk animations

/create-sprite create a side-view lightning knight with idle, run, attack, hurt, and death animations

/create-sprite --plan-only create a six-frame fire elemental boss idle
```

The agent previews its asset contract and planned image calls before invoking
`gpt_imagegen`. Generated images and references must remain inside the active
workspace. The `--plan-only` option produces prompts and an integration plan
without generating images or changing project files.

## Coding plans and review

An explicit request to implement an approved plan includes its initial and
subsequent scoped local commits without repeated approval prompts. Planning alone
and explicit no-commit/source-only instructions do not. Checks, review and
unrelated-work safeguards remain; pushes, installation and destructive actions
need their own applicable scope. See [commit authority](docs/agent-workflows.md#plan-launch-and-local-commits).

Use ordinary Codex or OpenCode sessions; /goal is optional. Planning defaults
to PLAN.md in both harnesses. develop-code handles ordinary implementation;
invoke run-agent-team explicitly for approved parallel plan execution.

prepare-implementation plans autonomous PRD implementation with automated checks,
independent agent review and scoped local delivery. It adds no manual test or
deployment verification gates; deployment checks require explicit scope and an
automatable path. It resolves applicable human approval gates and manual
prerequisites before marking a plan ready for unattended execution. Existing
grants carry forward; unresolved steps, required future-result approvals, or
mandatory runtime prompts block readiness. The plan records the evidence, and
execution rechecks it before implementation. See [unattended readiness](docs/agent-workflows.md#unattended-execution-readiness).

write-requirements uses the same automation-compatible acceptance in PRDs.
run-agent-team carries that scope through worker packets, automated checks,
bounded review and closeout without adding human test confirmation or release
gates. Unattended execution uses the existing main session, not a separate runner.

The generic reviewer combines assessment and authorized focused verification.
review-story supplies the staged-story contract and JSON schema; the workflow
supplies candidate identity, acceptance, verification scope and budgets. Explicit
inspection-only requests stay inspection-only. The reviewer never edits fixes or
commits. One initial and at most one targeted pass retain session identity and
blocker history. See [agent workflows](docs/agent-workflows.md).

Completed plans use archive-run for verified enrolled archival or copy-only
preservation under actual authority. New manifests use MarkdownPlan; historical
Markdown evidence retains its original provenance. Source retirement does not
remove installed files or historical project data. See the
[cleanup inventory](docs/remove-old-ai-files.md#retired-runner-and-story-role).

## Native agents and discovery

Five custom roles cover evidence gathering, planning, independent review,
inspection-only auditing and authorized operations: researcher, planner, reviewer,
auditor and operator. Implementation uses the main session or native execution
agents with matching skills and a supplied task contract.
The main session coordinates; these are not mandatory pipeline stages.
Specialized knowledge lives in conditional skills across the existing five
plugins. See [role selection](ai/plugins/delegating/skills/use-subagents/references/core-roles.md).

The canonical collection contains **5 TOML roles**, copied unchanged to Codex
and rendered generically for OpenCode. The minimal OpenCode sprite-artist adapter
preserves image-provider approval settings, bringing OpenCode to **6 definitions**.
Only auditor retains read-only metadata. Reviewer can perform authorized focused
verification while preserving the candidate. See [agent authoring](docs/agent-authoring.md).

Use native delegation to invoke agents; reading a definition is not delegation.
OpenCode `/find-agents` loads `use-subagents` for discovery; the skill bundles
the unchanged `subagents` helper. `/ship` loads `manage-changes` to prepare the
requested Git commit, branch push and GitHub PR sequence, with exact previews and
one explicit approval for the bounded sequence. It never merges implicitly.
`assess-work-item` reads GitHub issues and Projects through adequate exposed tools
or installed gh, including scoped item/field evidence and pagination gaps; its
default result is a draft. `/review-pr` remains the review command.
From this checkout:

```sh
helper=ai/plugins/delegating/skills/use-subagents/scripts/subagents
sh "$helper" --harness opencode list
sh "$helper" --harness opencode search security
sh "$helper" --harness opencode fetch reviewer
sh "$helper" help
```

`develop-code` unifies feature work, diagnosis/fixes and refactoring;
`review-code` independently handles assessment and authorized verification through four scopes and nine
conditional lenses. Adopt the [project guidance template](docs/templates/code-repository-AGENTS.md)
by merging verified local facts. See [source verification and evaluation limits](docs/coding-workflow-verification.md).

`resolve-review-feedback` combines feedback assessment and verified resolution
preparation. Analysis-only requests stop at findings; GitHub operations follow
its bundled reference and exact-preview approval protocol.

## Removing backup files

OpenCode V2 uses `cli.json` for its terminal theme and built-in notifications.
Cleanup recognizes its timestamped backups and legacy `tui.json`/notifier
backups, while preserving all active files. After verifying V2, review active
legacy files separately using [manual removal](docs/remove-old-ai-files.md#opencode-v2-legacy-settings).

AI installation now reconciles verified retired repository-owned skills after
installing replacements. Codex keeps native `craft` plugins and their Desktop
presentation; OpenCode uses the `skills` CLI. See [automatic retirement](docs/remove-old-ai-files.md#automatic-managed-retirement)
for ownership, shared-directory scope, and preserved conflicts.

1. Verify the installed configuration and copy any backups needed for rollback
   outside the cleanup locations before running `make clean`.
2. Review the generated backups: `$HOME/.zshrc.backup.<timestamp>`, adjacent
   timestamped AI configuration/agent/command backups, timestamped skill and
   retirement archives under `.install-ai-backups/`, and hashed plugin source
   snapshots under `.install-ai-backups/plugin-sources/`.
3. Run `make clean` to remove these installer backups for both OpenCode and Codex.
   It honors `CODEX_HOME` and `XDG_CONFIG_HOME`, defaulting to `~/.codex` and
   `~/.config/opencode`. This includes backups from the separate AI install targets.
   Active configurations, agents, commands, skills, plugin caches, installation
   inventories, unrelated legacy state, and legacy `.env` backups remain untouched. Invalid
   root paths are rejected before deletion; symlink roots are rejected and symlink
   backup candidates are skipped. Cleanup does not follow symlinks inside archives.
4. Cleanup matches installer names and timestamp/hash formats, not every file
   containing `backup`. Unknown backup names and unrelated files remain for manual
   review under the [manual removal guide](docs/remove-old-ai-files.md).
   Never delete a whole configuration root to remove backups.
5. Separately review the obsolete installed command and sprite-agent paths listed
   in that guide. Renames install no compatibility aliases or automatic cleanup;
   inventory retired installed assets separately and preserve project artifacts.
6. Review retained installed AWS/Elastic MCP entries and old PostgreSQL Docker
   fields separately. Back up customizations and approve exact config edits before
   removal; preserve approval rules, active `POSTGRESQL_CONNECTION_STRING`, and
    exports still used elsewhere. Source removal does not delete installed entries.
7. For `use-exa` renamed to `search-web`, verify the replacement after authorized
   installation or Codex native plugin refresh, preserve customized old copies,
   and approve exact paths before manual cleanup. Restart the harness and start
   a new Codex thread; follow the [rename steps](docs/remove-old-ai-files.md#renamed-web-research-skill).

8. For the producing/document rollout, preserve customized media/document copies,
   refresh `coding`, `researching`, and `producing` together through separately
   authorized native Codex installation/refresh or OpenCode skill copies, then
   restart and verify unique discovery in a new Codex task. Media skill names stay
   unchanged; do not delete active same-named OpenCode copies. Review exact obsolete
   paths separately under the [rollout cleanup steps](docs/remove-old-ai-files.md#producing-and-document-rollout).
   Never delete plugin caches manually or discard backups before verification.

9. For the combined `resolve-review-feedback` skill, preserve customized copies,
    separately authorize coding plugin refresh or OpenCode installation, restart,
    and verify the combined workflow. Installation automatically archives/removes
    verified historical `analyze-review-feedback` copies, including the shared
    `~/.agents/skills` copy. Unverified/customized copies are reported and preserved
    for separately approved manual reconciliation. Retain the active
   `resolve-review-feedback` copy and rollback backups. Follow the
   [migration steps](docs/remove-old-ai-files.md#combined-review-feedback-skill)
   and never delete plugin caches manually.

10. For consolidated coding workflows, preserve old development skills and needed
    policy/role backups, preview managed retirement, and separately authorize
    coordinated coding-plugin, personal-policy and native-role activation. Verify
    `develop-code` and independent `review-code` in a fresh task. Shared-root
    retirement affects other harnesses; customized/unverified/symlinked copies
    require separate exact-path reconciliation. Retain rollback archives and never
    delete caches manually. Follow the [activation and rollback steps](docs/remove-old-ai-files.md#consolidated-coding-workflows).

### Parallel agent teams

Select `run-agent-team` explicitly in the normal main AI session with an approved
plan, using the active harness's supported skill mechanism. Its workflow contracts
are harness agnostic; verify actual native tools and grants before dispatch.
Name the skill, plan and authorized execution scope in an ordinary request.
Codex CLI users can also select it through `/skills`; `/goal` is optional.
The current main session owns dispatch, Git, worktree lifecycle, integration
and canonical task state. No custom coordinator is needed;
no custom primary or nested manager is required. Planning stays independent.

Workers use isolated assigned worktrees. Sol coordination, Luna implementation
and Astra review/analysis are preferences with supported fallback to installed
pins or native defaults. Unknown coordinator model telemetry alone does not block.
Explicit user model constraints still apply. Generic reviewer with the supplied review-story contract
retains existing review budgets and session continuation.
Fill eligible capacity before waiting. Reconcile uncertain prior ownership before
takeover. See [current workflow entry points](docs/agent-workflows.md) and the
[historical verification record](docs/agent-team-verification.md) for source-check
and native-execution limits.
