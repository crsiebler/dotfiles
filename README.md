# dotfiles

A collection of configuration files for storing user preferences and preserving the state of a utility. Support for Zsh only.

## Setting Up

1. Copy the provided `env/.env.example` from this repository to your `$HOME` directory as `.env`, and fill in your own values:

   cp env/.env.example $HOME/.env
   # then edit $HOME/.env to add your secrets

2. The global opencode configuration, `ai/opencode/opencode.json`, should be copied to `$HOME/.config/opencode/opencode.json`:

    mkdir -p $HOME/.config/opencode/
    cp ai/opencode/opencode.json $HOME/.config/opencode/opencode.json

3. Run `make install` to copy all supported dotfiles to your home directory as usual.

4. **After installation:**
   - Open a new terminal, or manually run `source ~/.zshrc` to apply all settings and load environment variables from `$HOME/.env`.
   - Any changes to `$HOME/.env` require you to re-source it (`source ~/.env`) or start a new shell.

 `make install` will back up any existing files before overwriting them. Your secrets in `.env` will never be committed, and your configuration files (`.zshrc`, `.env`, and `opencode.json`) are each backed up with a timestamp-based filename prior to overwrite.

## Ralph Autonomous AI Loop

This dotfiles repository includes configuration for Ralph, an autonomous AI coding agent that can iteratively implement features from Product Requirements Documents (PRDs).

### Features

- **PRD Generation**: Use `/prd` command in OpenCode to create detailed requirements documents
- **PRD Conversion**: Use `/ralph` command to convert PRDs to JSON format for autonomous execution
- **Autonomous Implementation**: Run `ralph --max-iterations 10` to automatically implement user stories
- **Quality Assurance**: Each iteration includes type checking, linting, and testing
- **Progress Tracking**: Automatic commits and progress logging

### Setup

After running `make install`, the Ralph configuration is automatically set up:

- OpenCode skills and commands are installed to `~/.config/opencode/`
- The Ralph prompt is installed to `~/.config/opencode/ralph.md` (customizable)
- The `ralph` CLI tool is installed to `/usr/bin/ralph`

### Usage

1. **Create a PRD**: In any project directory, run OpenCode and use `/prd` to generate requirements
2. **Convert to JSON**: Use `/ralph` to create `prd.json` from your PRD
3. **Run Autonomous Loop**: Execute `ralph --max-iterations 10` to start implementation
4. **Monitor Progress**: Check `progress.txt` for detailed logs and `prd.json` for completion status

### Requirements

- OpenCode must be installed and configured with API keys
- Projects must be git repositories
- `grok-code-fast-1` model should be available for optimal performance

## Removing Backup Files (Cleanup)

If you wish to remove the backup files created by `make install` (such as `.zshrc.backup.*`, `.env.backup.*`, `opencode.json.backup.*`, and `ralph.backup.*`), run the following command:

    make clean

This will delete all backup versions of `.zshrc`, `.env`, `opencode.json`, and `ralph`. Use this if you want to clean up your home or configuration folders after verifying your new setup is working as expected.

---
