# Requirements

## Required and conditional dependencies

Git is required for commits and branch operations. The documented GitHub shipping
adapter uses installed GitHub CLI (`gh`), repository access, and user
authentication. Supplied descriptions can be drafted without GitHub access.
Run required project checks with their existing environment before shipping.

## Installation and checks

On macOS with Homebrew already installed, separately approved setup can use:

```sh
brew install git gh
git --version
gh --version
```

For other platforms or approved pinned versions, use official
[Git installation](https://git-scm.com/downloads) and
[GitHub CLI installation](https://cli.github.com/).
The user can complete `gh auth login` when needed; do not print tokens, inspect
credential stores, or infer authentication from executable presence.

Installation/login does not authorize a commit, push, PR creation, merge, or
external comment. Preserve the skill's exact write scope and preview requirements.
A GitHub MCP connection is not proof that the documented `gh` adapter is installed.
