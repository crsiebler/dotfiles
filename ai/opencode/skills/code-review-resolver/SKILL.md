---
name: code-review-resolver
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

## Temporary File Management
All temporary files MUST be created in the current working directory to avoid OpenCode permission prompts.

### File Naming Convention
- Pattern: `./.code-review-temp-{timestamp}-{pr_number}-{descriptor}.json`
- Example: `./.code-review-temp-20260130153045-2202-comments.json`

### Directory Structure
```bash
# Create temp directory at skill start
TEMP_DIR="./.code-review-temp-$(date +%s)-${pr_number}"
mkdir -p "$TEMP_DIR"

# Use for all temporary files
COMMENTS_FILE="$TEMP_DIR/comments.json"
THREADS_FILE="$TEMP_DIR/threads.json"
VALIDATION_FILE="$TEMP_DIR/validation.json"
```

### Cleanup Requirements
CRITICAL: Always cleanup temporary files as the FINAL action of the skill, even if errors occur:

```bash
# Cleanup function (call at script exit)
cleanup_temp_files() {
  if [ -d "$TEMP_DIR" ]; then
    echo "Cleaning up temporary files..."
    rm -rf "$TEMP_DIR"
    echo "✓ Cleanup complete"
  fi
}

# Register cleanup on exit
trap cleanup_temp_files EXIT
```

### Why Current Working Directory?
- ✅ No OpenCode permission prompts (working directory always accessible)
- ✅ Context-aware location (files stored where PR work happens)
- ✅ Easy debugging (visible in file tree during execution)
- ✅ Automatic isolation (timestamp prevents conflicts)
- ✅ Clean audit trail (can review temp files if skill fails)

### Anti-Patterns to Avoid
- ❌ NEVER use `/tmp/` - triggers OpenCode permission prompts
- ❌ NEVER use `/var/tmp/` - same issue
- ❌ NEVER use absolute paths outside working directory
- ❌ NEVER skip cleanup - leaves orphaned temp files

## Step-by-Step Execution Flow
1. **Repository Detection**: Auto-detect repo owner/name from git remote
2. **Validation**: Check PR accessibility and GitHub API permissions
3. **Data Fetching**: Query PR review comments via REST API
4. **Thread Mapping**: Use GraphQL to map comments to thread IDs
5. **Resolution Analysis**: Apply heuristics to identify addressed comments
6. **Confirmation**: Show proposed resolutions and replies (unless auto-resolve enabled)
7. **Response Generation**: Post technical replies using correct endpoint
   - Extract comment_id from each review comment's `id` field
   - Use endpoint: `/pulls/{pr_number}/comments/{comment_id}/replies`
   - Store posted reply IDs for validation
8. **Validation**: Verify each posted reply has `in_reply_to_id` populated
   - If null, reply was posted as top-level comment (error)
   - Track all validation failures for correction
9. **Auto-Correction**: Delete and repost any incorrectly posted comments
   - Only correct comments posted in current session
   - Use DELETE endpoint, then repost with correct endpoint
   - Validate corrections succeeded
10. **Resolution**: Execute GraphQL mutations to resolve approved threads
11. **Reporting**: Generate summary of actions, validation, and recommendations

## GitHub API Integration
### Fetch Review Comments (REST API)
```bash
# Store in working directory (not /tmp/) to avoid permission prompts
gh api repos/$repo_owner/$repo_name/pulls/$pr_number/comments > "$COMMENTS_FILE"
```

**CRITICAL:** Always use working directory variables like `$COMMENTS_FILE` defined in the temp directory structure above. Never hardcode paths or use `/tmp/`.

Returns all PR review comments with IDs, timestamps, and file context.

### Extract Comment IDs from Response
When fetching review comments, extract the `id` field for each comment:

