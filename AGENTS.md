# AGENTS.md - Dotfiles Repository Guidelines

This document provides guidelines for agents working in this dotfiles repository. These dotfiles contain shell configurations, aliases, and scripts primarily for Zsh environments.

## AI source ownership and installation

Read [docs/ai-configuration.md](docs/ai-configuration.md) for setup,
connections, and limitations; [docs/agent-authoring.md](docs/agent-authoring.md)
defines the native role contract.

- Portable skills live in `ai/plugins/<plugin>/skills/<action>/`. The checkout-local
  `craft` marketplace at `.agents/plugins/marketplace.json` contains `coding`,
  `reporting`, `researching`, and `delegating`.
- `researching` provides provider-agnostic `search-web`; load its Exa MCP reference
  only when those tools are available and selected. Skill discovery is automatic.
- The single harness-agnostic personal policy is `ai/AGENTS.md`. Installation
  copies its bytes unchanged to both user-level `AGENTS.md` destinations, without
  concatenation or normalization. This root file is repository-only guidance.
- Codex configuration sources are `ai/codex/config.toml` and `astra.config.toml`.
  OpenCode configuration and native prompts remain under `ai/opencode/`.
- `ai/codex/agents/*.toml` is the canonical custom-agent collection (127 roles).
  Copy all sources byte-for-byte to Codex and generate 127 OpenCode Markdown files.
  Keep `sprite-artist`, `ralph`, and `ralph-reviewer` native and OpenCode-only
  under `ai/opencode/agents/`; the installer copies all three unchanged (130 total).
  Agent metadata belongs in native TOML or those three Markdown frontmatters;
  use generic rendering, not exclusions or overrides JSON.
- The seven inspection roles, including `powershell-security-hardening`, use native
  `sandbox_mode = "read-only"` and guidance
  prohibiting tests, edits, mutating commands, and external posts. Native read-only
  shell inspection is permitted by the role when authorized by the runtime.
  OpenCode maps read-only sandbox mode to deny-all plus `read`/`glob`/`grep`, a more
  restrictive tool policy, not equivalent Codex sandbox or MCP enforcement.
  Codex parent runtime overrides apply after role settings; MCP approval is
  independent. Do not claim immutable per-role policy or project-only access.
- `use-subagents` bundles discovery tooling; do not install it globally.
  Inspecting a definition is not a native delegated invocation.
- OpenCode commands are `/create-sprite`, `/define-requirements`, `/plan-work`,
  `/ship`, `/find-agents`, and unchanged `/review-pr`. `create-sprites` owns common
  generation rules; load its Godot reference only for Godot requests or relevant
  project context. Asset-only work must not require a Godot binary.
- `make install-codex`, `make install-opencode`, and `make install-ai` modify user
  AI configuration only. They require explicit installation authorization. No
  logins, dependency bootstrap, shell setup, or binary installation are included.
  Missing `skills` is a blocker, not permission to download it with `npx`.
- `make install` additionally modifies shell/env/global Git and uses sudo for
  Ralph; it installs OpenCode but not Codex or global subagents. Never use it as
  a validation command.
- GitHub, Exa, Context7 are globally enabled. Jira/Rovo and PostgreSQL require
  trusted project opt-in. AWS/Elastic MCP definitions are intentionally absent.
  PostgreSQL uses the built local Node `mcp-suite` server documented in the
  installation guide, not Docker; installation does not clone/build/install it.
  Launcher tests use fake Node only, model known OpenCode env substitutions, and
  do not establish server-side validation or live integration.
  Exact GitHub/Jira/PostgreSQL read-tool exceptions skip approval; writes and
  unknown tools still ask. PostgreSQL `execute_query` always asks because it
  accepts arbitrary SQL. Exa/Context7 expose only approved research tools.
  OpenCode Chrome/Playwright/Jam allow all tools when enabled; ElevenLabs asks
  for every tool. These four remain absent from Codex. Preserve this policy and
  narrower reviewer restrictions; never log tokens,
  connection strings, full authorization headers, or credential stores.

## Review and Ralph boundaries

- Keep GitHub PR review objectives, schemas, orchestration, and context gathering
  canonical in `ai/opencode/commands/review-pr.md`. `/review-pr --post` must preview
  the exact GitHub review command/API payload and obtain explicit confirmation
  before any `gh` review write, regardless of available MCP write permissions.
- Ralph local staged reviews use only `ai/opencode/agents/ralph-reviewer.md`, not
  general reviewers. Preserve the three-step, project-local read/staged-Git-only
  boundary, exact JSON output, and at most one same-session follow-up.
