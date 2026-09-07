# Jira assessment adapter

Read the bundled [Rovo v2 source adapter](../../report-progress/references/jira.md)
before accessing Jira. It defines schema discovery, site resolution, pagination,
comment formats and the preview/approval boundary.

For assessment, use exposed `getJiraIssue` and `searchJiraIssuesUsingJql`
capabilities for the target and relevant dependencies. If needed and exposed,
use `discover` / `executeRead` for supported comments or related context. All
names must match actual exposed schemas, including harness prefixes; no assumed
argument lists. Only an explicitly approved, previewed
`addOrEditJiraIssueComment` operation may post the assessment, and it must add a
new comment rather than accidentally edit an existing one.

Asana is unsupported until an actual schema/adapter is verified. For GitHub,
use installed `gh` read operations (`gh pr view`, `gh pr checks`, scoped
`gh api` GET requests) or supplied evidence; do not assume a GitHub MCP suite.
Unavailable integrations limit evidence, not permission to guess state.
