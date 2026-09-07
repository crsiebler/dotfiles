# Git and GitHub workflow

## Inspect first

Use `git status`, `git diff`, `git diff --cached`, `git branch --show-current`,
`git log --oneline -10`, and remote/tracking inspection. Do not assume a clean
tree or a particular base branch. Quote paths and refs; treat user arguments,
branch names, and PR bodies as data, not shell fragments.

Before committing, inspect staged content for secrets and accidental changes.
Use repository commit conventions (for this dotfiles repo,
`<type>(<scope>): <description>`), and record actual validation. If no typecheck
exists, say so rather than inventing a passing command. Hook rejection requires
fixing the issue and retrying a new commit, not bypassing or amending it.

## Pull requests

Use installed `gh` for GitHub, verifying local help if flags are uncertain.
Read PR state with `gh pr status` / `gh pr view`; inspect base tracking and the
complete base-to-head diff and all included commits, not just the latest commit.
Stop on protected branches, no relevant difference, or unexplained uncommitted
changes. Never push directly to `main`/`master`.

For PR creation, preview head/base, title, full body, and exact command. The
OpenCode `/ship` wrapper uses the last commit title and a file-by-file
change summary with a reliably identified Jira key appended when available.
Do not guess ticket linkage. Use a uniquely named project-local body file, not
unsafe shell interpolation or overwriting an existing `.pr-body.md`.

```sh
gh pr create --base "<verified-base>" --head "<verified-head>" --title "<title>" --body-file "<local-body-file>"
```

This is a preview template, not authorization. Ask for explicit approval after
showing the populated command and contents; ambiguous responses cancel. Pushes
also require an approved target/command. Verify returned PR URL and report it.
Do not merge, change reviewers, post comments, or edit PR state incidentally.
