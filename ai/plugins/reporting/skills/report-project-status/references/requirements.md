# Requirements

## Required and conditional dependencies

Status synthesis from supplied project evidence needs no external package.
Live GitHub evidence uses the documented installed GitHub CLI (`gh`) adapter;
Jira/Rovo evidence needs an exposed authorized connector when selected.
Git is conditional for local repository evidence. There is no shipped Asana CLI
adapter or mandatory office/document utility.

## Installation and checks

For separately approved setup on macOS with existing Homebrew:

```sh
brew install gh
gh --version
```

Use [GitHub CLI installation](https://cli.github.com/) on other platforms.
The user can complete `gh auth login` when needed. Never print tokens or read
credential stores. For local evidence, Git can be installed via
[official instructions](https://git-scm.com/downloads) or approved
`brew install git`; verify `git --version`.

Configure Jira/Rovo using the active harness's connector setup and inspect its
actual schemas. Connection/login is separate from authority to post.
Use supplied exports/context when provider access is absent and report coverage
limits. Follow the selected producing skill's requirements only when a separate
artifact creation task calls for it.
