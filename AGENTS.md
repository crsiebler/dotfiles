# AGENTS.md - Dotfiles Repository Guidelines

This document provides guidelines for agents working in this dotfiles repository. These dotfiles contain shell configurations, aliases, and scripts primarily for Zsh environments.

## Ralph Autonomous AI Loop

This repository includes configuration for Ralph, an autonomous AI coding agent that iteratively processes user stories from Product Requirements Documents (PRDs) until completion.

### Ralph Setup

- **Skills**: PRD generation (`ai/opencode/skills/prd/SKILL.md`) and PRD-to-JSON conversion (`ai/opencode/skills/ralph/SKILL.md`)
- **Commands**: `/prd` for creating PRDs, `/ralph` for converting PRDs to JSON format
- **CLI Tool**: `ralph` command installed to `/usr/bin/ralph` with `--max-iterations` option
- **Configuration**: OpenCode skills and commands installed to `~/.config/opencode/`

### Using Ralph

1. **Create a PRD**: Use `/prd` command in OpenCode to generate requirements
2. **Convert to JSON**: Use `/ralph` command to create `prd.json` from the PRD
3. **Run Autonomous Loop**: Execute `ralph --max-iterations 10` in your project directory
4. **Monitor Progress**: Check `progress.txt` for iteration logs and `prd.json` for completion status

### Ralph Workflow

- Reads `prd.json` for user stories
- Implements highest-priority incomplete story
- Runs quality checks (lint, typecheck, test)
- Commits with format: `feat: [Story ID] - [Story Title]`
- Uses `/share` to create OpenCode conversation links for progress tracking
- Updates progress and repeats until completion

### Quality Requirements for Ralph

- Each story must be completable in one iteration
- Include "Typecheck passes" in all acceptance criteria
- UI stories require "Verify in browser using dev-browser skill"
- Follow existing code patterns and project conventions

## Build/Lint/Test Commands

Since this is a configuration repository, traditional build processes do not apply. There are no formal automated validation or testing targets. Manual validation/testing can be performed as follows:

### Manual Validation
```bash
# Check Makefile syntax (dry run of install)
make -n install

# Optionally, check dotfiles for syntax issues (no standalone *.sh scripts)
# Example: run shellcheck on a config file (if shellcheck is available)
shellcheck aliases/.aliases
shellcheck zsh/.zshenv
# etc.
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
There are no formal unit tests. For quick manual checks:

```bash
# Test a specific alias or function by sourcing and executing
zsh -c "source aliases/.aliases && mkcd /tmp/test_dir && pwd"

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
- Use descriptive commit messages
- Keep the repository focused on configuration files
- Test changes before committing

### Maintenance
- Regularly review and update aliases for relevance
- Remove unused or outdated configurations
- Keep dependencies documented
- Test configurations across different environments where possible

---

## Cleaning Up Dotfile Backups

After running `make install`, backup files are created for existing configuration files before they are overwritten. These backup files include:

- `~/.zshrc.backup.*`
- `~/.env.backup.*`
- `~/.config/opencode/opencode.json.backup.*`

To remove all backup files generated by install, use:

    make clean

This will remove all matching backup files in one step with no confirmation prompt. No other files are cleaned at this time.

**Process for future iterations:**
- If new or additional backup files are added to the Makefile, update the `clean` target to handle them.
- Always update both README.md and AGENTS.md to document the backup and cleanup process step-by-step so code and docs remain in sync.

---

## Development Workflow

1. Make changes to configuration files
2. Test changes locally: `source ~/.zshrc`
3. Run validation as appropriate
4. Test aliases and environment: `zsh -c "source .aliases && test_alias"`
5. Commit with descriptive message
6. Update documentation if needed

## Dependencies

This repository assumes:
- Zsh as the required shell
- Oh My Zsh framework
- Standard Unix tools (bash, cp, mkdir, etc.)
- Optional: shellcheck for linting (run manually, not automated)

## Environment Setup

After cloning this repository:
1. Run `make install` to install configurations (backs up existing `.zshrc` with a timestamp)
2. Source configurations: `source ~/.zshrc` (or open a new shell)
3. Copy `env/.env.example` to `$HOME/.env` and edit as needed for secrets
4. AI-specific config: `ai/opencode.json` copied to `$HOME/.config/opencode/opencode.json` (Makefile will handle this).
5. Verify setup: ensure `$JAVA_HOME` is set (for example, run `echo "$JAVA_HOME"`)

## Common Patterns

### Safe File Operations
```bash
# Check file exists before sourcing
if [ -f ~/.aliases ]; then
    . ~/.aliases
fi
```

### Function Definitions
```bash
mkcd() {
    mkdir -p "$1"
    cd "$1"
}
```

### Conditional Logic
```bash
if [ $# -eq 0 ]; then
    # Handle no arguments
else
    # Handle arguments
fi
```

Remember: These dotfiles are personal Zsh configurations. Changes should be tested thoroughly before deployment to avoid breaking shell functionality. Bash users will need to adapt or use at their own risk.
