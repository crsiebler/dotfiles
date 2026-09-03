# dotfiles

A collection of configuration files for storing user preferences and preserving the state of a utility. Support for Zsh only.

## Requirements

- Python 3.8+ (required by `make install` to synchronize `~/.env` with
  missing keys from `env/.env.example`)

## Setting Up

1. Copy the provided `env/.env.example` from this repository to your `$HOME` directory as `.env`, and fill in your own values:

   cp env/.env.example $HOME/.env
   # then edit $HOME/.env to add your secrets

2. The OpenCode user configuration, bundled skills, and commands should be copied into `$HOME/.config/opencode/`:

   ```bash
   mkdir -p $HOME/.config/opencode/
   cp ai/opencode/opencode.json $HOME/.config/opencode/opencode.json
   cp ai/opencode/tui.json $HOME/.config/opencode/tui.json
   mkdir -p $HOME/.config/opencode/skills/
   cp -R ai/opencode/skills/. $HOME/.config/opencode/skills/
   mkdir -p $HOME/.config/opencode/agents/
   cp -R ai/opencode/agents/. $HOME/.config/opencode/agents/
   mkdir -p $HOME/.config/opencode/commands/
   cp -R ai/opencode/commands/. $HOME/.config/opencode/commands/
   ```

3. Run `make install` to copy all supported dotfiles to your home directory as usual.

4. **After installation:**
   - Open a new terminal, or manually run `source ~/.zshrc` to apply all settings and load environment variables from `$HOME/.env`.
   - Any changes to `$HOME/.env` require you to re-source it (`source ~/.env`) or start a new shell.

`make install` will back up any existing files before overwriting them. Your secrets in `.env` will never be committed, and your configuration files (`.zshrc`, `.env`, `opencode.json`, OpenCode skills, agents, and commands) are backed up with timestamp-based names prior to overwrite.

## OpenCode PR Review Command

This repository includes a manual `/review-pr` OpenCode command that reviews GitHub pull requests using OpenCode's configured provider/model layer. It does not make direct OpenAI API calls.

### Setup

After running `make install`, the PR review assets are installed automatically:

- `/review-pr` command: `~/.config/opencode/commands/review-pr.md`
- GitHub PR review standards are self-contained in the command file.

### Requirements

- OpenCode configured with a working provider/model
- GitHub CLI (`gh`) authenticated via `gh auth login`; verify keyring
  authentication with `gh auth status`. No GitHub token environment variable
  is required.
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

## Godot Sprite Generation

This repository includes a `/godot-sprite` OpenCode command for generating
pixel-art sprite sheets through a ChatGPT subscription and integrating approved
assets into Godot 4 projects.

The workflow installs:

- `opencode-gpt-imagegen@0.1.9`, an unofficial OpenCode plugin that exposes the
  `gpt_imagegen` tool through the existing ChatGPT OAuth session
- `godot-sprite-artist`, the specialized generation and integration agent
- `godot-sprite-forge`, the reusable asset planning and prompt skill
- `/godot-sprite`, the command entry point

### Requirements

- OpenCode authenticated with OpenAI ChatGPT OAuth through `opencode auth login`
- A ChatGPT plan that permits image generation
- Godot 4 available as `godot` for project integration and headless validation
- An active Godot project with `project.godot` when scene integration is requested

No `OPENAI_API_KEY` is required for the plugin's subscription-backed generation
path. Image calls consume ChatGPT subscription capacity. The plugin is unofficial
and reads OpenCode's OAuth data from its standard authentication store.

After running `make install`, quit and restart OpenCode so it installs and loads
the configured plugin and prompt assets.

### Usage

```text
/godot-sprite create a four-direction forest ranger with idle and walk animations

/godot-sprite create a side-view lightning knight with idle, run, attack, hurt, and death animations

/godot-sprite --plan-only create a six-frame fire elemental boss idle
```

The agent previews its asset contract and planned image calls before invoking
`gpt_imagegen`. Generated images and references must remain inside the active
workspace. The `--plan-only` option produces prompts and an integration plan
without generating images or changing project files.