```bash
# Fetch all review comments and extract IDs
gh api repos/$repo_owner/$repo_name/pulls/$pr_number/comments \
  --jq '.[] | {id: .id, body: (.body | .[0:100]), path: .path, line: .line}'

# Example output:
# {
#   "id": 1234567890,
#   "body": "Group voting passes `decision: 'Yes'` / `'No'` into...",
#   "path": "ActionDecisionPendingButtons.vue",
#   "line": null
# }
```

Store each comment's `id` field to use as `$comment_id` when posting replies.

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

### Post Reply to Review Comment (REST API)

**CRITICAL: Use the correct endpoint to create threaded replies**

```bash
# ✅ CORRECT: Creates a reply in the review comment thread
gh api repos/$repo_owner/$repo_name/pulls/$pr_number/comments/$comment_id/replies \
  -X POST \
  -f body="$REPLY_TEXT"

# Example with actual values:
gh api repos/owner/myrepo/pulls/123/comments/1234567890/replies \
  -X POST \
  -f body="Fixed: Added null check in error handler"
```

**Extract comment_id from review comments:**
```bash
# Get review comments with their IDs
COMMENTS=$(gh api repos/$repo_owner/$repo_name/pulls/$pr_number/comments)

# Extract specific comment ID
COMMENT_ID=$(echo "$COMMENTS" | jq -r '.[] | select(.path == "file.js" and .line == 42) | .id')
```

**⚠️ COMMON MISTAKES - DO NOT USE THESE ENDPOINTS:**
```bash
# ❌ WRONG: Creates top-level PR conversation comment
gh api repos/$repo_owner/$repo_name/issues/$pr_number/comments -f body="text"
gh pr comment $pr_number --body "text"

# ❌ WRONG: Creates new review comment (not a reply)
gh api repos/$repo_owner/$repo_name/pulls/$pr_number/comments -f body="text" -f commit_id="..." -f path="..." -f line=1

# ✅ CORRECT: Creates threaded reply to review comment
gh api repos/$repo_owner/$repo_name/pulls/$pr_number/comments/$comment_id/replies -f body="text"
```

**Verify the reply was posted correctly:**
```bash
# Check that in_reply_to_id is populated (confirms threaded reply)
gh api repos/$repo_owner/$repo_name/pulls/comments/$new_comment_id \
  --jq '{id, in_reply_to_id, body: (.body | .[0:60])}'

# Correct response:
# {
#   "id": 2747500123,
#   "in_reply_to_id": 1234567890,  ← Must reference original comment
#   "body": "Fixed: Added null check in error handler"
# }

# If in_reply_to_id is null, the reply was posted incorrectly (top-level)
```

Posts a reply to a specific PR review comment thread with the resolution status and description.

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

## Response Generation
For each comment approved for resolution, generate and post a technical reply before marking the thread as resolved. This step only executes when:

- `auto_resolve: true` (automatic execution)
- OR user explicitly approves the proposed actions in dry-run mode
- Skipped entirely when `dry_run: true` without approval

### Reply Format
"[Status]: [Brief description of change made]"
- Examples:
  - "Fixed: Added null check in error handler to prevent crashes"
  - "Implemented: Refactored function to use async/await pattern"
  - "Declined: Breaks backward compatibility with existing API consumers"
  - "Addressed: Updated documentation to clarify parameter usage"

### Status Options
- "Fixed" - Bug or issue resolved
- "Implemented" - Feature or improvement added
- "Addressed" - Documentation or style issue resolved
- "Declined" - Suggestion not implemented (with technical reasoning)

### Session Tracking
Track all comments posted in the current session for validation and potential correction:

- Record timestamp when skill execution begins
- Store comment IDs returned by POST operations
- Filter validation to only comments created after session start
- Only auto-delete comments created by the current skill execution

```bash
# Record session start time
SESSION_START=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# After posting, extract and store the new comment ID
NEW_COMMENT_ID=$(gh api repos/$owner/$repo/pulls/$pr_number/comments/$original_comment_id/replies \
  -X POST \
  -f body="$REPLY_TEXT" \
  --jq '.id')

# Add to session tracking array
SESSION_COMMENT_IDS+=($NEW_COMMENT_ID)
```

