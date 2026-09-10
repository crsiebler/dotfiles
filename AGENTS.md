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
- `ai/codex/agents/*.toml` is the canonical custom-agent collection (128 roles).
  Copy all sources byte-for-byte to Codex and generate 128 OpenCode Markdown files.
  Keep `sprite-artist`, `ralph`, and `ralph-reviewer` native and OpenCode-only
  under `ai/opencode/agents/`; the installer copies all three unchanged (131 total).
  Agent metadata belongs in native TOML or those three Markdown frontmatters;
  use generic rendering, not exclusions or overrides JSON.
- The eight inspection roles, including `powershell-security-hardening` and
  `story-reviewer`, use native
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
  `/ship`, `/find-agents`, `/recover-ralph`, and unchanged `/review-pr`. `create-sprites` owns common
  generation rules; load its Godot reference only for Godot requests or relevant
  project context. Asset-only work must not require a Godot binary.
- `make install-codex`, `make install-opencode`, and `make install-ai` modify user
  AI configuration only. They require explicit installation authorization. No
  logins, dependency bootstrap, shell setup, or binary installation are included.
  Missing `skills` is a blocker, not permission to download it with `npx`.
- `make install` additionally modifies shell/env/global Git and uses sudo for
  Ralph; it installs OpenCode but not Codex or global subagents. Never use it as
  a validation command.
- `make install` first runs `install-zsh-extensions`: clone only missing custom
  plugins and Powerlevel10k from the explicit registry in
  `scripts/install-zsh-extensions.py`. Honor `ZSH`/`ZSH_CUSTOM`, require an existing
  Oh My Zsh installation, and never pull/reset/replace existing extensions.
  Preserve custom non-Git copies with readable entry points; stop on invalid
  directories or symlinks. Tests use local Git fixtures, not live downloads.
  No CLI applications or Railway setup are included. AI-only targets stay separate.
  Before manual extension updates/removal, inspect existing copies, retain needed
  backups, and obtain scoped approval. `make clean` must not remove plugins/themes.
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
- Shared story execution and the canonical review protocol/JSON schema live in
  `ai/plugins/coding/skills/prepare-implementation/references/story-execution.md`
  and `story-review.md`. Executors load both in full relative to the advertised
  installed skill, never via checkout or hardcoded plugin-cache paths, and supply
  the full review protocol to the native reviewer wrapper.
- Ralph local staged reviews use only native OpenCode `ralph-reviewer`; Codex Goal
  uses native `story-reviewer`, never general reviewers. The generated OpenCode
  `story-reviewer` has no shell permission and is not a Ralph substitute. Preserve
  the project-local read/staged-Git-only boundary and exact JSON output. OpenCode
  enforces `steps: 3` and its exact Git allowlist. The executor explicitly maps
  RalphJSON to `three-step` and CodexGoalMarkdown to `expanded-initial`, supplying
  `Review profile` and `Pass type` on every initial/targeted packet. Each native
  wrapper requires its profile; missing, unknown, or conflicting selection blocks
  in the existing JSON schema. Never infer the harness from tools, binaries,
  paths, or role names. Profiles grant no capabilities or runtime overrides.
  The `expanded-initial` initial review permits up to 40 small read-only evidence
  calls, inventory first, then manageable patch groups and missing-section
  recovery without repeating oversized requests.
  Track changed-file/affected-contract coverage and stop when sufficient; block
  with exact missing sections if required evidence remains unavailable at the
  ceiling. This configurable reading budget is behavioral, not equivalent hard
  step or immutable sandbox/MCP enforcement. Targeted review under either profile
  retains two evidence-gathering turns and only prior findings/remediation regressions.
- `write-requirements` creates requirements; `prepare-implementation` defaults to
  `plan.json` in OpenCode and a Markdown story checklist in `PLAN.md` in Codex.
  Explicit user format requests override these defaults. OpenCode entry points
  are `/define-requirements` and `/plan-work`; neither starts execution or creates
  execution logs/memory.
  Resolve active-harness identity from trusted runtime context or the invoking
  native entry point; `ai/opencode/commands/plan-work.md` supplies the JSON default.
  Ask when routing is unavailable or ambiguous, never infer it from `PATH`,
  installed binaries, directories, environment variables, or policy headings.
- Ralph is OpenCode-only:
  `ralph --mode standard --max-iterations 10`. Invocation grants scoped execution
  and passing-story commits; no separate authorization flag is required.
  Require a clean initial Git worktree and committed `plan.json` on its `branchName`;
  reject detached HEAD and main/master. Do not create or switch branches for Ralph.
- `--auto` is unsupported and rejected. Standing authorization covers routine scoped
  implementation, necessary project dependencies, and relevant tests, not
  permission bypasses. Docker lifecycle, migrations including local/test, service
  operations, global changes, and other sensitive actions need explicit approval.
- A fully complete valid Ralph PRD exits without launching OpenCode.
  Stop files and interrupted/blocked runner state still take precedence.
