# AGENTS.md - Dotfiles Repository Guidelines

This document provides guidelines for agents working in this dotfiles repository. These dotfiles contain shell configurations, aliases, and scripts primarily for Zsh/bash environments.

## Build/Lint/Test Commands

Since this is a configuration repository rather than a compiled application, traditional build processes don't apply. However, the following commands are relevant for validation and testing:

### Validation Commands
```bash
# Check shell syntax for scripts
bash -n reload.sh

# Validate all shell scripts in the repository
find . -name "*.sh" -exec bash -n {} \;

# Check for common shell scripting issues (if shellcheck is available)
shellcheck reload.sh
```

### Testing Commands
```bash
# Test the reload script (dry run - check what would be copied)
./reload.sh --dry-run  # Note: This would need to be implemented

# Verify alias files can be sourced without errors
bash -c "source .aliases"
bash -c "source .git_aliases"
bash -c "source .node_aliases"
bash -c "source .docker_aliases"
bash -c "source .symfony_aliases"

# Test configuration loading
zsh -c "source .zshenv"
```

### Single Test Execution
There are no formal unit tests in this repository. For testing individual components:

```bash
# Test a specific alias by sourcing and executing
bash -c "source .aliases && mkcd /tmp/test_dir && pwd"

# Test environment variable loading
bash -c "source .zshenv && echo \$JAVA_HOME"
```

## Code Style Guidelines

### Shell Scripts

#### File Structure
- Always include shebang: `#!/bin/bash`
- Use descriptive comments at the top explaining the script's purpose
- Keep scripts simple and focused on a single responsibility
- Exit with appropriate status codes (0 for success, non-zero for failure)

#### Naming Conventions
- Use lowercase with underscores for function names: `mkcd()`, `urlencode()`
- Use lowercase for variable names: `old_lc_collate`, `length`
- Alias names should be short but descriptive: `hs`, `myip`, `gac`, `nis`
- File names for configuration use dot prefix: `.zshrc`, `.aliases`

#### Formatting
- Use consistent indentation (prefer tabs for shell scripts)
- Use spaces around operators: `if [ $# -eq 0 ]`
- Break long lines for readability (aim for < 80 characters)
- Use blank lines to separate logical sections

#### Error Handling
- Check for file existence before sourcing: `if [ -f ~/.aliases ]; then`
- Use `set -e` in scripts to exit on first error (if appropriate)
- Provide meaningful error messages when operations fail
- Handle edge cases gracefully

#### Best Practices
- Quote variables to prevent word splitting: `"$1"`, `"${1}"`
- Use `local` for function variables to avoid polluting global scope
- Prefer `printf` over `echo` for portability
- Use descriptive variable names that explain their purpose
- Avoid hardcoded paths; use variables or relative paths

### Configuration Files

#### Zsh Configuration (.zshrc)
- Group related settings together with comments
- Use consistent commenting style for disabled options
- Keep personal customizations separate from framework settings
- Document any non-obvious configurations

#### Environment Files (.zshenv)
- Load aliases conditionally to avoid errors if files don't exist
- Use clear section headers for different types of configurations
- Keep environment variables organized by category

### Aliases

#### General Aliases (.aliases)
- Keep aliases simple and focused
- Use descriptive names that indicate the command's purpose
- Group related aliases together
- Comment complex aliases explaining their functionality

#### Specialized Aliases (.git_aliases, .node_aliases, etc.)
- Prefix with tool name if not obvious: `gac` for git add commit
- Keep alias definitions to one line when possible
- Use consistent naming patterns within each category

### Comments
- Use `#` for single-line comments
- Place comments above the code they explain
- Keep comments concise but informative
- Comment complex logic or non-obvious operations

### File Organization
- Keep related configurations in separate files
- Use consistent naming patterns (.tool_aliases)
- Maintain alphabetical ordering where appropriate
- Document file purposes in README.md

### Security Considerations
- Never store secrets or credentials in dotfiles
- Be cautious with `sudo` commands in aliases
- Validate URLs and commands before execution
- Use safe practices for file operations (check existence, permissions)

### Git Workflow
- Commit related changes together
- Use descriptive commit messages
- Keep the repository focused on configuration files
- Test changes before committing

### Maintenance
- Regularly review and update aliases for relevance
- Remove unused or outdated configurations
- Keep dependencies documented
- Test configurations across different environments when possible

## Development Workflow

1. Make changes to configuration files
2. Test changes locally: `source ~/.zshrc`
3. Run validation: `bash -n script.sh`
4. Test functionality: `bash -c "source .aliases && test_alias"`
5. Commit with descriptive message
6. Update documentation if needed

## Dependencies

This repository assumes:
- Zsh as the primary shell
- Oh My Zsh framework
- Standard Unix tools (bash, cp, mkdir, etc.)
- Optional: shellcheck for linting

## Environment Setup

After cloning this repository:
1. Run `./reload.sh` to install configurations
2. Source configurations: `source ~/.zshrc`
3. Verify setup: `echo $JAVA_HOME`

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
function_name() {
    # Function body
    local var="$1"
    # ... logic ...
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

Remember: These dotfiles are personal configurations. Changes should be tested thoroughly before deployment to avoid breaking shell functionality.