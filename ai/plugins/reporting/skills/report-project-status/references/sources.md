# Reporting source adapters

## Jira: Atlassian Rovo v2

Read the bundled [Jira adapter](../../report-progress/references/jira.md) for
actual-schema discovery, site resolution, pagination, and legacy separation.
Use exposed `searchJiraIssuesUsingJql` for scoped period populations and
`getJiraIssue` for relevant details. Where exposed, `discover` / `executeRead`
can identify and execute supported changelog/comment reads. Do not assume
operation names, field expansions, or response completeness.

Record query scope and pagination coverage. Updated-in-period is not the same
as completed-in-period; use transition timestamps for transition claims. A
current status cannot establish when work moved. This workflow is read-only:
do not invoke `addOrEditJiraIssueComment` or a write executor.

## GitHub

Use installed `gh` read commands after confirming repository and period:
`gh pr list`, `gh pr view`, `gh pr checks`, and scoped `gh api` GET requests for
events that require details. Inspect actual local help when flags/fields are
uncertain. Paginate list/API results and disclose caps. Do not treat an open-PR
default query as a complete history including closed/merged PRs.

Retrieve opened/reviewed/merged timestamps as relevant, and distinguish release
records from verified deployments to an environment. Link work only through
explicit ticket references or reliable metadata. Do not infer identity mappings
from similar names. GitHub MCP schemas are not assumed or documented here.

## Unsupported sources and fallback

Asana is unsupported until actual exposed schemas and a source adapter are
verified. If Jira or GitHub is unavailable, use supplied evidence independently
and label gaps. Do not invent tool calls, links, transition histories, or team
activity. Never broaden the project/person/time scope to compensate for missing
data. Return the report directly; external posting requires a separate workflow
with an exact preview and explicit approval.
