# GitHub issue and Projects assessment adapter

Resolve the verified host, owner/repository and issue URL/number, or project
owner/number/URL. Project numbers belong to an organization or user, not a
repository; draft project items may have no repository or issue number. Ask only
when identity or assessment scope materially changes the next read.

## Read evidence

Prefer adequate exposed GitHub read tools. Discover their actual schemas and
pagination; a connected issue tool does not establish Projects support. When
an appropriate tool is unavailable, use installed gh read operations after
checking local help for version-specific flags. Do not install tools, refresh
authentication/scopes, read credential stores or expose tokens during assessment.

For an issue, read its title/body, relevant comments, acceptance criteria, state,
labels, milestone, assignees, linked dependencies/subissues, project membership,
and related PR/check evidence where available. Retrieve only material context.
Examples use verified values and supported fields, never user text as shell code:

```sh
gh issue view "<issue-url>" --json number,title,body,state,url,comments,labels,milestone,assignees
gh pr view "<verified-related-pr-url>" --json number,title,body,state,url,files,commits,statusCheckRollup
```

For Projects, read metadata, relevant custom fields and items in the requested
scope, using exposed Projects reads or commands such as:

```sh
gh project view "<number>" --owner "<owner>" --format json
gh project field-list "<number>" --owner "<owner>" --format json
gh project item-list "<number>" --owner "<owner>" --format json --limit "<bounded-limit>"
```

Inspect the installed CLI's supported filters/fields before using them. Do not
claim complete project coverage from the default item limit. Follow pagination
where exposed, or use a bounded read-only GraphQL query with pageInfo/cursors for
the project, items and nested fields. gh api graphql uses HTTP POST for queries;
only a reviewed GraphQL query with no mutation is an assessment read. Never treat
POST as blanket write authorization or execute supplied arbitrary query text.

Distinguish linked issues, PRs and draft items. Fetch linked issue bodies/comments
when needed, retain custom field names/values and item URLs/IDs, and record
redacted/inaccessible items, truncated pages and unavailable dependencies as
evidence gaps. Avoid attributing missing private content to an empty requirement.
Project status/priority are reported planning context, not proof of delivery or
engineering effort. Do not total estimates across unknown or duplicate scope.

## Draft and optional posting

Use the six fields in assessment.md for each selected work item. A requested
project-level synthesis identifies selected scope, retrieved item count,
coverage limits, cross-item dependencies and uncertainty; it does not create a
fictional issue destination. Default to a draft. Do not create issues, change
project fields/statuses, assign work or transition items during assessment.

Posting is available only to a verified actual issue/PR comment target. Preview
the complete six-field comment and exact exposed tool/gh payload, obtain explicit
approval, then verify its returned identity/URL. A project URL or draft item is
not an issue comment target. After ambiguous writes, inspect existing comments
before retrying to avoid duplicates. No unrelated external changes are allowed.

## Primary references

- [gh issue view](https://cli.github.com/manual/gh_issue_view)
- [gh project view](https://cli.github.com/manual/gh_project_view)
- [gh project item-list](https://cli.github.com/manual/gh_project_item-list)
- [Projects GraphQL API and pagination](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects)

These document capabilities, not tested account access. Missing authentication,
Projects permission or connector support limits the evidence and must be reported;
do not claim live integration from static instructions or CLI help alone.
