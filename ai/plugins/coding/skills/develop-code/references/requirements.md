# Requirements

## Required and conditional dependencies

No language runtime or package is universally required by this instruction-only
skill. The target project determines compilers, runtimes, package managers,
formatters, tests, and services. Git is needed for Git-based change inspection;
native file/search tools are adequate for source-only tasks.

Before implementation, read the project's setup instructions, manifests,
lockfiles, version files, and configured scripts. Load the selected testing,
formatting, or interface skill's own requirements when that workflow applies.
A dependency mentioned in a reference is not automatically required.

## Installation and checks

Restore the existing environment using the project's documented command after
installation is authorized. Examples, only for projects that declare them:

```sh
node --version
npm --version
npm ci
uv sync --locked
```

Choose one matching workflow; do not run every example. `npm ci` replaces
`node_modules` and can run lifecycle scripts. `uv sync` changes the project
environment. Inspect scripts and follow project restrictions before either.
See [npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci) and
[uv project setup](https://docs.astral.sh/uv/guides/projects/).

Missing runtimes should follow project version pins and official installation
instructions, not an arbitrary latest version. On macOS with Homebrew already
available, separately approved `brew install git` supplies Git
([formula](https://formulae.brew.sh/formula/git)); check `git --version`.
Planning, diagnosis-only, and read-only scopes do not authorize dependency setup.
