# Requirements

## Required and conditional dependencies

Read-only assessment needs source/read tools, not a language runtime or package
installation. Git is conditional for local patch, staged change, and history
evidence. Live PR evidence needs an exposed authorized provider tool or the
already available adapter selected for that review. Supplied patches need neither
provider login nor application dependencies.

## Installation and checks

If Git is missing, report the unavailable evidence. For user-operated setup in
a separate authorized scope, macOS with existing Homebrew can use:

```sh
brew install git
git --version
```

Other platforms: [Git installation](https://git-scm.com/downloads).
If GitHub CLI is specifically selected, its
[official installation guide](https://cli.github.com/) supplies platform setup
(`brew install gh` on macOS); user authentication is separate.

Execute-mode review requires existing project check tools and an identified candidate.
Do not install dependencies, switch checkouts, edit source or post external reviews.
Honor explicit inspection-only mode and runtime restrictions.
Missing tools remain explicit coverage limits until separately provisioned.
