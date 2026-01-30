---
name: github-review-resolver
description: Mark GitHub PR code review comments as resolved based on commit history or agent context
metadata:
  audience: developers, reviewers
  workflow: pull-request-review
---

## What I do
- Fetch all review comments from a GitHub PR using REST API
- Map comments to review threads using GraphQL API
- Analyze commit history and agent context to identify resolved comments
- Automatically resolve identified threads via GraphQL mutation
- Provide detailed feedback on resolutions and manual follow-ups

## When to use me
Use this skill when:
- You want to clean up resolved review comments after pushing fixes
- Managing PR reviews with many threads becomes tedious
- Ensuring review threads are properly resolved before merge
- Automating routine follow-up on code review feedback

## Parameters
### Required
- `pr_number`: GitHub PR number (e.g., `2201`)

### Optional
- `repo_owner`: Repository owner (auto-detected from current git repo)
- `repo_name`: Repository name (auto-detected from current git repo)
- `commit_sha`: Specific commit to analyze (defaults to PR branch head)
- `resolution_method`: commit-history/agent-context/both (default: both)
- `dry_run`: Preview mode without changes (default: true)
- `auto_resolve`: Skip confirmations (default: false)
- `max_threads`: Max threads to process (default: 50)

## Repository Detection
Automatically detects repository information from the current git repository:
1. Gets remote origin URL using `git remote get-url origin`
2. Parses owner and repo name from GitHub URL formats
3. Falls back to manual input if detection fails

Error handling:
- Not in git repo: Prompt for manual repo_owner/repo_name
- No origin remote: Prompt for manual input
- Invalid URL format: Fallback to user input

## Step-by-Step Execution Flow
1. **Repository Detection**: Auto-detect repo owner/name from git remote
2. **Validation**: Check PR accessibility and GitHub API permissions
3. **Data Fetching**: Query PR review comments via REST API
4. **Thread Mapping**: Use GraphQL to map comments to thread IDs
5. **Resolution Analysis**: Apply heuristics to identify addressed comments
6. **Confirmation**: Show proposed resolutions (unless auto-resolve enabled)
7. **Resolution**: Execute GraphQL mutations to resolve approved threads
8. **Reporting**: Generate summary of actions and recommendations

## GitHub API Integration
### Fetch Review Comments (REST API)
```bash
gh api repos/$repo_owner/$repo_name/pulls/$pr_number/comments
```

Returns all PR review comments with IDs, timestamps, and file context.

### Map Comments to Threads (GraphQL)
```bash
gh api graphql -f query='
query GetPRReviewThreads($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          comments(first: 10) {
            nodes { id }
          }
        }
      }
    }
  }
}
' -f owner="$repo_owner" -f repo="$repo_name" -f number="$pr_number"
```

### Resolve Thread (GraphQL)
```bash
gh api graphql -f query='mutation ResolveThread($threadId: ID!) { resolveReviewThread(input: {threadId: $threadId}) { thread { id isResolved } } }' -f threadId="$THREAD_ID"
```

## Resolution Logic
### Commit-History Method
1. File containing comment modified after comment creation
2. Commit messages reference resolution keywords ("fix", "address", "resolve")
3. Code around commented line has changed

### Agent Context Method
- Use conversation history to identify addressed issues
- Cross-reference with current agent knowledge

### Combined Method
- Apply both heuristics for higher accuracy
- Require consensus for automatic resolution

## Error Handling & Safety
- **API Limits**: Respect GitHub's 5,000 queries/hour with backoff
- **Permissions**: Verify write access to PR reviews
- **Dry-Run**: Preview-only mode prevents accidental changes
- **Audit Trail**: Log actions with timestamps and rollback info
- **Thread Mapping**: Handle cases where comments don't map to threads

## Dependencies & Permissions
### Required
- GitHub CLI for API operations
- GraphQL support for thread resolution

### GitHub Scopes
- `repo` (full control) or `pull_requests:write`

## Sample Agent Prompts
```
"Address the code review comments on PR #2201 and resolve the ones that have been completed."

"There are resolved comments on PR #123 based on recent commits - please mark them as resolved."

"Review PR #456 and automatically resolve any comments that match the commit history."
```

The agent will discover and load the github-review-resolver skill, analyze commits and context, and resolve appropriate review threads.

## Output Format
Detailed resolution report:
```
PR Review Resolution Summary
===========================

Pull Request: https://github.com/owner/repo/pull/123
Processed: 2024-01-29 10:30:00 UTC
Threads Analyzed: 25
Threads Resolved: 18
Threads Skipped: 7

Resolved Threads:
- Thread PRRT_xxx (file.js:42): Comment about error handling - addressed by commit abc123
- Thread PRRT_yyy (config.py:15): Documentation update - addressed by commit def456

Unresolved Threads (requiring manual review):
- Thread PRRT_zzz (utils.js:78): Performance concern - no changes detected
- Thread PRRT_aaa (api.py:23): Security question - requires human judgment

Recommendations:
- Review unresolved threads manually
- Consider adding more context in commit messages for better automation
```