## Ralph Autonomous AI Loop

This dotfiles repository includes configuration for Ralph, an autonomous AI coding agent that can iteratively implement features from Product Requirements Documents (PRDs).

### Features

- **PRD Generation**: Use the PRD skill in OpenCode to create detailed requirements documents
- **PRD Conversion**: Use the Ralph skill in OpenCode to convert PRDs to JSON format for autonomous execution
- **Autonomous Implementation**: Run `ralph --max-iterations 10` to automatically implement user stories
- **Scoped Auto Approval**: Add `--auto` to pre-authorize required project-local development operations in every iteration
- **Execution Modes**: Use `ralph --mode fast|standard|deep` to control Ralph's agent budget and review depth
- **Model Selection**: Use `ralph --model provider/model` to select an available OpenCode model
- **Recommended Agents**: Story `notes` can list optional `@agent-name` recommendations that Ralph may invoke before implementation based on story risk and mode
- **Quality Assurance**: Each iteration includes type checking, linting, and testing
- **Mode-Aware Review Gate**: Each staged story gets self-review or one bounded `ralph-reviewer` pass based on mode and risk before commit
- **Bounded Read-Only Review**: The Ralph reviewer receives compact story context and uses at most two read-only inspection turns before its final holistic review; all mutation, browser, web, MCP, external-directory, and delegation tools remain denied
- **Iterative Feedback**: One targeted re-review can resume the initial reviewer session after Ralph fixes blocking findings
- **Bounded Review Memory**: Validated review patterns and false-positive suppressions are stored project-locally in `memory.json`
- **Self-Contained Review Standards**: Ralph includes local staged-change review standards directly in its agent so target-project agents do not need access to `~/.config/opencode/`
- **Progress Tracking**: Automatic commits and progress logging

### Setup

After running `make install`, Ralph configuration is automatically set up:

- OpenCode skills are installed to `~/.config/opencode/skills/`
- `ai/opencode/opencode.json` is installed to `~/.config/opencode/opencode.json`
- `ai/opencode/tui.json` is installed to `~/.config/opencode/tui.json`
- `ai/opencode/skills/*/SKILL.md` files are installed under `~/.config/opencode/skills/`
- `ralph-reviewer` is installed to `~/.config/opencode/agents/ralph-reviewer.md`
- The Ralph primary agent is installed to `~/.config/opencode/agents/ralph.md` (customizable)
- The `ralph` CLI tool is installed to `/usr/local/bin/ralph`

### Usage

1. **Create a PRD**: In any project directory, open OpenCode and use the PRD skill to generate requirements
2. **Convert to JSON**: Use the Ralph skill to create `prd.json` from your PRD
3. **Run Autonomous Loop**: Execute `ralph --auto --mode standard --max-iterations 10` to start implementation with scoped project-local approval
4. **Select a Model (optional)**: Add `--model openai/gpt-5.4` or another supported model
5. **Monitor Progress**: Check `progress.txt` for detailed logs, `memory.json` for bounded validated review knowledge, and `prd.json` for completion status

For a single direct OpenCode invocation, select the same primary agent with
`opencode run --agent ralph "your task"`. The `/ralph` command is separate and
converts PRDs to `prd.json`; it does not run the autonomous implementation loop.

Supported Ralph models:

- `opencode/big-pickle`
- `opencode/ling-3.0-flash-fin-free`
- `opencode/mimo-v2.5-free`
- `opencode/muse-spark-1.2-contributor-free`
- `opencode/nemotron-3-ultra-free`
- `opencode/nemotron-3.5-lightning-free`
- `mlx/mlx-community/Qwen3-Coder-30B-A3B-Instruct-4bit`
- `openai/gpt-5.3-codex-spark`
- `openai/gpt-5.4`
- `openai/gpt-5.4-fast`
- `openai/gpt-5.4-mini`
- `openai/gpt-5.4-mini-fast`
- `openai/gpt-5.5`
- `openai/gpt-5.5-fast`
- `openai/gpt-5.6-luna`
- `openai/gpt-5.6-luna-fast`
- `openai/gpt-5.6-sol`
- `openai/gpt-5.6-sol-fast`
- `openai/gpt-5.6-terra`
- `openai/gpt-5.6-terra-fast`

