# Requirements

## Required and conditional dependencies

Assessment from supplied issue/ticket/context needs no external package.
Live GitHub or Jira evidence needs the provider capability/adapter selected in
this skill's references. GitHub CLI (`gh`) is conditional when its installed
CLI fallback is selected; Git is conditional for local repository evidence.
Jira/Rovo requires an exposed configured connector and user access, not a
universal Jira CLI. Target project build tools are unnecessary for estimation.

## Installation and checks

For approved GitHub CLI setup on macOS with existing Homebrew:

```sh
brew install gh
gh --version
```

Use [GitHub CLI installation](https://cli.github.com/) for other platforms.
The user can complete `gh auth login` separately. If local Git evidence is
needed, approved `brew install git` or
[Git installation](https://git-scm.com/downloads) supplies it;
verify `git --version`. Do not print tokens or inspect credential stores.

For Jira/Rovo, use the active harness's connector setup and inspect its exposed
schemas; no package installation command applies to every connector.
If provider access is absent, assess supplied material and identify evidence gaps.
Assessment does not authorize ticket edits, posts, dependency setup, or execution.
