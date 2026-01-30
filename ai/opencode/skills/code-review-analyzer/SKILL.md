---
name: code-review-analyzer
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

## Comment Quality & Feasibility Assessment

### What Constitutes a Good Code Review Comment
A good code review comment is:
- **Technically sound**: Correct for the specific codebase, stack, and constraints
- **Context-aware**: Considers existing functionality, backward compatibility, and architectural decisions
- **Actionable**: Clear enough to implement without additional clarification
- **Necessary**: Avoids YAGNI (You Aren't Gonna Need It) - doesn't suggest unused features
- **Non-breaking**: Doesn't introduce regressions or break existing functionality
- **Scoped appropriately**: Addresses real issues rather than theoretical "professional" improvements

### Bad Comment Characteristics to Watch For
- Vague or unclear requirements that need clarification before assessment
- Performative suggestions without technical justification
- Suggestions that conflict with established architectural decisions
- Features suggested for "professional" reasons but not actually used (YAGNI)

### Feasibility Analysis Framework
Before implementation planning, assess each comment's feasibility using these checks:

1. **Codebase verification**: Check if suggestion works with current implementation
2. **Impact assessment**: Evaluate if it breaks existing functionality or compatibility
3. **Usage validation**: Verify if suggested features are actually needed/used
4. **Context completeness**: Ensure reviewer understands full system context
5. **Technical correctness**: Validate against platform/version requirements
6. **Architectural alignment**: Check against established patterns and decisions

### Real-World Examples

**Example: Technical Verification**
```
Reviewer: "Remove legacy code"
❌ Bad: "You're absolutely right! Let me remove that..."
✅ Good: "Checking... build target is 10.15+, this API needs 13+. Need legacy for backward compat. Current impl has wrong bundle ID - fix it or drop pre-13 support?"
```

**Example: YAGNI Check**
```
Reviewer: "Implement proper metrics tracking with database, date filters, CSV export"
✅ Analysis: "Grepped codebase - nothing calls this endpoint. Remove it (YAGNI)? Or is there usage I'm missing?"
```

**Example: Unclear Feedback Handling**
```
Reviewer: "Fix items 1-6"
✅ Analysis: "Understand 1,2,3,6. Need clarification on 4 and 5 before assessing feasibility."
```

### Flagging Guidelines
Comments should be flagged for human review if they:
- Have unclear technical requirements or scope
- Suggest changes that would break existing functionality
- Propose features that aren't used in the current codebase
- Lack sufficient context about system constraints
- Conflict with documented architectural decisions

### Integration with Impact Assessment
Feasibility analysis directly affects priority levels:
- Comments passing all checks receive appropriate High/Medium/Low impact ratings
- Comments failing feasibility get flagged as "Requires Human Review" with specific reasoning
- Unclear comments are categorized separately until clarified

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