- Ralph persists `running` before launch and requires a matching completed,
  retryable, or blocked outcome before continuation. See the installed skill's
  `references/ralph-control.md`. Default two recoveries per story survive restart;
  only a validated retryable candidate may enter a new bounded review cycle.
  `.ralph-stop`, malformed/missing handoffs, permission blockers, failed commits,
  timeouts, and ineffective/exhausted recovery stop future sessions. `--resume`
  requires human reconciliation and never resets counts or accepts provisional
  completion. Autonomous Ralph must not edit the ledger, clear stop files, or
  raise budgets. The separate interactive `recover-ralph` workflow defaults to
  read-only diagnosis (`ralph --status`) and preparation. Repairs require scoped
  approval. Only after an exact-action preview and explicit user confirmation may
  that interactive assistant remove the verified project-root `.ralph-stop` or
  launch the approved resume command; material state changes invalidate approval.
  It must never edit/delete the ledger, reset counters, or fabricate outcomes.
  Additional recovery budget needs a separate explicit decision via the CLI.
  Never stage stop/outcome files. Before manual cleanup inspect exact paths and
  retain needed audit evidence; `make clean` must not delete runner controls.
  Follow `docs/ralph-recovery.md`; inspection exit zero is not proof of readiness.
- Codex Goal and Ralph share the full execution, memory, review, prepared-branch,
  and per-story commit contract; task adapters use Markdown checkboxes versus JSON
  `passes`. Goal requires the plan's exact existing branch and an existing commit;
  reject detached HEAD, main/master, or mismatch before any writes. Never create
  or switch branches for either adapter. Explicit execution and story-commit scope
  authorization is required; a quoted Goal template is not permission.
- Both use the shared fast/standard/deep risk budgets: at most two read-only
  implementation advisors, budget-selected self/native staged review, one initial
  pass and at most one targeted pass in the same actual native session per attempt. Missing
  required protocol/reviewer/session, invalid memory, failed required checks,
  failed review, or failed commit stops delivery with the story pending.
- A final blocked native review stops further story review attempts. Preserve the
  candidate, incomplete status, findings/history, and consumed passes; record the
  exact blocker, required material change, and resolution evidence. Goal may resume
  that story only after verifying the change, not merely on continuation, elapsed
  time, compaction, or reviewer replacement. Preserve bounded evidence recovery
  before a final verdict and the actionable-findings initial/targeted contract.
  Carry forward existing authorization; ask only for genuinely missing authority
  or input. Another story must be independently eligible and safely isolated, or
  stop work without manufactured experiments/bookkeeping. Native Goal lifecycle
  audits do not reset story review budgets. Ralph's explicit recovery protocol and
  persisted counters remain authoritative and unchanged.
- Keep only story completion status in the task source; append execution status,
  notes, evidence, dispositions, and resumption checkpoints to `docs/progress.md`.
  Delivery requires passing checks/review and a successful authorized story commit;
  restore only the provisional completion marker on failed finalization/commit.
  Goal retains native continuation/compaction, not Ralph's external hard iteration
  controller, fresh-session loop, or completion sentinel. Record actual runtime,
  model/source, mode, limits, and reviewer session provenance; mark unknowns.
  Automatic story-boundary compaction is deferred in `docs/backlog.md`;
  do not install compaction hooks/controllers.
- Each Ralph story should fit one iteration and include typecheck acceptance criteria.
  Use `verify-interface` for browser verification of UI changes. Run relevant
  lint/typecheck/tests before committing; do not claim unavailable checks passed.
- Keep append-only review history in worktree-root `docs/progress.md` (never rewrite headers),
  bounded version-1 operational knowledge in project `memory.json` (at most 20
  patterns and 20 suppressions), and only durable repository instructions in the
  nearest `AGENTS.md`. Missing memory is normal; invalid memory blocks without
  overwrite. Update memory only after passing review, promoting reusable verified
  accepted fixes and suppressing only evidenced false positives.
- One active plan belongs to each worktree. Keep task sources and `memory.json`
  at the root; create the journal only for a permitted execution checkpoint, never
  during planning/PRD drafting. Do not read or migrate legacy execution logs.
- Completed-run archival follows the installed skill's
  `references/completed-run-archive.md`: verify all tasks/checks/reviews/commits,
  wait for Ralph runner validation and exit, preview and obtain explicit approval,
  append the final summary, copy the actual plan/journal/memory to a unique archive,
  verify contents, then remove only approved active copies. Preserve runner controls
  and unrelated work; archive commits need separate approval. Never reset journals.
- PRD replacement requires exact-path archival approval and verified preservation
  before writing the replacement. Same-PRD revisions stay scoped; requirements
  drafting never archives execution state as a side effect.

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
- Python 3.11+, Git, and POSIX process groups/flock for the Ralph supervisor;
  jq remains a shell regression-test fixture dependency, not a runner dependency
- Optional: shellcheck for linting (run manually, not automated)

## Environment Setup

Follow [README setup](README.md#setup-and-documentation) and the
[installation guide](docs/ai-configuration.md) before any authorized install.
Never overwrite an existing `$HOME/.env`:
merge missing example keys privately and export the needed values in the launching
shell. AI-only targets neither source nor synchronize it. Enabled GitHub MCP
requires `GITHUB_MCP_TOKEN`; installation never performs authentication. Restart
the selected harness after installation, and start a new Codex thread for plugins.