- `write-requirements` creates requirements; `prepare-implementation` defaults to
  `plan.json` in OpenCode and a Markdown story checklist in `PLAN.md` in Codex.
  Explicit user format requests override these defaults. OpenCode entry points
  are `/define-requirements` and `/plan-work`; neither starts execution.
  Resolve active-harness identity from trusted runtime context or the invoking
  native entry point; `ai/opencode/commands/plan-work.md` supplies the JSON default.
  Ask when routing is unavailable or ambiguous, never infer it from `PATH`,
  installed binaries, directories, environment variables, or policy headings.
- Ralph is OpenCode-only: `ralph --mode standard --max-iterations 10`.
  Require a prepared committed Git worktree on exactly `plan.json`'s `branchName`;
  reject detached HEAD and main/master. Do not create or switch branches for Ralph.
- `--auto` is unsupported and rejected. Standing authorization covers routine scoped
  implementation, necessary project dependencies, and relevant tests, not
  permission bypasses. Docker lifecycle, migrations including local/test, service
  operations, global changes, and other sensitive actions need explicit approval.
- A fully complete valid Ralph PRD exits without launching OpenCode.
- Codex may execute an approved Markdown plan through native `/goal`. Keep story
  evidence and resumption checkpoints in the plan. Do not import Ralph's reviewer
  gate or fresh-session loop into that workflow. Automatic story-boundary compaction
  is deferred in `docs/backlog.md`; do not install compaction hooks/controllers.
- Each Ralph story should fit one iteration and include typecheck acceptance criteria.
  Use `verify-interface` for browser verification of UI changes. Run relevant
  lint/typecheck/tests before committing; do not claim unavailable checks passed.
- Keep append-only review history in `progress.txt`, bounded operational knowledge
  in project `memory.json` (at most 20 patterns and 20 suppressions), and only
  durable repository instructions in the nearest `AGENTS.md`.

## Build/Lint/Test Commands

There is no standalone repository typecheck target. Run local source validation
and relevant regression tests; record unavailable checks explicitly:

```bash
make validate-ai
python3.11 -m unittest discover -s tests -p '*test*.py'
python3.11 tests/agent_contract_test.py
bash tests/ralph_model_test.sh
bash tests/ralph_review_test.sh
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

1. Verify the installed configuration and retain any backups needed for rollback.
2. Review adjacent `.backup.<timestamp>` files and changed OpenCode skill assets
   under `.install-ai-backups/<timestamp>/skills/` in the configuration root.
   The broad installer backs up `.zshrc`. Existing `.env` files are synchronized
   by appending missing keys/exports without creating backups.
3. With explicit approval covering all matching `.zshrc` backups, `make clean`
   removes only `$HOME/.zshrc.backup.*`. It preserves active files, existing
   `.env` backups, and all AI configuration/backups.
4. For AI files and backups, follow [manual removal](docs/remove-old-ai-files.md),
   obtain explicit deletion approval, and remove only reviewed paths. Never delete
   a whole configuration root to remove backups.
5. Review obsolete installed command/agent paths listed in that guide separately;
   command renames do not rename `bin/ralph`, native Ralph agents, `prd.json`, or
   the bundled `subagents` helper. No automatic migration or aliases are installed.
6. For the PowerShell consolidation, verify `powershell-expert`, preserve custom
   copies, and obtain exact-path approval before removing the three retired roles
   in either harness using that guide. Keep UI and read-only assessment roles.
7. Review retained installed AWS/Elastic MCP entries and old PostgreSQL Docker
   fields separately. Back up customizations and approve exact config edits before
   removal; preserve approval rules, active `POSTGRESQL_CONNECTION_STRING`, and
   environment exports still used elsewhere. Source removal is not installed cleanup.
8. For `use-exa` renamed to `search-web`, verify the replacement after authorized
   installation or Codex native plugin refresh, preserve customizations, and
   approve exact old installed paths before manual removal using that guide.
   Restart the harness and start a new Codex thread; never delete plugin caches
   manually or assume OpenCode copies were automatically removed.

**Process for future iterations:**
- Keep AI and old `.env` backup removal manual; limit `make clean` to `.zshrc` backups.
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
- Ruby only for native reviewer YAML validation in `tests/ralph_review_test.sh`,
  not as an installer dependency
- Codex CLI 0.153.4 for Codex installation; `skills` CLI for OpenCode skill copies
- jq for Ralph `plan.json` completion checks
- Optional: shellcheck for linting (run manually, not automated)

## Environment Setup

Follow [README setup](README.md#setup-and-documentation) and the
[installation guide](docs/ai-configuration.md) before any authorized install.
Never overwrite an existing `$HOME/.env`:
merge missing example keys privately and export the needed values in the launching
shell. AI-only targets neither source nor synchronize it. Enabled GitHub MCP
requires `GITHUB_MCP_TOKEN`; installation never performs authentication. Restart
the selected harness after installation, and start a new Codex thread for plugins.
