# dotfiles

A collection of configuration files for storing user preferences and preserving the state of a utility. Support for Zsh only.

## Setup and documentation

- [AI configuration, connections, and validation](docs/ai-configuration.md)
- [Manual removal of old AI files](docs/remove-old-ai-files.md)
- [Native agent authoring and rendering](docs/agent-authoring.md)
- [Diagnosing and recovering stopped Ralph runs](docs/ralph-recovery.md)
- [Repository contributor instructions](AGENTS.md)

### Requirements

- Shell setup: Zsh, Oh My Zsh, standard Unix tools, and `python3` for environment synchronization.
- AI installer: Python 3.11+ (`PYTHON` defaults to `python3.11`).
- Codex installation: Codex CLI **0.153.4**.
- OpenCode skill installation: the `skills` CLI already on `PATH`, plus OpenCode to use the result.
- Source validation and agent rendering: Python 3.11+. Ralph requires Python 3.11+, POSIX, and Git;
  its review regression test also uses Ruby to validate native reviewer YAML.

The AI installer does not download missing tools. If `skills` is missing, arrange
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

For the broader shell setup, `make install` first installs missing custom Zsh
plugins and the configured theme, then copies shell/alias files, creates or
synchronizes `$HOME/.env`, sets the global Git excludes file, calls
`install-opencode`, and installs Ralph with `sudo`. It does **not** install Codex
or a global `subagents`. It can change shell/env/git files before AI preflight
fails, so resolve prerequisites first. Not every overwritten shell
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
3. Prepare a clean Git worktree with `plan.json` committed on exactly the plan's
   `branchName`, not detached HEAD, `main`, or `master`. Ralph does not switch branches.
4. With OpenCode configured and Python 3.11+ available, run:

   ```sh
   ralph --mode standard --max-iterations 10
   ```

`make install` installs the executable; AI-only targets do not. The checkout
entry point is the single-file Python supervisor `bin/ralph`. `--auto` and the old
`--authorize-story-commits` flag are unsupported. Invoking `ralph` itself
authorizes passing-story commits, routine scoped implementation, necessary project
dependencies, and relevant tests, not permission bypasses. Docker lifecycle,
migrations (including local/test), global changes, service operations, and other
sensitive actions still need separate approval.

Modes are `fast` (minimal review for low-risk work), `standard` (risk-based), and
`deep` (bounded reviewer for every story). Optional story notes recommend agents,
not mandatory delegation. OpenCode defaults to `openai/gpt-5.6-sol-fast`;
`--model` must match the allowlist in `bin/ralph` and an available provider model.
The interactive Astra profile does not expand Ralph's model allowlist.

Both Ralph and Codex Goal follow the full shared
[story execution contract](ai/plugins/coding/skills/prepare-implementation/references/story-execution.md)
and [review protocol/schema](ai/plugins/coding/skills/prepare-implementation/references/story-review.md).
Executors load both references in full from the advertised installed
`prepare-implementation` skill, not checkout paths, and pass the full review
protocol to the reviewer. Ralph's review gate uses self-review where allowed or
the dedicated three-step, project-local `ralph-reviewer`, with at most one same-session follow-up after
substantive fixes. It never substitutes a general-purpose reviewer. Checks include
relevant typecheck, lint, tests, and `verify-interface` for UI changes.

Worktree-root `docs/progress.md` is the append-only handoff and review history. Optional
version-1 `memory.json` retains at most 20 validated patterns and 20 evidenced
false-positive suppressions; its initial absence is normal, invalid memory blocks.
Memory changes follow passing review; reusable accepted fixes require passing
verification before promotion. Only durable rules belong in the nearest
`AGENTS.md`. `plan.json` tracks story completion, not execution notes.
Delivery requires passing checks/review and a successful explicitly authorized
story commit. Failed finalization or commit leaves the story pending, restoring
only its provisional completion marker and preserving unrelated work.

### Completed-run archives

