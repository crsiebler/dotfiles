# dotfiles

A collection of configuration files for storing user preferences and preserving the state of a utility. Support for Zsh only.

## Setting Up

1. Copy the provided `env/.env.example` from this repository to your `$HOME` directory as `.env`, and fill in your own values:

   cp env/.env.example $HOME/.env
   # then edit $HOME/.env to add your secrets

2. The OpenCode user configuration and bundled skills should be copied into `$HOME/.config/opencode/`:

     mkdir -p $HOME/.config/opencode/
     cp ai/opencode/opencode.json $HOME/.config/opencode/opencode.json
     mkdir -p $HOME/.config/opencode/skills/
     cp -R ai/opencode/skills/. $HOME/.config/opencode/skills/

3. Run `make install` to copy all supported dotfiles to your home directory as usual.

4. **After installation:**
   - Open a new terminal, or manually run `source ~/.zshrc` to apply all settings and load environment variables from `$HOME/.env`.
   - Any changes to `$HOME/.env` require you to re-source it (`source ~/.env`) or start a new shell.

 `make install` will back up any existing files before overwriting them. Your secrets in `.env` will never be committed, and your configuration files (`.zshrc`, `.env`, `opencode.json`, and OpenCode skills) are backed up with timestamp-based names prior to overwrite.

## Ralph Autonomous AI Loop

This dotfiles repository includes configuration for Ralph, an autonomous AI coding agent that can iteratively implement features from Product Requirements Documents (PRDs).

### Features

- **PRD Generation**: Use the PRD skill in OpenCode to create detailed requirements documents
- **PRD Conversion**: Use the Ralph skill in OpenCode to convert PRDs to JSON format for autonomous execution
- **Autonomous Implementation**: Run `ralph --max-iterations 10` to automatically implement user stories
- **Quality Assurance**: Each iteration includes type checking, linting, and testing
- **Progress Tracking**: Automatic commits and progress logging

### Setup

After running `make install`, Ralph configuration is automatically set up:

- OpenCode skills are installed to `~/.config/opencode/skills/`
- `ai/opencode/opencode.json` is installed to `~/.config/opencode/opencode.json`
- `ai/opencode/skills/*/SKILL.md` files are installed under `~/.config/opencode/skills/`
- The Ralph prompt is installed to `~/.config/opencode/ralph.md` (customizable)
- The `ralph` CLI tool is installed to `/usr/local/bin/ralph`

### Usage

1. **Create a PRD**: In any project directory, open OpenCode and use the PRD skill to generate requirements
2. **Convert to JSON**: Use the Ralph skill to create `prd.json` from your PRD
3. **Run Autonomous Loop**: Execute `ralph --max-iterations 10` to start implementation
4. **Monitor Progress**: Check `progress.txt` for detailed logs and `prd.json` for completion status

### Requirements

- OpenCode must be installed and configured with API keys
- Projects must be git repositories
- `grok-code-fast-1` model should be available for optimal performance

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

If you wish to remove the backup files created by `make install` (such as `.zshrc.backup.*`, `.env.backup.*`, `opencode.json.backup.*`, `skills.backup.*`, `ralph.backup.*`, and `subagents.backup.*`), run the following command:

    make clean

This will delete all backup versions of `.zshrc`, `.env`, `opencode.json`, OpenCode skills, `ralph`, and `subagents`. Use this if you want to clean up your home or configuration folders after verifying your new setup is working as expected.

---
