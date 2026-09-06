# dotfiles

A collection of configuration files for storing user preferences and preserving the state of a utility. Support for Zsh only.

## Setup and documentation

- [AI configuration, connections, and validation](docs/ai-configuration.md)
- [Manual removal of old AI files](docs/remove-old-ai-files.md)
- [Native agent authoring and rendering](docs/agent-authoring.md)
- [Repository contributor instructions](AGENTS.md)

### Requirements

- Shell setup: Zsh, Oh My Zsh, standard Unix tools, and `python3` for environment synchronization.
- AI installer: Python 3.11+ (`PYTHON` defaults to `python3.11`).
- Codex installation: Codex CLI **0.153.4**.
- OpenCode skill installation: the `skills` CLI already on `PATH`, plus OpenCode to use the result.
- Source validation and agent rendering: Python 3.11+. Ralph requires `jq` and Git;
  its review regression test also uses Ruby to validate native reviewer YAML.

The installer does not download missing tools. If `skills` is missing, arrange
an explicitly approved installation; there is no silent `npx` fallback.

### Choose an installation scope

Run validation from this checkout without credentials. Before choosing one of the
installation targets, review the [installation guide](docs/ai-configuration.md#installation-and-merge-behavior),
authorize installation, and securely export the required `GITHUB_MCP_TOKEN`:

```sh
make validate-ai       # Local source validation only; no harness or MCP starts
make install-codex     # Codex configuration, local plugins, native roles
make install-opencode  # OpenCode configuration, copied skills, agents, commands
make install-ai        # Both AI harnesses; no shell/env/git setup or binaries
```

The four checkout-local `craft` plugins are `coding`, `reporting`, `researching`,
and `delegating`. The `researching` plugin provides provider-agnostic `search-web`
with conditional Exa MCP guidance.
The single harness-agnostic personal policy, [`ai/AGENTS.md`](ai/AGENTS.md), is
copied byte-for-byte to both user-level `AGENTS.md` destinations. Root
[`AGENTS.md`](AGENTS.md) remains separate, repository-only guidance.
GitHub, Exa, and Context7 are globally enabled; Jira/Rovo and PostgreSQL remain off.
AWS and Elastic MCP definitions are intentionally absent from both source configs.
See the guide for credentials, project opt-in, profiles, and merge behavior.

For the broader shell setup, `make install` copies shell/alias files, creates or
synchronizes `$HOME/.env`, sets the global Git excludes file, calls
`install-opencode`, and installs Ralph with `sudo`. It does **not** install Codex
or a global `subagents`. It can change shell/env/git files before AI preflight
fails, so resolve prerequisites first. Not every overwritten shell
file or binary is backed up.

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

## Sprite Generation

This repository includes a `/create-sprite` OpenCode command for generating
pixel-art sprite sheets through a ChatGPT subscription and integrating approved
assets into projects when requested, including Godot 4. Asset-only work needs
neither a Godot project nor binary; Godot guidance is loaded only for Godot
requests or relevant project context.

The workflow installs:

- `opencode-gpt-imagegen@0.1.9`, an unofficial OpenCode plugin that exposes the
  `gpt_imagegen` tool through the existing ChatGPT OAuth session
- `sprite-artist`, the specialized generation and integration agent
- `create-sprites`, the reusable asset planning and prompt skill
- `/create-sprite`, the command entry point

### Requirements

- OpenCode authenticated with OpenAI ChatGPT OAuth through `opencode auth login`
- A ChatGPT plan that permits image generation
- Godot 4 available as `godot` for project integration and headless validation
- An active Godot project with `project.godot` when scene integration is requested

No `OPENAI_API_KEY` is required for the plugin's subscription-backed generation
path. Image calls consume ChatGPT subscription capacity. The plugin is unofficial
and reads OpenCode's OAuth data from its standard authentication store.

After running `make install-opencode`, quit and restart OpenCode so it installs and loads
the configured plugin and prompt assets.

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

## Ralph Autonomous AI Loop

Ralph's implementation loop runs through **OpenCode only**.

1. Use `write-requirements` (OpenCode `/define-requirements`) to create a PRD.
2. Use `prepare-implementation` (OpenCode `/plan-work`) to create `plan.json`.
3. Prepare a Git worktree with an existing commit on exactly the PRD's
   `branchName`, not detached HEAD, `main`, or `master`. Ralph does not switch branches.
4. With OpenCode configured and `jq` available, run:

   ```sh
   ralph --mode standard --max-iterations 10
   ```

`make install` installs the executable; AI-only targets do not. The checkout
entry point is `bin/ralph`. `--auto` is unsupported and rejected. Standing
authorization covers routine scoped implementation, necessary project
dependencies, and relevant tests, not permission bypasses. Docker lifecycle,
migrations (including local/test), global changes, service operations, and other
sensitive actions still need separate approval.

Modes are `fast` (minimal review for low-risk work), `standard` (risk-based), and
`deep` (bounded reviewer for every story). Optional story notes recommend agents,
not mandatory delegation. OpenCode defaults to `openai/gpt-5.6-sol-fast`;
`--model` must match the allowlist in `bin/ralph` and an available provider model.
The interactive Astra profile does not expand Ralph's model allowlist.

The review gate uses self-review where allowed or the dedicated three-step,
project-local `ralph-reviewer`, with at most one same-session follow-up after
substantive fixes. It never substitutes a general-purpose reviewer. Checks include
relevant typecheck, lint, tests, and `verify-interface` for UI changes.

`progress.txt` is the append-only handoff and review history. Optional
`memory.json` retains at most 20 validated patterns and 20 false-positive
suppressions; its initial absence is normal. Only durable rules belong in the
nearest `AGENTS.md`. `plan.json` tracks story completion.

## Codex Story Checklists

Invoke `prepare-implementation` in Codex to turn approved requirements into
`PLAN.md`: ordered user stories, unchecked acceptance criteria, verification,
independent review, and evidence checkpoints. The same skill defaults to Ralph's
`plan.json` in OpenCode. Explicit format requests take precedence; no format question
is needed when trusted runtime context or the invoking native entry point identifies
the active harness. OpenCode's `ai/opencode/commands/plan-work.md` supplies the JSON
default. If routing is unavailable or ambiguous, the skill asks rather than
inferring the harness from `PATH`, installed tools, folders, or environment variables.

Planning does not start execution. After reviewing the plan, you can use native
`/goal` to continue through its stories in the same thread. See
[Codex goals](docs/codex-goals.md) for the handoff and authorization boundaries.
Automatic story-boundary compaction is [backlogged](docs/backlog.md); no custom
hook runs during normal development.

## Native agents and discovery

The canonical custom agents are **127 native TOML files** in `ai/codex/agents/`.
Codex receives all 127 sources byte-for-byte. OpenCode receives 127 generated
Markdown agents plus three unchanged native sources from `ai/opencode/agents/`:
`sprite-artist`, `ralph`, and `ralph-reviewer`, for **130 installed agents**.
Those three native Markdown roles are OpenCode-only.

PowerShell scripting, modules, and profiles use `powershell-expert`; GUI/TUI work
uses `powershell-ui-architect`, and dedicated read-only control assessment uses
`powershell-security-hardening`. After an authorized installation, verify the
replacement, preserve customized old copies, then approve each exact retired path
before manual removal in either harness. Follow the
[PowerShell cleanup steps](docs/remove-old-ai-files.md#consolidated-powershell-agents);
the installer performs no automatic deletion or alias migration.
Seven inspection roles, including `powershell-security-hardening`, use native
`sandbox_mode = "read-only"` and read-only role guidance.
Codex permits runtime-authorized read-only shell inspection; OpenCode
renders a more restrictive deny-by-default `read`/`glob`/`grep` allowlist. These
are not equivalent sandbox or MCP guarantees: Codex parent runtime overrides
apply, and MCP approvals are independent. See [agent authoring](docs/agent-authoring.md)
for role boundaries and renderer semantics.

Use native delegation to invoke agents; reading a definition is not delegation.
OpenCode `/find-agents` loads `use-subagents` for discovery; the skill bundles
the unchanged `subagents` helper. `/ship` prepares a PR with preview and explicit
approval; it does not push implicitly. `/review-pr` remains the review command.
From this checkout:

```sh
helper=ai/plugins/delegating/skills/use-subagents/scripts/subagents
sh "$helper" --harness opencode list
sh "$helper" --harness opencode search security
sh "$helper" --harness opencode fetch cli-developer
sh "$helper" help
```

## Removing backup files

1. Verify the installed configuration and retain backups needed for rollback.
2. Review adjacent `.backup.<timestamp>` files and changed OpenCode skill assets
   under `.install-ai-backups/<timestamp>/skills/` in the configuration root.
   The broad installer backs up `.zshrc`. Existing `.env` files are synchronized
   by appending missing keys/exports without creating backups.
3. After reviewing all matching `.zshrc` backups, run `make clean` to remove
   only `$HOME/.zshrc.backup.*`. It preserves active files, existing `.env`
   backups, and all AI configuration/backups.
4. For AI files and backups, follow the [manual removal guide](docs/remove-old-ai-files.md).
   Approve and remove only reviewed paths; never delete a whole configuration root.
5. Separately review the obsolete installed command and sprite-agent paths listed
   in that guide. Renames install no compatibility aliases or automatic cleanup;
   preserve the Ralph executable, native Ralph agents, and project artifacts.
6. Review retained installed AWS/Elastic MCP entries and old PostgreSQL Docker
   fields separately. Back up customizations and approve exact config edits before
   removal; preserve approval rules, active `POSTGRESQL_CONNECTION_STRING`, and
    exports still used elsewhere. Source removal does not delete installed entries.
7. For `use-exa` renamed to `search-web`, verify the replacement after authorized
   installation or Codex native plugin refresh, preserve customized old copies,
   and approve exact paths before manual cleanup. Restart the harness and start
   a new Codex thread; follow the [rename steps](docs/remove-old-ai-files.md#renamed-web-research-skill).