### Validation Workflow
After each reply is posted:

1. **Immediate Validation**: Check `in_reply_to_id` field
2. **Track Result**: Record success/failure with comment details
3. **Continue Processing**: Don't stop on validation failure
4. **Batch Correction**: After all replies posted, correct any failures

```bash
# Validate a posted reply
validate_reply() {
  local comment_id=$1
  local expected_parent_id=$2
  
  VALIDATION=$(gh api repos/$owner/$repo/pulls/comments/$comment_id \
    --jq '{id, in_reply_to_id, created_at}')
  
  ACTUAL_PARENT=$(echo "$VALIDATION" | jq -r '.in_reply_to_id')
  
  if [ "$ACTUAL_PARENT" = "null" ]; then
    echo "VALIDATION_FAILED:$comment_id:$expected_parent_id"
    return 1
  elif [ "$ACTUAL_PARENT" != "$expected_parent_id" ]; then
    echo "VALIDATION_WRONG_PARENT:$comment_id:$expected_parent_id:$ACTUAL_PARENT"
    return 1
  else
    echo "VALIDATION_SUCCESS:$comment_id"
    return 0
  fi
}
```

### Posting Replies
Use GitHub API to reply in comment threads using the `/replies` endpoint. Process:

1. Post reply to review comment
2. Extract returned comment ID
3. Immediately validate `in_reply_to_id` field
4. Track validation result
5. Continue to next comment
6. After all posts complete, auto-correct failures

Replies are posted after user confirmation (unless `auto_resolve: true`) to ensure transparency and control.

## Error Handling & Safety
- **API Limits**: Respect GitHub's 5,000 queries/hour with backoff
- **Permissions**: Verify write access to PR reviews
- **Dry-Run**: Preview-only mode prevents accidental changes (replies only posted after explicit approval)
- **Auto-Resolve**: When enabled, skips confirmations and posts replies automatically
- **Audit Trail**: Log actions with timestamps and rollback info
- **Thread Mapping**: Handle cases where comments don't map to threads
- **Validation Failures**: Track all validation failures; don't fail immediately
- **Auto-Correction Errors**: Log correction attempts and failures for end report
- **Incorrect Posting Detection**: Automatically detect `in_reply_to_id: null` as error
- **Session Isolation**: Only attempt to correct comments created in current session
- **Correction Retry**: If repost still fails validation, report to user for manual intervention
- **Temp File Cleanup**: Always remove temporary files via `trap cleanup EXIT`
- **Working Directory Only**: Never use `/tmp/` or absolute paths outside working directory
- **Permission Safety**: Using working directory prevents OpenCode permission prompts

## Validation & Auto-Correction

### Validation Process
Every reply posted by the skill MUST be validated immediately:

```bash
# Validation function for posted replies
validate_posted_replies() {
  local session_start="$1"
  local username="$2"
  
  # Fetch all comments posted by this user after session start
  POSTED_COMMENTS=$(gh api repos/$owner/$repo/pulls/$pr_number/comments \
    --jq --arg start "$session_start" --arg user "$username" \
    '[.[] | select(.user.login == $user and .created_at > $start)]')
  
  # Check each comment's in_reply_to_id
  VALIDATION_FAILURES=()
  VALIDATION_SUCCESSES=()
  
  echo "$POSTED_COMMENTS" | jq -c '.[]' | while read -r comment; do
    COMMENT_ID=$(echo "$comment" | jq -r '.id')
    IN_REPLY_TO=$(echo "$comment" | jq -r '.in_reply_to_id')
    BODY=$(echo "$comment" | jq -r '.body | .[0:50]')
    
    if [ "$IN_REPLY_TO" = "null" ]; then
      VALIDATION_FAILURES+=("$COMMENT_ID|$BODY")
      echo "❌ FAILED: Comment $COMMENT_ID posted as top-level (in_reply_to_id is null)"
    else
      VALIDATION_SUCCESSES+=("$COMMENT_ID|$IN_REPLY_TO")
      echo "✓ SUCCESS: Comment $COMMENT_ID correctly replied to $IN_REPLY_TO"
    fi
  done
  
  echo "${#VALIDATION_FAILURES[@]} failures, ${#VALIDATION_SUCCESSES[@]} successes"
}
```

