# Requirements

## Required and conditional dependencies

Drafting from supplied evidence needs no external utility. Live GitHub evidence
uses the documented installed GitHub CLI (`gh`) adapter where selected; Git
is conditional for local change/history evidence. Jira/Rovo needs an exposed
authorized connector for live ticket retrieval or an explicitly approved post.
No general Jira CLI, document renderer, or target application runtime is required.

## Installation and checks

Separately approved setup on macOS with existing Homebrew:

```sh
brew install gh
gh --version
```

Other platforms: [GitHub CLI installation](https://cli.github.com/).
User authentication through `gh auth login` is separate; never print tokens or
inspect credential stores. Git, if needed, follows
[Git installation](https://git-scm.com/downloads) (`brew install git` on macOS);
check `git --version`.

For Jira/Rovo, configure the active harness's supported connector with the user's
authorized account and inspect the actual schemas. Installing an SDK does not
provide a connector. Use supplied evidence if live access is unavailable.
Availability/login checks do not authorize posting; drafting remains the default.