Use one active plan per worktree. `PLAN.md` or `plan.json` and `memory.json` remain
at the root; the journal is `docs/progress.md`, independent of a custom plan path.
Neither workflow reads or migrates legacy execution logs. PRDs retain requirements
and open questions, not implementation checkpoints.

Both workflows use the [completed-run archive procedure](ai/plugins/coding/skills/prepare-implementation/references/completed-run-archive.md):

1. Verify all tasks, required checks/reviews, and story commits. For Ralph, wait
   until the runner validates completion and exits before changing active state.
2. Preview the final summary, unique `archive/YYYY-MM-DD-feature-name/` destination,
   exact plan/journal/memory paths, and active-copy removals; obtain explicit approval.
3. Append the final summary, copy existing run artifacts with relative paths intact,
   and verify identical contents before removing approved active copies.
4. Preserve PRDs, unrelated work, and Ralph controls. Do not reset the journal or
   create replacement state. Any archive commit needs separate authorization.

Archival is manual, not automatic runner behavior. Memory is archived with its run;
new execution starts fresh. PRD replacement separately requires approval to archive
the existing PRD and verified preservation before replacement. Drafting requirements
never archives execution state as a side effect.

### Stops, crashes, and bounded recovery

Before each paid session the runner atomically records `running` state in
per-worktree Git metadata. A successful OpenCode exit alone cannot launch another
session: the agent must write a matching iteration outcome. A `completed` outcome
requires a new descendant commit with the selected story completed and no pending
candidate changes. A `retryable` outcome keeps the story incomplete, preserves its
work, and supplies unresolved finding IDs, attempted fix, evidence, and a concrete
next approach. The next session continues that same candidate and gets one new
bounded review cycle. Missing handoffs, human blockers, crashes, failed commits,
and repeated ineffective recovery stop instead of automatically consuming usage.

Default recovery allowance is **two additional sessions per story**, persisted
across invocations. `--max-story-retries 0..5` explicitly adjusts that allowance,
never resets consumed retries. `--max-iterations` also caps sessions per invocation.
For a 30-minute wall-clock limit per session, for example:

```sh
ralph --mode standard --max-iterations 10 --iteration-timeout 1800
```

Timeout defaults to `0` (unlimited); it is not provider-specific quota detection.
Timeout, Ctrl+C, or SIGTERM stops future sessions and cleans up the managed process
group. Processes that deliberately escape the group are not covered.

Create `.ralph-stop` at the worktree root to request a stop, including termination
of the currently managed session. Ralph never removes it. Before resuming, inspect
`docs/progress.md`, the latest `.ralph-outcome-<id>.json`, and the candidate changes;
resolve the blocker and clear the stop file yourself, or authorize the separate
interactive recovery assistant to remove that exact file after preview. Then use
`ralph --resume` only after reconciliation and launch approval.
It preserves retry counts and cannot accept uncommitted completion markers.
An interrupted ledger or changed candidate requires this explicit reconciliation.
A validated ready handoff resumes without `--resume` only if its snapshot matches.

Control artifacts are not story files: never stage `.ralph-stop` or the exact
`.ralph-outcome-<32-lowercase-hex-ID>.json` files. They are excluded from runner
snapshots but refused if tracked. Review and retain needed audit copies before
separately approved exact-path cleanup. State is located with
`git rev-parse --git-path ralph/state.json`; do not delete it to reset retry budgets.
The lock prevents concurrent runners, but the ledger is not protected from an
unrestricted same-user agent. A different plan requires manual state reconciliation.
`make clean` does not remove these controls, outcomes, or execution history.

### Interactive recovery

Run `ralph --status` for a read-only snapshot of state, attempts, remaining
recoveries, and detectable blockers. It never launches a model or writes runner
state. Exit zero means it produced a diagnosis, not that resumption is approved;
runtime prerequisites and the technical fix still need verification.

