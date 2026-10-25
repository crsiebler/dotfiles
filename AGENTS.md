# AGENTS.md - Dotfiles Repository Guidelines

This document provides guidelines for agents working in this dotfiles repository. These dotfiles contain shell configurations, aliases, and scripts primarily for Zsh environments.

## Repository context

For unfamiliar or cross-cutting work, start with [docs/overview.md](docs/overview.md)
and follow the links relevant to the task. Small, well-scoped changes do not
require reading the full collection. Maps describe the repository and do not
override these instructions; verify affected paths and important relationships
against current source before making changes.

## AI source ownership and installation

Read [docs/ai-configuration.md](docs/ai-configuration.md) for setup,
connections, and limitations; [docs/agent-authoring.md](docs/agent-authoring.md)
defines the native role contract.

- Portable skills live in `ai/plugins/<plugin>/skills/<action>/`. The checkout-local
  `craft` marketplace at `.agents/plugins/marketplace.json` contains `coding`,
  `reporting`, `researching`, `delegating`, and `producing`.
  `producing` owns `create-audio`, `create-sprites`, `create-gif`, `create-docx`,
  `create-pptx`, `create-xlsx`, and `create-pdf`; `coding` owns `create-skill`
  and `create-mcp-server`.
  `researching` owns `read-docx`, `read-pptx`, `read-xlsx`, and `read-pdf` alongside
  web research. Reporting owns synthesis/communication, not file production.
  Prefer adequate native tools for simple reads. Resolve bundled resources from
  the loaded skill. Each skill links to `references/requirements.md` for required
  and optional dependencies, installation instructions, and availability checks.
  Keep the 47-skill [dependency inventory](docs/skill-dependencies.md) aligned with
  source changes. Core-method additions include operate-systems and assess-controls
  in coding, analyze-data/research-users in researching, plan-product in reporting,
  write-content/design-interface in producing, and prepare-handoff in delegating.
  Dependency setup is separately authorized and never performed
  by AI installation.
  See [document verification](docs/document-skill-verification.md) for actual tested
  environments and artifact/rendering limits. Document implementations are original;
  create-skill/create-gif and create-mcp-server adapt attributed Apache upstream
  bundles. create-mcp-server is instruction-only, with no runtime dependencies;
  see [MCP skill verification](docs/create-mcp-server-verification.md).
- `coding` provides `archive-run` for the reusable deterministic archival helper.
  run-agent-team owns delivery and review-story owns the reusable staged-review
  contract supplied to generic reviewer. Keep their safeguard/schema invariants tested.
- `coding` adds `run-agent-team` for explicit parallel execution of an
  existing approved plan. The normal main AI session owns dispatch, Git,
  integration and canonical task state. The main session follows the workflow directly;
  no coordinator role, primary switch or nested dispatcher is required. Reconcile prior
  ownership before takeover. Preserve native capability/model/pin preflight. Source
  delivery does not activate installed roles or prove native team execution.
