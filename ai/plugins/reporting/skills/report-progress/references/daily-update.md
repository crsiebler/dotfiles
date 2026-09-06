# Daily progress contract

## Evidence

Identify the supplied ticket and confirm summary, description, status, assignee,
acceptance criteria, and previous comments. Note previous next steps, blockers,
ETA, and stakeholder requests. Establish the reporting date/timezone and interval
since the previous update. Do not post against a guessed ticket.

Inspect scoped local evidence:

```sh
git status
git branch --show-current
git log --oneline --decorate -10
git diff --stat
git diff --cached --stat
```

Compare history to the verified base/tracking branch, not assumed `origin/main`.
When installed and authorized, GitHub CLI read operations can supply PR evidence:

```sh
gh pr status
gh pr view --json number,title,state,isDraft,mergeStateStatus,reviewDecision,statusCheckRollup,url,mergedAt,baseRefName,headRefName
gh pr checks
```

Find PRs through reliable branch/commit/ticket linkage. Include only work tied
to this issue, not every nearby commit. If GitHub is unavailable, use supplied
links and label state as unverified; never invent a GitHub MCP tool.

## Exact output

```text
Date: YYYY-MM-DD
What I completed:
- Evidence-backed work, with concise commit or PR reference.

What’s next:
- Remaining engineering work based on acceptance criteria and current evidence.

Blockers:
- Explicit blocker or “None identified.”

ETA:
- Supported engineering-hour range or “Unknown pending <specific information>.” Excludes QA testing.
```

No extra headings/sections in the posted comment. Explain retrieval limits
concisely within relevant fields and in the conversational preview.

### Completed

Label uncommitted work explicitly. Commits do not prove merge, merge does not
prove deployment, and checks do not prove QA acceptance. Include relevant PR
state and validation only when observed. If no new completed work is supported,
write “No new completed engineering work found since the last update.” This
does not imply nobody worked.

### Next

Use acceptance criteria and prior commitments to identify missing work. An open
PR still requires merge; deployment remains only if the project's workflow
requires it. Failed/pending checks require attention before merge. Draft PRs
need readiness review; commits without a PR need PR preparation where required.
Uncommitted work may still need finalization, tests, commit, and PR inclusion.
Do not assert incomplete criteria solely because a commit title omits them.

### Blockers

Use explicit active-context reports first, then issue comments, dependencies,
failed checks, missing approvals, unresolved reviews, and environment evidence.
Label inferred risks as potential blockers. Do not turn routine waiting into a
confirmed blocker without context. If none are evidenced, use “None identified.”

### ETA

Estimate engineering effort, not elapsed delivery time. Include remaining
implementation, review fixes, merge preparation, and deployment work when
required. Exclude QA/product acceptance testing, stakeholder delays, approval
waiting time, and other non-engineering elapsed time. State assumptions and a
range only when evidence supports it; otherwise state what prevents estimation.
Zero engineering hours requires no engineering work remaining, including any
required deployment. Always include `Excludes QA testing.` Do not use canned
hour ranges based only on PR status.

## Posting

Check exact labels, target, evidence, and sensitive-data removal. Preview the
full body and populated tool payload, then ask for explicit approval. No setting
or initial request bypasses this step. After the approved write, verify the
returned issue/comment ID (re-read when needed) and report actual results.
On timeout, inspect existing comments before retrying to avoid duplicate posts.
Never edit/delete an earlier update or transition status incidentally.
