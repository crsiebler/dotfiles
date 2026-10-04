# Requirements

## Required and conditional dependencies

Assessment of supplied feedback needs no external package. Git is conditional
for local revision/remote evidence. Live GitHub feedback uses the documented
installed GitHub CLI (`gh`) adapter and authorized repository authentication;
MCP discovery alone does not provide that adapter. Repairs need the target
project's existing implementation/test environment.

## Installation and checks

For separately authorized setup on macOS with Homebrew already installed:

```sh
brew install git gh
git --version
gh --version
```

Use [Git installation](https://git-scm.com/downloads) and
[GitHub CLI installation](https://cli.github.com/) on other platforms.
If access is missing, the user can complete `gh auth login`; never print tokens
or read credential stores. Availability is distinct from access to a given PR.

Load the selected development/test skill's requirements for repairs. Installing
tools does not authorize feedback posts, PR reviews, commits, or resolving threads.
If live access is unavailable, use supplied feedback and report evidence gaps.
