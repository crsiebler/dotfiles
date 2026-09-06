# GitHub review-thread resolution protocol

## Read and map

Resolve owner/repo/PR from explicit input or verified GitHub remote metadata.
Retrieve the PR head and paginated review comments with installed `gh`:

```sh
gh api --paginate "repos/<owner>/<repo>/pulls/<number>/comments"
```

Query GraphQL `repository { pullRequest { reviewThreads } }` for thread `id`,
`isResolved`, `isOutdated`, and comment `id`, `databaseId`, `body`, `url`, and
commit context. Paginate threads and each nested comments connection separately.
Use `pageInfo { hasNextPage endCursor }`; do not assume `first: 100` or
`comments(first: 10)` is complete. For `gh api graphql`, pass an integer PR
variable with `-F number=<number>` rather than string-valued `-f number`.

REST numeric comment `id` maps to GraphQL `databaseId`; REST `node_id` maps to
GraphQL comment `id`. The `PRRT_...` thread ID is a separate GraphQL identifier.
Never derive thread IDs from file/line guesses, especially for outdated comments.

Inspect actual fix commits and tests reachable from the current PR head.
Conversation context and commit messages help locate evidence but cannot prove
resolution. Local-only fixes are not available to reviewers. A declined
suggestion needs an evidence-backed explanation and explicit approval to close.

## Preview and approve

For each item show PR URL/head SHA, original concern, fix evidence, numeric
parent comment ID, GraphQL thread ID, complete reply, and exact proposed writes.
Default statuses for replies: `Fixed`, `Implemented`, `Addressed`, or `Declined`
with a concise technical explanation. Never claim a test or fix without evidence.

These templates illustrate supported GitHub endpoint shapes, not executable
authorization. Populate and preview actual safely quoted values first:

```sh
gh api "repos/<owner>/<repo>/pulls/<number>/comments/<parent-id>/replies" --method POST -f body="<approved-reply>"
gh api graphql -f query='mutation($threadId: ID!) { resolveReviewThread(input: {threadId: $threadId}) { thread { id isResolved } } }' -f threadId="<approved-thread-id>"
```

Use the original/root review comment as the reply parent. The issue-comments
endpoint and `gh pr comment` create conversation comments, not threaded review
replies. The pull review-comments creation endpoint creates a new inline comment,
not a reply. Do not use either as a fallback.

Ask for explicit confirmation after preview (`yes`, `y`, `confirm`, `fix it`, or
`go ahead`); treat other responses as cancellation or clarify. Batch approval
applies only to the displayed, unchanged batch. Re-read relevant state if the
PR changed before execution; invalidate approval when targets/content change.

## Verify and recover

Record the exact IDs returned by this session's writes. After a reply:

```sh
gh api "repos/<owner>/<repo>/pulls/comments/<new-reply-id>" --jq '{id, in_reply_to_id}'
```

Require `in_reply_to_id` to equal the expected numeric parent, not merely be
non-null. Verify this before resolving that thread. After resolution, require
the returned or re-read matching thread to have `isResolved: true`. A successful
HTTP response containing GraphQL errors is not success.

On validation failure, stop that item's subsequent writes and report the
problem. Preview corrections with original body, returned ID, intended parent,
and exact edit/delete/repost payload; obtain fresh approval. Correct only IDs
created by this session, not every comment by the same author after a timestamp.
If correction fails, leave it for manual follow-up rather than a retry loop.

On timeout or ambiguous write response, read state to determine whether the
write succeeded before considering a retry. Respect actual rate-limit responses
and permission errors; do not assume a fixed hourly allowance or broaden scopes.

Prefer in-memory data. If temporary artifacts are needed, use a unique
project-local path, avoid secrets, track created paths, and clean up only those
artifacts under repository deletion policy. Never use recursive cleanup of a
guessed path or claim project-local paths bypass permission controls.

Report analyzed, replied, validated, resolved, skipped, and failed counts plus
URLs/IDs and remaining actions. Do not print a static “all correctly posted”
summary when any result is unverified.