Ralph modes:

- `fast`: minimizes implementation agents and specialist reviews; best for low-risk stories
- `standard`: default risk-based agent and review budget
- `deep`: broader specialist help for complex or high-risk stories

Ralph keeps review data in three layers. `progress.txt` is the append-only audit
trail of findings and dispositions. `memory.json` retains at most 20
validated patterns and 20 false-positive suppressions for later iterations.
Its absence before the first passing review is normal; Ralph uses empty memory
in process and creates the file only after review succeeds.
Durable repository conventions may be promoted to the nearest `AGENTS.md`, but
temporary findings, counters, and story-specific review details must remain out
of agent instruction files.

`ralph --auto` passes OpenCode's `--auto` option to every fresh iteration and
pre-authorizes operations required by the active story, including dependency
installation, project configuration, local development containers, local/test
migrations, quality checks, browser verification, and the story commit. Explicit
OpenCode denials still apply. The option does not authorize production access,
secrets, changes outside the worktree, destructive database or Docker volume
operations, history rewriting, protected-branch pushes, disabled safeguards, or
out-of-scope work under Ralph's instructions. Ralph records whether auto approval
was enabled in each `progress.txt` entry.

### Requirements

- OpenCode must be installed and configured with API keys
- `jq` must be installed for reliable `prd.json` completion checks
- Projects must be git repositories
- The default `openai/gpt-5.6-sol-fast` model, or another supported model, should be available

## Subagents CLI Tool

This dotfiles repository includes a CLI tool for managing OpenCode subagents, providing access to 130+ specialized agents organized by category.

### Features

- **List**: View all configured subagents organized by category (Backend, Frontend, DevOps, Security, etc.)
- **Search**: Find subagents by keyword in names, descriptions, and tools
- **Fetch**: Retrieve complete agent definitions with capabilities and tool descriptions
- **Global Access**: Works from any directory - no path context issues
- **Pure Bash**: No Python dependency required for operation

### Available Agent Categories

- **Backend Development**: API design, database architecture, performance optimization
- **Frontend Development**: React, Vue, Angular, UI/UX implementation
- **DevOps & Infrastructure**: CI/CD, containerization, cloud deployment
- **Security**: Security auditing, vulnerability assessment, compliance
- **Data & Analytics**: Data engineering, machine learning, business intelligence
- **Mobile Development**: iOS, Android, cross-platform development
- And 6+ additional specialized categories

### Setup

After running `make install`, the subagents CLI is automatically installed to `/usr/local/bin/subagents` and can access agent files from `~/.config/opencode/agents/`.

### Usage

```bash
# List all agents by category
subagents list

# Search for specific agents
subagents search security
subagents search react
subagents search database

# Fetch complete agent definition
subagents fetch frontend-developer
subagents fetch cli-developer

# Get help
subagents help
```

### Integration with OpenCode

The subagents CLI integrates with the OpenCode subagents skill. When you use that skill to list, search, or fetch agents in OpenCode, it internally calls the global `subagents` command to access agent definitions regardless of your current working directory.

## Removing Backup Files (Cleanup)

If you wish to remove the backup files created by `make install` (such as `.zshrc.backup.*`, `.env.backup.*`, `opencode.json.backup.*`, `skills.backup.*`, `agents.backup.*`, `commands.backup.*`, `ralph.backup.*`, and `subagents.backup.*`), run the following command:

    make clean

This will delete all backup versions of `.zshrc`, `.env`, `opencode.json`, OpenCode skills, agents, commands, `ralph`, and `subagents`. Use this if you want to clean up your home or configuration folders after verifying your new setup is working as expected.

---