### Auto-Correction Process
When validation detects incorrectly posted comments, automatically fix them:

```bash
# Auto-correct incorrectly posted comments
auto_correct_replies() {
  local failures=("$@")
  
  CORRECTED_COUNT=0
  CORRECTION_ERRORS=()
  
  for failure in "${failures[@]}"; do
    INCORRECT_ID=$(echo "$failure" | cut -d'|' -f1)
    ORIGINAL_BODY=$(echo "$failure" | cut -d'|' -f2)
    TARGET_COMMENT_ID=$(echo "$failure" | cut -d'|' -f3)  # Original comment to reply to
    
    echo "Correcting comment $INCORRECT_ID..."
    
    # Step 1: Delete the incorrectly posted comment
    DELETE_RESULT=$(gh api repos/$owner/$repo/pulls/comments/$INCORRECT_ID -X DELETE 2>&1)
    
    if [ $? -eq 0 ]; then
      echo "  ✓ Deleted incorrect comment $INCORRECT_ID"
      
      # Step 2: Repost using correct endpoint
      NEW_COMMENT=$(gh api repos/$owner/$repo/pulls/$pr_number/comments/$TARGET_COMMENT_ID/replies \
        -X POST \
        -f body="$ORIGINAL_BODY" 2>&1)
      
      if [ $? -eq 0 ]; then
        NEW_ID=$(echo "$NEW_COMMENT" | jq -r '.id')
        NEW_PARENT=$(echo "$NEW_COMMENT" | jq -r '.in_reply_to_id')
        
        if [ "$NEW_PARENT" != "null" ]; then
          echo "  ✓ Reposted correctly as comment $NEW_ID (reply to $NEW_PARENT)"
          CORRECTED_COUNT=$((CORRECTED_COUNT + 1))
        else
          CORRECTION_ERRORS+=("$NEW_ID: Repost still has null in_reply_to_id")
          echo "  ❌ Repost failed validation (still null in_reply_to_id)"
        fi
      else
        CORRECTION_ERRORS+=("Failed to repost: $NEW_COMMENT")
        echo "  ❌ Repost failed: $NEW_COMMENT"
      fi
    else
      CORRECTION_ERRORS+=("$INCORRECT_ID: Failed to delete - $DELETE_RESULT")
      echo "  ❌ Delete failed: $DELETE_RESULT"
    fi
  done
  
  echo "Auto-correction complete: $CORRECTED_COUNT successfully corrected"
  
  if [ ${#CORRECTION_ERRORS[@]} -gt 0 ]; then
    echo "Correction errors:"
    printf '%s\n' "${CORRECTION_ERRORS[@]}"
  fi
}
```

### Validation Report
Generate detailed validation report for user transparency:

```markdown
Validation Summary:
==================
Total Replies Posted: 18
Successfully Validated: 15 ✓
Validation Failures: 3 ❌

Auto-Correction Results:
========================
Corrections Attempted: 3
Successfully Corrected: 3 ✓
Correction Failures: 0

Corrected Comments:
- Comment 2747500111: Deleted top-level, reposted as reply to 1234567890
- Comment 2747500112: Deleted top-level, reposted as reply to 1234567891
- Comment 2747500113: Deleted top-level, reposted as reply to 1234567892

Final Status: All replies correctly posted as threaded responses ✓
```

## Troubleshooting

### Diagnosis: Are replies posting correctly?

