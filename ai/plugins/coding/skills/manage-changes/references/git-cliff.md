# Optional changelog generation with git-cliff

Use only when changelog work is requested or the repository's established
shipping workflow requires it. Commit formatting does not require git-cliff.
Inspect existing `cliff.toml`, changelog conventions, tag/range selection and
release workflow before choosing commands. Configuration may filter or regroup
commit types; conventional messages alone do not define the rendered output.

Recommend release-time generation unless the project already maintains an
Unreleased section on every change. git-cliff runs when invoked manually or by
automation; it does not automatically update a file when Git commits are made.
Preview unreleased entries without writing a file:

```sh
git cliff --unreleased
```

For an authorized full regeneration using the project's configured history:

```sh
git cliff --output CHANGELOG.md
```

This replaces the output file: preserve curated content and inspect the resulting
diff. For an authorized release update to an existing changelog:

```sh
git cliff --unreleased --tag <approved-version> --prepend CHANGELOG.md
```

Replace the placeholder with the approved version. `--tag` labels the generated
section; it does not create a Git tag. Ensure release changes are committed before
generation so the selected Git history contains them. Verify boundaries and avoid
duplicate sections when repeating a prepend operation. Follow the project's
policy for excluding changelog maintenance commits from subsequent release notes.

GitHub Actions can generate a changelog or release notes using git-cliff-action.
Fetch the required history and tags (typically checkout with `fetch-depth: 0`).
Generation in a runner does not commit the file back to the repository. If a
tracked CHANGELOG.md must be part of the tagged release, prepare it in a release
PR before tagging. A tag-triggered job can instead generate GitHub release notes
or an artifact without adding a commit after the release tag.

Do not add workflows, commit generated files, push, create tags or publish releases
without the applicable authorization. Prefer the repository's existing release
process; this reference does not start or configure one automatically.

Official references: [usage examples](https://git-cliff.org/docs/usage/examples/),
[configuration](https://git-cliff.org/docs/configuration/), and
[GitHub Actions](https://git-cliff.org/docs/github-actions/git-cliff-action/).