- `coding` uses `develop-code` for feature/fix/refactor methods and independent
  `review-code` for independent assessment and authorized focused verification. The three former development bundles
  are retired; no aliases remain. Keep the project template optional and preserve
  workflow-supplied staged-review contracts. Follow [coding activation](docs/remove-old-ai-files.md#consolidated-coding-workflows)
  for coordinated policy/role/skill refresh; source delivery is not installed discovery.
- `researching` provides provider-agnostic `search-web`; load its Exa MCP reference
  only when those tools are available and selected. Skill discovery is automatic.
- The single harness-agnostic personal policy is `ai/AGENTS.md`. Installation
  copies its bytes unchanged to both user-level `AGENTS.md` destinations, without
  concatenation or normalization. This root file is repository-only guidance.
- Codex configuration lives in `ai/codex/config.toml`.
  OpenCode configuration and native prompts remain under `ai/opencode/`.
- OpenCode source uses native V2 fields and ordered permissions. Its installer
  requires an OpenCode 2.x-or-newer binary before writes; it never upgrades it.
  Built-in notifications live in cli.json. Image generation is optional via
  opencode-img with separate API billing, not a bundled active plugin. See
  [V2 configuration](docs/opencode-v2.md). Retain legacy tui/notifier backups
  in cleanup recognition, but never remove their active installed files implicitly.
- Coding runtime/model selection policy lives in the run-agent-team skill; see
  [selection and rollout](docs/runtime-selection.md). Reusable roles omit model
  and effort pins; preserve their expertise and permission/review contracts.
  Global subagent/build defaults must not silently override session selection.
  Explicit runtime profiles remain supported; inheritance is not automatic routing.
  Galena is the source checkout and local verification host. Explicit team sessions
  use dependency-ready task workers. Paperclip/NCase
  multi-session management is a separate future project. Controller/application
  integrations belong in Avengers; Apple integration and external tracker adapters
  are excluded from this foundation.
- `ai/codex/agents/*.toml` is the canonical custom-agent collection (5 roles).
  Copy all sources byte-for-byte to Codex and generate 5 OpenCode Markdown files.
  Keep `sprite-artist` native and OpenCode-only under `ai/opencode/agents/`;
  the installer copies the minimal provider-permission adapter unchanged (6 total).
  Agent metadata belongs in native TOML or that Markdown frontmatter;
  use generic rendering, not exclusions or overrides JSON.
- Only auditor uses native sandbox_mode = "read-only". Its contract prohibits
  tests, builds, active scans, edits, remediation and external posts. Codex may
  permit read-only shell inspection; OpenCode maps this metadata to deny-all plus
  read/glob/grep. Parent runtime overrides and MCP approvals remain independent.
  Reviewer inherits runtime permissions for authorized focused verification and
  preserves the candidate. Neither role may repair a candidate under review.
- The five custom roles are researcher, planner, reviewer, auditor and operator.
  Implementation uses the main session or available native execution agents. They are optional task contracts, not a required pipeline. The main
  session owns dispatch, Git/integration and canonical state. No nested delegation
  or proxy dispatch. Specialized knowledge lives in existing plugins. See
  [role selection](ai/plugins/delegating/skills/use-subagents/references/core-roles.md).
- Technology standards live in eight apply-*-standards skills in coding;
  MCP standards extend create-mcp-server. Generic roles own responsibility and
  permission boundaries. Discover current roles through use-subagents and load
  standards through the relevant skill; no historical role lookup is required.
- `use-subagents` bundles discovery tooling; do not install it globally.
  Inspecting a definition is not a native delegated invocation.
- OpenCode commands are `/create-sprite`, `/define-requirements`, `/plan-work`,
  `/ship`, `/find-agents`, and unchanged `/review-pr`. `create-sprites` owns common
  generation rules; load its Godot reference only for Godot requests or relevant
  project context. Asset-only work must not require a Godot binary.
- `create-audio` owns the audio generation workflow and backend adapters;
  `/create-audio` is configured inline in OpenCode JSON and agents resolve
  `scripts/create_audio.py` from the installed skill. There is no audio shell
  alias. Stable Audio MLX infrastructure defaults to
  `~/Models/local-audio/`; project request JSON owns prompts and generation
  preferences. AI installation must not provision models. Existing game
  installations are not automatically moved or removed. No chat-provider entry
  is added for an audio-only model.
- Managed AI JSON/TOML files are replaced byte-for-byte, not merged: Codex
  `config.toml` and OpenCode V2 `opencode.json` and `cli.json`. Keep desired local settings
  and permission restrictions in source before installation. Preserve preflight
  checks and timestamped backups. After installation, verify the installed files,
  retain needed rollback copies outside cleanup locations before `make clean`.
- `make install-codex`, `make install-opencode`, and `make install-ai` modify user
  AI configuration only. They require explicit installation authorization. No
  logins, dependency bootstrap, shell setup, or binary installation are included.
  Missing `skills` is a blocker, not permission to download it with `npx`.
  All installation targets require `skills`; retirement requires the tested CLI
  1.5.24. Authorized installation includes automatic retirement of verified managed
  skills in the selected private root and shared `~/.agents/skills`, affecting all
  harnesses reading that shared root. `all` uses OpenCode's private root for skills;
  Codex-only uses its private root, while retaining native plugin installation.
  `make preview-ai-cleanup` (optional `AI_TARGET=opencode|codex`) is read-only and
  does not invoke either CLI. Inventories bind to the checkout; never hand-edit
  them to manufacture ownership. Preserve unverified/customized/symlinked assets.
  Native removal is limited to previously recorded plugins removed from the
  current marketplace; preserve current Craft bundles and unrelated plugins.
- `make install` additionally modifies shell/env/global Git and installs OpenCode but not Codex or global subagents. Never use it as
  a validation command.
- `make install` first runs `check-install-prerequisites`, checking OpenCode V2
  and the skills CLI before any mutation, including under parallel make. This
  CLI-only check does not replace later source/destination/conflict preflight or
  make the full install transactional. No binary upgrade is implicit. Only then
  run `install-zsh-extensions`: clone only missing custom
  plugins and Powerlevel10k from the explicit registry in
  `scripts/install-zsh-extensions.py`. Honor `ZSH`/`ZSH_CUSTOM`, require an existing
  Oh My Zsh installation, and never pull/reset/replace existing extensions.
  Preserve custom non-Git copies with readable entry points; stop on invalid
  directories or symlinks. Tests use local Git fixtures, not live downloads.
  No CLI applications or Railway setup are included. AI-only targets stay separate.
  Before manual extension updates/removal, inspect existing copies, retain needed
  backups, and obtain scoped approval. `make clean` must not remove plugins/themes.
- GitHub, Exa, and Context7 are globally enabled. Vercel, Jira/Rovo, PostgreSQL, and Jev require
  trusted project opt-in. AWS/Elastic MCP definitions are intentionally absent.
  PostgreSQL uses the built local Node `mcp-suite` server documented in the
  installation guide, not Docker; installation does not clone/build/install it.
  Jev likewise uses its built local Node server, forwards `AI_GATEWAY_API_KEY`,
  and prompts for every tool; installation does not build it or run evaluations.
  Launcher tests use fake Node only, model known OpenCode env substitutions, and
  do not establish server-side validation or live integration.
  Exact GitHub/Jira/PostgreSQL read-tool exceptions skip approval; writes and
  unknown tools still ask. PostgreSQL `execute_query` always asks because it
  accepts arbitrary SQL. Exa/Context7 expose only approved research tools.
  OpenCode Chrome/Playwright/Jam allow all tools when enabled; ElevenLabs asks
  for every tool. These four remain absent from Codex. Preserve this policy and
  narrower reviewer restrictions; never log tokens,
  connection strings, full authorization headers, or credential stores.

## Local coding model

Bonsai 2 MLX is the only local coding provider in `ai/opencode/opencode.json`.
Runtime installation pins are documented in `docs/local-bonsai.md`; no separate
local provider profile is needed. The `mlx-bonsai` function in
`aliases/.aliases` invokes the
uv-tool executable directly with weights in `~/Models/bonsai-2-mlx`; no Conda
environment or checkout path is used. Follow `docs/local-bonsai.md`.
Installation does not provision this runtime or download weights. Preserve the
separate audio environment. For cleanup: inventory exact coding model paths,
stop their users with authorization, remove only approved model directories,
and retain needed rollback copies until the MLX integration is verified. Never
delete a shared cache/environment wholesale. Keep README and this guide aligned.

## Review and workflow boundaries

- Carry existing bounded user authorization through skill handoffs and continuation.
  Separately authorized scope does not require a repeated approval turn. Ask for
  missing authority or material changes in target, content, effect, or cost;
  preserve exact-payload preview requirements and runtime restrictions. See
  [workflow approval scope](docs/agent-workflows.md#approval-scope-across-workflows).

- OpenCode PR review objectives/schema remain in ai/opencode/commands/review-pr.md.
  /review-pr --post must preview the exact payload and obtain explicit confirmation.
- Generic reviewer owns independent assessment and authorized focused
  verification, with no candidate edits or fixes. Explicit inspection-only
  requests prohibit tests/builds/browser actions. Runtime permissions remain
  authoritative; inheriting permissions is not an immutable read-only guarantee.
- review-story owns the staged-story protocol/schema. run-agent-team discovers
  the installed skill and embeds its complete contract in every generic reviewer
  packet; never guess cache paths or rely on inherited context. Supply story,
  attempt/pass/session identity, base and staged tree, worktree, acceptance,
  verification mode/commands, private outputs, resources and count/time limits.
  Select the native reviewer when supported. Without a custom-role selector,
  supply the complete discovered reviewer instructions and review-story contract
  to a fresh independent generic agent; no exception approval is needed solely
  for that missing selector. Preserve role pins, native restrictions and actual
  same-session continuation. Never reuse the candidate implementer for review or
  claim custom native role loading from a label or supplied instructions.
  Review uses candidate-equivalent inputs; mixed staged/unstaged results cannot
  prove the staged candidate. Verify identity/state before and after checks.
- One initial and at most one targeted pass share the actual native session per
  attempt. Initial reading permits at most 40 small calls; targeted reading uses
  two tool turns for prior findings/remediation regressions only. Verification
  budgets are supplied separately. Missing evidence blocks rather than inventing
  a pass, expanding permission or resetting attempts.
- A final blocked verdict preserves candidate, pending status, history and passes.
  Resume only on verified material resolution. Another turn, new agent/model,
  compaction or elapsed time is insufficient. Independently eligible isolated
  stories may continue; do not manufacture activity or duplicate review cycles.
- Plans default to PLAN.md in both harnesses; explicit formats override. Planning
  creates no execution logs/memory or workers. Ordinary sessions suffice; /goal is
  optional. An explicit user request to implement an approved plan authorizes
  initial and subsequent scoped local commits without repeated approval prompts.
  Carry that grant through continuation; narrower no-commit/planning/source-only
  instructions take precedence. A copied template or plan approval alone grants
  no execution. Initial plan/checkpoint commits contain only the approved plan
  and required task-owned metadata; implementation commits retain checks/review.
- prepare-implementation audits approval gates and manual prerequisites through
  the requested endpoint and resolves them before unattended readiness. Keep the
  evidence in the plan; unresolved mandatory gates mean a blocked draft. Planning
  performs no setup or implementation. Execution checks readiness before edits or
  dispatch, carrying unchanged grants forward without bypassing runtime controls.
  Plan only agent-executable, noninteractive verification; do not add manual QA
  or routine deployment gates. Deployment checks require explicit scope and
  automation. Explicit non-automatable requirements need upfront resolution,
  not manual implementation stories or silently weakened acceptance.
- write-requirements keeps PRD acceptance automation-compatible and preserves
  explicit human requirements as conflicts for upfront resolution. run-agent-team
  carries the approved autonomous scope into packets and required closeout; no
  added manual QA, human result confirmation or routine deployment gates. Required
  checks still need actual evidence; optional human follow-up cannot block delivery.
- The main session owns dispatch, Git, integration and canonical state. Workers
  receive absolute task roots, exact prepared branches/bases and owned paths.
  Validate dependency references/cycles and clean committed baselines before
  dispatch. A scoped initial plan/checkpoint commit may precede that clean base.
  Never copy or commit unrelated/pre-existing implementation work to prepare one
  or switch the user's checkout. Worktree lifecycle needs scoped authority. Reject detached HEAD,
  main/master and branch mismatch. Coordinate shared resources and freeze the
  candidate and conflicts during review, not unrelated isolated workers.
- Keep fast/standard/deep risk budgets, at most two implementation advisors,
  required checks and bounded native/self-review selection. Invalid memory,
  unavailable required protocol/session, failed checks/review or failed commit
  stops delivery. Only completion markers belong in task sources; execution
  history belongs in progress.md. Restore only provisional completion on failed
  finalization. No new runner, daemon, restart loop or compaction hook.
- Use relevant project lint/tests/type checks and verify-interface for UI changes.
  Never claim unavailable checks passed. Source changes do not activate installed
  configuration; installation/refresh remains separately authorized.

- Keep append-only review history in worktree-root `progress.md` (never rewrite headers),
  bounded version-1 operational knowledge in project `memory.json` (at most 20
  patterns and 20 suppressions), and only durable repository instructions in the
  nearest `AGENTS.md`. Missing memory is normal; invalid memory blocks without
  overwrite. Update memory only after passing review, promoting reusable verified
  accepted fixes and suppressing only evidenced false positives.
- One active plan belongs to each worktree. Keep task sources and `memory.json`
  at the root; create the journal only for a permitted execution checkpoint, never
  during planning/PRD drafting. Do not read or migrate legacy execution logs.
- Completed-run archival follows the installed archive-run capability's
  `references/completed-run-archive.md` and `scripts/archive_run.py`. PRDs declare
  the run ID, exact task source and associated PRDs in a work-run JSON block.
  Root `progress.md` carries truthful pre-commit story-result records; the script
  verifies their committed task markers, copies/hashes all run-owned artifacts,
  then removes only unchanged active copies. PRDs, plan, progress and memory are
  peers in `archive/YYYY-MM-DDTHHMMSSffffffZ-feature/`; the receipt maps original
  paths and records provenance. Preserve existing historical archive layouts.
  Keep the persistent archive lock at Git's per-worktree `archive-run.lock`
  metadata path, outside tracked files; never stage, reset or delete it.
  Invoke automatically after verified delivery under an explicit scoped
  archival/removal grant, which may be included upfront with execution. One
  closeout commit is covered by an approved-plan implementation launch; archival
  and active-copy removal still require their applicable scope. Carry existing
  approval forward without another commit prompt.
  Wait for all writers to stop before archival. Preserve unrelated work.
  Never reset journals, infer evidence from prose, overwrite archives or retry
  partial cleanup automatically. Archival may run on any branch, including
  main/master after merge, using retained reachable/squash delivery evidence.
  Do not recreate/switch branches or rewrite historical plan metadata. Missing
  metadata/evidence blocks archival; this does not relax execution branch guards.
- PRD replacement requires exact-path archival approval and verified preservation
  before writing the replacement. Same-PRD revisions stay scoped; requirements
  drafting never archives execution state as a side effect.

## Build/Lint/Test Commands

For Python checks, use the existing Conda `dotfiles` environment when available.
It includes PyYAML for create-skill validation. In a noninteractive shell on this
machine, activate it without sourcing personal shell configuration:

```bash
source /opt/anaconda3/etc/profile.d/conda.sh
conda activate dotfiles
```

Use the activated `python` for skill helpers, or its absolute interpreter path
when activation does not persist between tool calls. Check this environment before
reporting a missing Python dependency. If unavailable, report that limitation;
do not create an environment or install dependencies without authorization.

There is no standalone repository typecheck target. Run local source validation
and relevant regression tests; record unavailable checks explicitly:

```bash
make validate-ai
python3.11 -m unittest discover -s tests -p '*test*.py'
python3.11 tests/agent_contract_test.py
python3.11 tests/archive_run_test.py
bash tests/zsh_aliases_test.sh
```

### Manual Validation
```bash
# Check Makefile syntax (dry run of install)
make -n install

# Check relevant shell syntax without sourcing personal environment files
zsh -n aliases/.aliases zsh/.zshenv zsh/.zshrc
```

### Testing Manual Sourcing
```bash
# Verify alias files can be sourced without errors (Zsh only recommended)
zsh -c "source aliases/.aliases"
zsh -c "source aliases/.git_aliases"
zsh -c "source aliases/.node_aliases"
zsh -c "source aliases/.docker_aliases"
zsh -c "source aliases/.symfony_aliases"

# Test configuration loading
zsh -c "source zsh/.zshenv"
```

### Single Test Execution
Python, Ruby, and shell regression tests live under `tests/`. For an optional
manual sourcing check, use a project-local scratch directory, not `/tmp`:

```bash
# Test a specific alias or function by sourcing and executing
zsh -c "source aliases/.aliases && mkcd ./tests/manual-mkcd && pwd"

# Test environment variable loading
zsh -c "source zsh/.zshenv && echo \$JAVA_HOME"
```

## Code Style Guidelines

### Zsh Dotfiles
#### File Structure
- Include meaningful comments explaining each section or alias group
- Keep files simple and focused on a clear purpose

#### Naming Conventions
- Use lowercase with underscores for function names (`mkcd()`)
- Use lowercase for variable names (`old_lc_collate`, `length`)
- Alias names should be short but descriptive: `hs`, `myip`, `gac`, `nis`
- File names for configuration use dot prefix: `.zshrc`, `.aliases`, etc.

#### Formatting
- Use consistent indentation
- Use spaces around operators: `if [ $# -eq 0 ]`
- Break long lines for readability (< 80 characters)
- Use blank lines to separate logical sections

#### Error Handling
- Check for file existence before sourcing: `if [ -f ~/.aliases ]; then`
- Provide meaningful feedback if operations fail
- Handle edge cases gracefully

#### Best Practices
- Quote variables: `"$1"`, `"${1}"`
- Use `local` for function variables to avoid polluting global scope
- Prefer `printf` over `echo` for portability
- Avoid hardcoded paths where possible

### Configuration Files

#### Zsh Configuration (.zshrc)
- Group related settings together with comments
- Use consistent commenting style for disabled options
- Keep personal customizations separate from framework settings
- Document any non-obvious configurations

#### Environment Files (.zshenv)
- Load aliases conditionally to avoid errors if files don't exist
- Organize environment variables clearly by category
- Sets `JAVA_HOME=/usr/bin/java` by default (customize as needed)

### Aliases
- Keep aliases simple and focused
- Use descriptive names that indicate the command's purpose
- Group related aliases together
- Comment complex aliases explaining their functionality

#### Specialized Aliases (.git_aliases, .node_aliases, etc.)
- Prefix with tool name if not obvious: `gac` for git add commit
- The provided `gac` alias does not include a commit message; users should edit it to add their message
- Use consistent naming and grouping in each alias file

### Comments
- Use `#` for single-line comments
- Place comments above the code/alias they explain
- Keep comments concise but informative
- Comment complex logic or non-obvious operations

### File Organization
- Keep related configurations in separate files
- Use consistent naming patterns (`.tool_aliases`)
- Document file purposes in README.md

### Security Considerations
- Never store secrets or credentials directly in dotfiles
- Be cautious with `sudo` commands in aliases
- Validate URLs and commands before execution
- Use safe practices for file operations (check existence, permissions)
- Secrets should go in `$HOME/.env`, which is never tracked by git

### Git Workflow
- Commit related changes together
- Use `<type>(<scope>): <description>` commit messages; commit only when authorized
- Keep the repository focused on configuration files
- Test changes before committing

### Maintenance
- Regularly review and update aliases for relevance
- Remove unused or outdated configurations
- Keep dependencies documented
- Test configurations across different environments where possible

---

## Cleaning Up Dotfile Backups

1. Verify installed configurations and retain needed rollback copies outside the
   cleanup locations before running `make clean`.
2. Review generated `.zshrc.backup.<timestamp>` files, adjacent timestamped AI
   configuration/agent/command backups, timestamped skill/retirement archives under
   `.install-ai-backups/`, and hashed `plugin-sources/` snapshots. Existing `.env`
   files are synchronized without generating backups.
3. `make clean` removes these recognized backups for both AI harnesses, honoring
   `CODEX_HOME` and `XDG_CONFIG_HOME`, including backups from AI-only installation.
   Preserve active files, plugin caches, installation inventories, unrelated legacy controls,
   and legacy `.env` backups. Reject invalid or symlinked roots before deletion;
   skip symlink backup candidates and never follow archive symlinks.
4. Preserve unknown backup names and unrelated files for separate manual review
   using [manual removal](docs/remove-old-ai-files.md). Never delete a whole
   configuration root to remove backups. An agent must not run global cleanup
   merely to validate code; use isolated project-local fixtures.
5. Review obsolete installed command/agent paths listed in that guide separately;
   source retirement does not remove installed files or project artifacts. No automatic migration or aliases are installed.
6. Technology-specific roles now use generic roles plus standards skills.
   Verify current roles and skills after separately authorized installation.
   Preserve customizations and obtain exact-path approval for old
   installed role removal. Source retirement does not remove installed copies.
7. Review retained installed AWS/Elastic MCP entries and old PostgreSQL Docker
   fields separately. Back up customizations and approve exact config edits before
   removal; preserve approval rules, active `POSTGRESQL_CONNECTION_STRING`, and
   environment exports still used elsewhere. Source removal is not installed cleanup.
8. For `use-exa` renamed to `search-web`, verify the replacement after authorized
   installation or Codex native plugin refresh, preserve customizations, and
   approve exact old installed paths before manual removal using that guide.
   Restart the harness and start a new Codex thread; never delete plugin caches
   manually or assume OpenCode copies were automatically removed.

9. For producing/document activation, preserve customized copies and coordinate
   `coding`, `researching`, and `producing` refresh/copies with separate installation
   authorization. Restart the harness and use a new Codex task to verify unique
   skill discovery. Audio/sprite identifiers are unchanged: never remove active
   same-named OpenCode copies merely because source ownership moved. Follow
   [rollout cleanup](docs/remove-old-ai-files.md#producing-and-document-rollout),
   retain backups and obtain exact-path approval for obsolete copies. Never manually
   delete caches; native plugin replacement requires its own reviewed scope.

10. For the combined `resolve-review-feedback` skill, preserve customized copies,
    separately authorize coding plugin refresh or OpenCode installation, restart,
    and verify assessment plus resolution preparation. Authorized installation now
    archives/removes exact historical `analyze-review-feedback` trees automatically,
    including shared global copies. Unverified versions/customizations still need
    exact-path reconciliation approval; preserve the active
    `resolve-review-feedback` copy and needed rollback backups. Follow the
    [migration steps](docs/remove-old-ai-files.md#combined-review-feedback-skill).
    Never delete plugin caches manually; source retirement is not installed cleanup.

11. For consolidated coding workflows, preserve customized old development bundles,
    personal policy and role copies; preview managed retirement, then separately
    authorize coordinated installation/refresh. Verify `develop-code` and independent
    `review-code` after restart in a fresh task. Shared-root removals affect all
    harnesses reading it. Preserve unverified/customized/symlinked copies for exact-path
    reconciliation approval; retain retirement archives, changed-copy backups and
    plugin snapshots for an approved coherent rollback. Never manually delete caches.
    Follow [activation and rollback](docs/remove-old-ai-files.md#consolidated-coding-workflows).

**Process for future iterations:**
- Keep cleanup scoped to recognized installer backups; preserve active files,
  installation inventories, unknown backups, and legacy `.env` backups.
- Always update both README.md and AGENTS.md to document the backup and cleanup process step-by-step so code and docs remain in sync.

---

## Development Workflow

1. Make changes to configuration files
2. Run relevant repository-local regression and syntax checks
3. Use manual sourcing only when appropriate; it can load personal environment files
4. Inspect the diff and preserve unrelated work; do not install globally to test
5. Commit with the repository convention only when authorized
6. Update documentation if needed

## Dependencies

This repository assumes:
- Zsh as the required shell
- Oh My Zsh framework
- Standard Unix tools (bash, cp, mkdir, etc.)
- Python 3.11+ for AI source validation, rendering, and installation;
  `python3` for environment sync
- Codex CLI with native local marketplace and plugin add/list/remove support
  (capability checks, no exact release pin); `skills` CLI for OpenCode skill copies
- OpenCode 2.x or newer before OpenCode configuration installation; upgrade separately
- Optional: shellcheck for linting (run manually, not automated)

## Environment Setup

Follow [README setup](README.md#setup-and-documentation) and the
[installation guide](docs/ai-configuration.md) before any authorized install.
Never overwrite an existing `$HOME/.env`:
merge missing example keys privately and export the needed values in the launching
shell. AI-only targets neither source nor synchronize it. Enabled GitHub MCP
requires `GITHUB_MCP_TOKEN`; installation never performs authentication. Restart
the selected harness after installation, and start a new Codex thread for plugins.