**Quick Check Command:**
```bash
# Check recent comments for in_reply_to_id status
gh api repos/$owner/$repo/pulls/$pr_number/comments \
  --jq '[.[] | select(.created_at > "2026-01-30T00:00:00Z") | {id, in_reply_to_id, body: (.body | .[0:50]), user: .user.login}]'
```

**What to look for:**
- ✅ `in_reply_to_id` has a number → Correctly posted as reply
- ❌ `in_reply_to_id` is `null` → Incorrectly posted as top-level comment

### Common Issues

#### Issue 1: All replies show `in_reply_to_id: null`

**Cause**: Using wrong endpoint

**Solutions**:
- Verify using `/pulls/{pr_number}/comments/{comment_id}/replies`
- NOT using `/issues/{issue_number}/comments`
- NOT using `gh pr comment` command

**Fix**:
```bash
# Find the incorrect endpoint usage in your script
grep -n "gh api.*issues.*comments" your_script.sh
grep -n "gh pr comment" your_script.sh

# Replace with correct endpoint
# /issues/{issue_number}/comments → /pulls/{pr_number}/comments/{comment_id}/replies
```

#### Issue 2: 404 Error when posting reply

**Cause**: Invalid comment_id or using wrong ID type

**Solutions**:
- Verify `comment_id` is the numeric `id` field from REST API (not `node_id`)
- Confirm comment exists and is a review comment (not issue comment)
- Check you're using pull_number (not issue number)

**Diagnostic**:
```bash
# Verify comment exists and get its details
gh api repos/$owner/$repo/pulls/comments/$comment_id \
  --jq '{id, pull_request_review_id, path, line, body: (.body | .[0:50])}'

# If 404, comment doesn't exist or wrong ID type
```

#### Issue 3: Auto-correction fails

**Cause**: Permission issues or rate limiting

**Solutions**:
- Verify GitHub token has `pull_requests:write` scope
- Check rate limit: `gh api rate_limit`
- Ensure bot user has permission to delete own comments

**Diagnostic**:
```bash
# Check current rate limit
gh api rate_limit --jq '.resources.core'

# Check authentication scopes
gh api user --jq '.login' && gh auth status
```

### Manual Cleanup

If auto-correction fails, manually clean up incorrect comments:

```bash
# Find all top-level comments that should be replies
INCORRECT_COMMENTS=$(gh api repos/$owner/$repo/pulls/$pr_number/comments \
  --jq '[.[] | select(.user.login == "YOUR_BOT" and .in_reply_to_id == null and .created_at > "2026-01-30T00:00:00Z") | .id]')

# Delete each one
echo "$INCORRECT_COMMENTS" | jq -r '.[]' | while read cid; do
  echo "Deleting comment $cid..."
  gh api repos/$owner/$repo/pulls/comments/$cid -X DELETE
done

# Now rerun the skill to post correctly
```

#### Issue 4: OpenCode Permission Prompts for /tmp/ Access

**Cause**: Skill or subagent attempting to write to `/tmp/` or other external directories

**Symptoms**:
- "Permission Required: Access External Directory" prompt appears
- Subagent cannot continue without user intervention
- Autonomous workflow breaks

**Solutions**:
1. Verify all temp file paths use working directory:
   ```bash
   # ❌ WRONG - triggers permission prompt
   gh api ... > /tmp/pr_data.json
   
   # ✅ CORRECT - no permission prompt
   gh api ... > "$TEMP_DIR/pr_data.json"
   ```

2. Ensure temp directory is created in working directory:
   ```bash
   TEMP_DIR="./.code-review-temp-$(date +%s)-${PR_NUMBER}"
   mkdir -p "$TEMP_DIR"
   ```

3. Verify cleanup is registered:
   ```bash
   trap cleanup_temp_files EXIT
   ```

**Diagnostic**:
```bash
# Check where temp files are being created
ps aux | grep "gh api" | grep -o "/[^ ]*\.json"

# Expected: paths starting with ./
# Problem: paths starting with /tmp/ or /var/
```

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

