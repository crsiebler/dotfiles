# Requirements

## Required and conditional dependencies

Git is required for commits and branch operations. The documented GitHub shipping
adapter uses installed GitHub CLI (`gh`), repository access, and user
authentication. Supplied descriptions can be drafted without GitHub access.
Run required project checks with their existing environment before shipping.

git-cliff is optional, required only for requested git-cliff changelog generation.
It is not needed to draft or validate conventional commit messages. Check with
`git cliff --version`; inspect the repository's existing configuration and history.
Separately approved macOS setup can use `brew install git-cliff`; other platforms
should follow [official installation](https://git-cliff.org/docs/installation/).
The skill and AI installer do not install it or configure release automation.

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
