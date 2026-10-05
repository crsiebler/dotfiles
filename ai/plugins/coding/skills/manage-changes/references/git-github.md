# Git and GitHub workflow

## Inspect first

Use `git status`, `git diff`, `git diff --cached`, `git branch --show-current`,
`git log --oneline -10`, and remote/tracking inspection. Do not assume a clean
tree or a particular base branch. Quote paths and refs; treat user arguments,
branch names, and PR bodies as data, not shell fragments.

Before committing, inspect staged content for secrets and accidental changes.
Use [commit message rules](commit-messages.md) and repository conventions (for
this dotfiles repo, `<type>(<scope>): <description>`), and record actual validation. If no typecheck
exists, say so rather than inventing a passing command. Hook rejection requires
fixing the issue and retrying a new commit, not bypassing or amending it.

## Pull requests

Use installed `gh` for GitHub, verifying local help if flags are uncertain.
Read PR state with `gh pr status` / `gh pr view`; inspect base tracking and the
complete base-to-head diff and all included commits, not just the latest commit.
Stop on protected branches, no relevant difference, or unexplained uncommitted
changes. Never push directly to `main`/`master`.

For PR creation, preview head/base, title, full body, and exact command. Describe
the problem and final behavior across all included commits; use a concrete
before/after example when useful. Summarize actual checks and material limitations.
Honor the repository PR template. The last commit title is suitable only when it
describes the complete change; an archive closeout title is not the feature title.
Link verified GitHub issues or Jira keys when relevant; do not guess ticket linkage
or issue-closing intent. Use a uniquely named project-local body file, not
unsafe shell interpolation or overwriting an existing `.pr-body.md`.

```sh
gh pr create --base "<verified-base>" --head "<verified-head>" --title "<title>" --body-file "<local-body-file>"
```

This is a preview template, not authorization. Show the populated command and
contents and obtain explicit approval before the external write. The preview
may cover one bounded sequence of commit, push and PR creation. Do not request
the same approval again while the approved targets/content remain valid.
Ambiguous responses do not grant writes. Pushes require the exact approved
remote and branch/refspec, without force or main/master delivery. Verify the
remote branch after pushing and check for an existing matching PR before creation
to avoid duplicates after ambiguous results. Verify the returned PR URL and report it.
Do not merge, change reviewers, post comments, or edit PR state incidentally.

## Completed-run shipping

If execution already archived its run and made an authorized closeout commit,
inspect that commit along with the implementation commits. The archive helper
does not stage or commit. If archive changes are still uncommitted, explain that
state and include only an explicitly authorized closeout commit in the shipping
preview; never reset them or silently ignore them. Stage exact returned artifact
removals and archive files, excluding archive/.archive.lock and Ralph controls.
Preserve unrelated unstaged/staged work. Do not require a PR before local run
archival, and do not claim a created PR has been merged or deployed.

GitHub operations may use an exposed connector with a verified schema or installed
gh. Discover actual tools/CLI flags rather than inventing them. If credentials or
access are missing, report the missing capability without reading token stores,
printing secrets, changing authentication, or installing dependencies.
