---
name: github-review-analyzer
description: Analyze GitHub PR code reviews and provide structured breakdowns of recommendations, impact assessment, and change descriptions
metadata:
  audience: developers, reviewers
  workflow: pull-request-review
---

## What I do
- Fetch all review comments from a GitHub PR using REST API
- Analyze each comment for actionable recommendations and impact level
- Generate clear descriptions of suggested changes with code examples
- Group related comments by theme, file, or priority
- Provide implementation guidance and effort estimates

## When to use me
Use this skill when:
- You need to understand and prioritize code review feedback
- Breaking down complex PR reviews into actionable items
- Assessing the scope and impact of required changes
- Planning implementation of review suggestions

## Parameters
### Required
- `pr_number`: GitHub PR number (e.g., `2201`)

### Optional
- `repo_owner`: Repository owner (auto-detected from current git repo)
- `repo_name`: Repository name (auto-detected from current git repo)
- `analysis_depth`: Analysis detail level - basic/detailed/comprehensive (default: detailed)
- `group_by`: Grouping method - file/theme/priority/author (default: file)
- `include_resolved`: Include already-resolved comments (default: false)
- `max_comments`: Maximum comments to analyze (default: 100)

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
4. **Analysis**: Categorize comments and assess impact
5. **Grouping**: Organize by specified criteria
6. **Reporting**: Generate structured breakdown with recommendations

## GitHub API Integration
### Fetch Review Comments (REST API)
```bash
gh api repos/$repo_owner/$repo_name/pulls/$pr_number/comments
```

Returns all PR review comments with details like body, author, timestamps, file path, and line numbers.

## Analysis Categories
- **Bug Fixes**: Critical issues requiring immediate attention
- **Improvements**: Enhancements to code quality or performance
- **Style Issues**: Code formatting and convention adherence
- **Documentation**: Comments, docstrings, or README updates
- **Architecture**: Design patterns and structural changes

## Impact Assessment
- **High**: Significant code changes, multiple files affected
- **Medium**: Moderate changes, single file or focused area
- **Low**: Minor tweaks, naming, or documentation

## Error Handling
- **API Errors**: Handle rate limits and permission issues
- **Invalid PR**: Validate PR exists and is accessible
- **Large PRs**: Process comments in batches if needed

## Dependencies & Permissions
### Required
- GitHub CLI for API access
- JSON parsing for API responses

### GitHub Scopes
- `repo` (read access) or `pull_requests:read`

## Sample Agent Prompts
```
"Analyze the code reviews on PR #2201 and provide a breakdown of recommendations, impact assessment, and implementation suggestions."

"There are code reviews on PR #123, provide feedback on each comment with priority levels and suggested fixes."

"Review PR #456 comments and group them by file with effort estimates for each change."
```

The agent will discover and load the github-review-analyzer skill, auto-detect the repository from git remote, and execute the analysis workflow.

## Output Format
Structured analysis report:
```
PR Review Analysis Summary
==========================

Pull Request: https://github.com/owner/repo/pull/123
Comments Analyzed: 25
Grouped by: file

File: src/main.js
- Bug Fix (High Impact): Memory leak in event handler - Replace manual cleanup with proper disposal pattern
- Style (Low Impact): Inconsistent variable naming - Use camelCase throughout

File: tests/utils.test.js
- Improvement (Medium Impact): Add error handling for edge cases - Implement try-catch blocks
[...]

Implementation Priority:
1. High impact bug fixes (3 items)
2. Medium impact improvements (5 items)
3. Low impact style/documentation (17 items)
```