## Complete Workflow Example

### Example: Resolving PR Comments

```bash
#!/bin/bash

# Configuration
REPO_OWNER="owner"
REPO_NAME="repository"
PR_NUMBER=123
SESSION_START=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
BOT_USERNAME=$(gh api user --jq '.login')

# ===== TEMPORARY FILE SETUP (REQUIRED) =====
# Create unique temp directory in current working directory
TIMESTAMP=$(date +%s)
TEMP_DIR="./.code-review-temp-${TIMESTAMP}-${PR_NUMBER}"
mkdir -p "$TEMP_DIR"

# Define all temp file paths
COMMENTS_FILE="$TEMP_DIR/comments.json"
THREADS_FILE="$TEMP_DIR/threads.json"
VALIDATION_FILE="$TEMP_DIR/validation.json"
SESSION_FILE="$TEMP_DIR/session.json"

# Register cleanup handler
cleanup_temp_files() {
  if [ -d "$TEMP_DIR" ]; then
    echo ""
    echo "Cleaning up temporary files..."
    rm -rf "$TEMP_DIR"
    echo "✓ Temporary files removed: $TEMP_DIR"
  fi
}
trap cleanup_temp_files EXIT
echo "✓ Temp directory created: $TEMP_DIR"
echo ""
# ===== END TEMPORARY FILE SETUP =====

# Track session comments
declare -a SESSION_COMMENT_IDS
declare -a VALIDATION_FAILURES

# Step 1: Fetch review comments (store in working directory)
echo "Fetching review comments..."
COMMENTS=$(gh api repos/$REPO_OWNER/$REPO_NAME/pulls/$PR_NUMBER/comments | tee "$COMMENTS_FILE")

# Step 2: Analyze which comments have been addressed
# (Application of resolution logic here - commit history, agent context, etc.)

# Step 3: Post replies to resolved comments
echo "Posting replies to resolved comments..."

# Example: Post reply to a review comment
COMMENT_ID=1234567890
REPLY_BODY="Fixed: Added null check in error handler to prevent crashes"

echo "Posting reply to comment $COMMENT_ID..."
POSTED_REPLY=$(gh api repos/$REPO_OWNER/$REPO_NAME/pulls/$PR_NUMBER/comments/$COMMENT_ID/replies \
  -X POST \
  -f body="$REPLY_BODY")

NEW_COMMENT_ID=$(echo "$POSTED_REPLY" | jq -r '.id')
SESSION_COMMENT_IDS+=($NEW_COMMENT_ID)

echo "  Posted as comment $NEW_COMMENT_ID"

# Step 4: Validate immediately
echo "Validating reply $NEW_COMMENT_ID..."
VALIDATION=$(gh api repos/$REPO_OWNER/$REPO_NAME/pulls/comments/$NEW_COMMENT_ID \
  --jq '{id, in_reply_to_id}')

IN_REPLY_TO=$(echo "$VALIDATION" | jq -r '.in_reply_to_id')

if [ "$IN_REPLY_TO" = "null" ]; then
  echo "  ❌ VALIDATION FAILED: in_reply_to_id is null"
  VALIDATION_FAILURES+=("$NEW_COMMENT_ID|$REPLY_BODY|$COMMENT_ID")
else
  echo "  ✓ VALIDATION PASSED: Correctly replied to $IN_REPLY_TO"
fi

# Step 5: Continue with remaining comments...
# (Repeat steps 3-4 for each comment)

# Step 6: Auto-correct any failures
if [ ${#VALIDATION_FAILURES[@]} -gt 0 ]; then
  echo ""
  echo "Auto-correcting ${#VALIDATION_FAILURES[@]} failed replies..."
  
  for failure in "${VALIDATION_FAILURES[@]}"; do
    INCORRECT_ID=$(echo "$failure" | cut -d'|' -f1)
    ORIGINAL_BODY=$(echo "$failure" | cut -d'|' -f2)
    TARGET_ID=$(echo "$failure" | cut -d'|' -f3)
    
    echo "Correcting comment $INCORRECT_ID..."
    
    # Delete incorrect comment
    gh api repos/$REPO_OWNER/$REPO_NAME/pulls/comments/$INCORRECT_ID -X DELETE
    echo "  Deleted incorrect comment"
    
    # Repost correctly
    REPOSTED=$(gh api repos/$REPO_OWNER/$REPO_NAME/pulls/$PR_NUMBER/comments/$TARGET_ID/replies \
      -X POST \
      -f body="$ORIGINAL_BODY")
    
    NEW_ID=$(echo "$REPOSTED" | jq -r '.id')
    NEW_PARENT=$(echo "$REPOSTED" | jq -r '.in_reply_to_id')
    
    echo "  ✓ Reposted as comment $NEW_ID (reply to $NEW_PARENT)"
  done
fi

# Step 7: Resolve threads via GraphQL
# (Resolve threads using GraphQL mutations)

# Step 8: Generate summary report
echo ""
echo "========================================"
echo "PR Review Resolution Complete"
echo "========================================"
echo "Replies Posted: ${#SESSION_COMMENT_IDS[@]}"
echo "Validation Failures: ${#VALIDATION_FAILURES[@]}"
echo "Corrections Applied: ${#VALIDATION_FAILURES[@]}"
echo "Final Status: All replies correctly posted ✓"
```

