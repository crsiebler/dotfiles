---
name: status-update
description: Generate concise, evidence-backed project status updates for leadership, delivery teams, or stakeholders. Use when reporting progress, wins, QA, risks, blockers, workflow deviations, and stakeholder concerns over a defined period using available Jira, GitHub, and supplied context.
---

# Status Update

Create a project status update for an arbitrary team and reporting period. Use
only available evidence, adapt sections to the project and audience, and
identify missing or incomplete data.

## Context Required

Resolve the following from the request, project configuration, repository
metadata, or connected read-only integrations:

- Project name and brief identity
- Intended audience
- Reporting period, including timezone when relevant
- Team members, roles, and Jira/GitHub identity mappings
- Jira project key or filter, base URL, relevant statuses, and workflow
- GitHub repository or repositories
- Expected delivery workflow, including issue, review, QA, and deployment stages
- Narrative voice and output format
- Whether to save the report and, if so, the output path
- Optional stakeholder concerns, team context, milestones, or reporting priorities

Do not infer a person's role or map source identities based only on similar
names. Repository contributors may be discovered, but team membership and role
assignments require reliable project evidence or user confirmation.

If required context cannot be safely discovered, ask one focused clarification
containing only the unresolved items. Offer neutral defaults where appropriate:

- Period: previous 7 calendar days ending today
- Voice: neutral third person
- Format: concise GitHub-flavored Markdown
- File output: disabled

A file path is required only when file output is enabled. Do not silently select
or write one. Never request credentials, tokens, private keys, or unnecessary
personal data.

## Operating Rules

- Use Jira and GitHub independently. Either, both, or neither may be available.
- Proceed with available evidence and state material coverage gaps.
- Use read-only operations. Do not modify issues, comments, pull requests,
  reviews, releases, deployments, or repository state.
- Do not broaden queries beyond the configured projects, repositories,
  identities, and reporting period.
- Distinguish current state from activity that occurred during the period.
- Distinguish verified facts, stakeholder-reported context, and uncertainty.
- Do not claim that silence in a source means no work occurred.
- Do not expose secrets, private query parameters, access tokens, email
  addresses, or unnecessary account identifiers in the report.
- Minimize individual-level reporting unless the audience requires it.

## Evidence Gathering

### 1. Establish Scope

Confirm the inclusive reporting dates and timezone, integration scopes, team
identity mappings, expected workflow, and requested report detail. Record which
sources are available before gathering data.

### 2. Gather Jira Evidence

When Jira is available, retrieve issues in the configured project or filter
that were created, updated, or transitioned during the period. When supported,
collect:

- Issue key, summary, type, assignee, current status, and update time
- Status changelog with transition timestamps
- Resolution and completion evidence
- Blocker indicators and relevant comments
- QA or acceptance evidence
- Sprint, milestone, release, or deployment fields when applicable

Use the changelog to report transitions. A current status alone does not prove
that a transition occurred during the period. Label status-count populations
precisely; do not present a partial query as the status of the entire project.

### 3. Gather GitHub Evidence

When GitHub is available, retrieve relevant activity from the configured
repositories and reporting period:

- Commits
- Pull requests opened, reviewed, closed, or merged
- Review outcomes and requested changes
- Linked issues or ticket references
- Releases, deployments, or environment events when available
- Failed checks or other delivery risks when relevant

Prefer pull-request and merge evidence for delivered changes. Treat commits as
development activity, not proof of release or deployment. Map repository
activity to issues only through explicit references or reliable linkage.
Describe activity without a reliable issue mapping as "unmapped repository
activity" rather than assuming process compliance or completion.

### 4. Incorporate Supplied Context

Use user-provided project-management, team, client, or stakeholder context when
it is relevant to the requested period. Present concerns as reported concerns,
not verified technical facts, unless source evidence supports them.

## Claim Validation

Apply these standards before drafting:

- **Ticket transition:** Jira changelog evidence within the period
- **Commit activity:** repository, author identity, and timestamp evidence
- **Pull request state:** recorded PR state and relevant timestamps
- **QA pass or failure:** explicit transition, test result, approval, or
  attributable QA comment
- **Deployment or release:** deployment, release, environment, or equivalent
  delivery evidence; a merge or issue status is insufficient
- **Blocker:** explicit blocked status, label, dependency, failed check, or
  attributable report, including whether it is current, resolved, or unknown
- **Workflow deviation:** configured expected workflow and observed transition
  sequence
- **Individual contribution:** validated source identity or supplied context
- **Team well-being:** explicit supplied or documented context, never activity
  volume
- **No activity:** "no activity found in the available source data," not "no
  work occurred"

When sources conflict, describe the inconsistency and do not choose a version
without evidence.

## Analysis

Using only validated evidence:

1. Identify the most important outcomes and team wins.
2. Summarize engineering, QA, project-management, and stakeholder activity where
   applicable.
3. Identify active risks, blockers, failed checks, testing failures, and
   unresolved dependencies.
4. Compare observed transitions with the configured workflow and flag supported
   skips, reversals, or unusual paths.
5. Note unmapped repository activity without assuming missing process
   compliance.
6. Record retrieval failures, incomplete histories, identity gaps, and source
   inconsistencies.
7. Prioritize audience-relevant outcomes over exhaustive activity lists.

## Report Structure

Adapt the report to the audience and omit sections that are not applicable:

1. **Project and reporting period**
2. **Executive summary**
3. **Team wins and delivered outcomes**
4. **Engineering progress**
5. **QA and acceptance**
6. **Project or delivery management**
7. **Risks, blockers, and workflow deviations**
8. **Stakeholder concerns or decisions needed**
9. **Next-period priorities**
10. **Evidence gaps and retrieval errors**

Use role-based or team-level summaries by default. Add individual sections only
when explicitly requested or appropriate for the audience. For each risk or
blocker, state its impact, current known state, and required action or owner only
when supported.

## Formatting

- Keep the report concise and audience-ready.
- Follow the requested narrative voice; otherwise use neutral third person.
- Use the requested output format; otherwise use GitHub-flavored Markdown.
- Use `YYYY-MM-DD` dates unless another format is requested.
- Order activities by importance, then reverse chronologically when listing
  comparable events.
- Link Jira issues and GitHub artifacts when valid URLs are available. Do not
  fabricate links from an unknown base URL.
- Avoid raw account identifiers, unsupported precision, speculation, and
  repetitive source details.

## Evidence Gaps and Errors

Include an evidence-gap section when a source is unavailable, incomplete,
inconsistent, or outside the authorized scope. For each material gap, state:

- What source or query was unavailable
- What information may be missing
- How the gap limits confidence in the report

Do not fail the entire report because one integration is unavailable.

## File Output

Write a file only when the user explicitly enables file output. When saving:

- Use the confirmed output path within the permitted project scope.
- Write exactly the finalized report.
- Report the saved path only after the write succeeds.
- If writing fails, return the report directly and describe the error.

When file output is disabled, return the report directly without creating files.
