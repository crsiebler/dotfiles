# Requirements

## Required and conditional dependencies

No runtime or package is required for source mapping when native read/search
tools are available. Git is conditional for history/diff evidence. Ripgrep (`rg`)
is a preferred shell search utility; its absence permits an adequate exposed
search tool or standard fallback. Target application dependencies are not
required merely to inspect its files.

## Installation and checks

If shell search is selected and installation is approved, macOS with existing
Homebrew can use:

```sh
brew install ripgrep
rg --version
```

See [ripgrep installation](https://github.com/BurntSushi/ripgrep#installation) for
other platforms. Git can be installed with separately approved `brew install git`
or [official platform instructions](https://git-scm.com/downloads);
verify `git --version`.

Keep mapping read-only until the requested documentation write. Do not run build,
dependency installation, generated-code, or application startup commands merely
to collect a source map.
