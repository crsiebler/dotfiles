# Jira assessment adapter

Inspect the exposed schemas for exact names, required arguments, site and issue
identifiers, pagination and comment formats. Resolve the authorized site; do not
assume the first returned site is correct. Follow pagination or disclose incomplete
coverage. Constrain queries to the requested issue and relevant dependencies.

For assessment, use exposed `getJiraIssue` and `searchJiraIssuesUsingJql`
capabilities for the target and relevant dependencies. If needed and exposed,
use `discover` / `executeRead` for supported comments or related context. All
names must match actual exposed schemas, including harness prefixes; no assumed
argument lists. Only an explicitly approved `addOrEditJiraIssueComment`
operation may post the assessment, and it must add a new comment rather than
accidentally edit an existing one. Show the exact tool, site, issue and complete
payload in its required format. Reuse posting authority for the same target,
content, and effect; otherwise obtain it after preview. Re-preview material
changes; continuation and mechanical encoding do not invalidate unchanged
approval. Read back ambiguous outcomes before retrying.

Asana is unsupported until an actual schema/adapter is verified. For GitHub,
use this skill's [GitHub issue and Projects adapter](github.md), not Jira routing.
Unavailable integrations limit evidence, not permission to guess state.