## Output Format
Detailed resolution report with validation and correction results:

```
PR Review Resolution Summary
===========================

Pull Request: https://github.com/owner/repo/pull/123
Session Started: 2024-01-29 10:30:00 UTC
Session Ended: 2024-01-29 10:35:23 UTC
Duration: 5m 23s

Analysis Results:
-----------------
Threads Analyzed: 25
Threads Resolved: 18
Threads Skipped: 7

Reply Posting:
--------------
Replies Posted: 18
Post Failures: 0

Validation Results:
-------------------
Replies Validated: 18
Validation Passed: 15 ✓
Validation Failed: 3 ❌
  - Comment 2747500111: in_reply_to_id was null (posted as top-level)
  - Comment 2747500112: in_reply_to_id was null (posted as top-level)
  - Comment 2747500113: in_reply_to_id was null (posted as top-level)

Auto-Correction:
----------------
Corrections Attempted: 3
Successfully Corrected: 3 ✓
Correction Failures: 0

Final Status: ✓ All replies correctly posted as threaded responses

Resolved Threads:
-----------------
✓ Thread PRRT_xxx (ActionDecisionPendingButtons.vue:42)
  - Original: "Group voting passes `decision: 'Yes'`..."
  - Reply: "Fixed: Normalized decision casing to lowercase"
  - Resolution: Addressed by commit abc123
  
✓ Thread PRRT_yyy (ActionDecisionPendingButtons.vue:58)
  - Original: "`isAcceptButtonLoading`/`isRejectButtonLoading`..."
  - Reply: "Fixed: Loading indicators now work with grouped voting"
  - Resolution: Addressed by commit abc123
  
[... 16 more resolved threads ...]

Unresolved Threads (requiring manual review):
---------------------------------------------
⚠ Thread PRRT_zzz (utils.js:78)
  - Issue: Performance concern - no changes detected
  - Recommendation: Review and address in separate PR
  
⚠ Thread PRRT_aaa (api.py:23)
  - Issue: Security question - requires human judgment
  - Recommendation: Consult security team before resolving

Recommendations:
----------------
✓ All review comments successfully addressed
✓ All replies correctly posted as threaded responses
- Consider adding performance benchmarks for future PRs
- Schedule security review meeting for open questions

API Usage:
----------
REST API Calls: 47
GraphQL Queries: 3
Rate Limit Remaining: 4,953/5,000
```