Use OpenCode `/recover-ralph`, or ask another harness's primary assistant to load
the `recover-ralph` skill, to assess the stop and propose a bounded repair. The
default endpoint is a readiness report, not an automatic restart. Repairs require
scoped approval; removing the stop file and launching the exact resume command
require separately previewed explicit confirmation. The autonomous Ralph agent
cannot clear its own stop, and no helper may reset the ledger or retry counters.
See the [recovery runbook](docs/ralph-recovery.md) for the full process and examples.

## Codex Story Checklists

Invoke `prepare-implementation` in Codex to turn approved requirements into
`PLAN.md`: ordered user stories, unchecked acceptance criteria, verification,
budget-selected staged review, and completion checkboxes. Execution status,
implementation notes, evidence, and resumption checkpoints go in append-only `docs/progress.md`, not
growing sections in `PLAN.md`. The same skill defaults to Ralph's
`plan.json` in OpenCode. Explicit format requests take precedence; no format question
is needed when trusted runtime context or the invoking native entry point identifies
the active harness. OpenCode's `ai/opencode/commands/plan-work.md` supplies the JSON
default. If routing is unavailable or ambiguous, the skill asks rather than
inferring the harness from `PATH`, installed tools, folders, or environment variables.

Planning does not start execution or create `docs/progress.md`/`memory.json`. After
reviewing the plan, explicitly authorize scoped implementation, necessary project
dependencies, checks, and story commits when launching an actual native `/goal`.
A quoted template or prepared plan grants no permission. Goal uses the same
execution/memory/review/branch/commit contract as Ralph, with Markdown rather than
JSON task status. Require an existing commit and the plan's exact prepared branch;
reject detached HEAD, `main`, `master`, and mismatch without branch repair.

Both use the same fast/standard/deep risk budgets, at most two read-only advisors,
and one initial staged review plus at most one targeted same-session pass. Codex
requires native `story-reviewer` when the budget selects native review; missing
protocol, required reviewer/session, invalid memory, or failed checks/review/commit
stops delivery with the story pending. It is not a general-reviewer fallback.
Goal retains native continuation and compaction, not Ralph's external hard
iteration limit, fresh-session loop, or completion sentinel. OpenCode's reviewer
has `steps: 3`; Codex's tool-turn budget is behavioral, not a hard cap.
See [Codex goals](docs/codex-goals.md) for the handoff and authorization boundaries.
Automatic story-boundary compaction is [backlogged](docs/backlog.md); no custom
hook runs during normal development.

## Native agents and discovery

The canonical custom agents are **128 native TOML files** in `ai/codex/agents/`.
Codex receives all 128 sources byte-for-byte. OpenCode receives 128 generated
Markdown agents plus three unchanged native sources from `ai/opencode/agents/`:
`sprite-artist`, `ralph`, and `ralph-reviewer`, for **131 installed agents**.
Those three native Markdown roles are OpenCode-only.

PowerShell scripting, modules, and profiles use `powershell-expert`; GUI/TUI work
uses `powershell-ui-architect`, and dedicated read-only control assessment uses
`powershell-security-hardening`. After an authorized installation, verify the
replacement, preserve customized old copies, then approve each exact retired path
before manual removal in either harness. Follow the
[PowerShell cleanup steps](docs/remove-old-ai-files.md#consolidated-powershell-agents);
the installer performs no automatic deletion or alias migration.
Eight inspection roles, including `powershell-security-hardening` and
`story-reviewer`, use native
`sandbox_mode = "read-only"` and read-only role guidance.
Codex permits runtime-authorized read-only shell inspection; OpenCode
renders a more restrictive deny-by-default `read`/`glob`/`grep` allowlist. These
are not equivalent sandbox or MCP guarantees: Codex parent runtime overrides
apply, and MCP approvals are independent. See [agent authoring](docs/agent-authoring.md)
for role boundaries and renderer semantics.

The new `story-reviewer.toml` is rendered generically for OpenCode too, but that
read/glob/grep-only counterpart cannot replace Ralph's native `ralph-reviewer`
with its exact staged-Git allowlist. Adding this role retires no installed paths.

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
