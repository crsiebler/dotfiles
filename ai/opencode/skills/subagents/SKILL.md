---
name: subagents
description: Tool for searching, listing, and fetching subagents from the VoltAgent catalog. Allows browsing available subagents, searching by keywords, and retrieving full definitions.
tools: webfetch
---

# Subagents Catalog Tool

Manage and access subagents from the VoltAgent awesome-claude-code-subagents repository.

---

## The Job

1. Receive user request for subagent operations (list, search, fetch)
2. Fetch the latest catalog from the VoltAgent repository
3. Parse and filter subagent information as requested
4. Return formatted results to the user

**Important:** Always fetch fresh data from the repository to ensure up-to-date information.

---

## Step 1: Parse User Request

Identify the operation type:
- **list**: Show all categories and their subagents
- **search <query>**: Find subagents matching keywords in name or description
- **fetch <name>**: Get the full markdown content for a specific subagent

---

## Step 2: Fetch Catalog Data

Use webfetch to retrieve the README.md from:
https://raw.githubusercontent.com/VoltAgent/awesome-claude-code-subagents/main/README.md

Parse the markdown to extract:
- Category names and numbers
- Subagent names and descriptions
- Links to individual subagent markdown files

---

## Step 3: Process Request

### For List Operation
Return organized list by categories:
```
## 01. Core Development
- api-designer: API architecture expert...
- backend-developer: Senior backend engineer...
...
```

### For Search Operation
Search through names and descriptions, return matches with category context.

### For Fetch Operation
Fetch the specific subagent's markdown from:
https://raw.githubusercontent.com/VoltAgent/awesome-claude-code-subagents/main/categories/{category}/{name}.md

Return the full content.

---

## Output Format

- Use markdown formatting for readability
- Include category numbers for organization
- Show brief descriptions in lists
- Return full content for fetches

---

## Error Handling

If fetch fails:
- Inform user of network issue
- Suggest retrying
- Provide alternative search methods

If subagent not found:
- Suggest similar names
- Recommend using search instead

---

## Examples

### List all subagents:
```
## 01. Core Development
- api-designer: API architecture expert designing scalable interfaces
- backend-developer: Senior backend engineer for scalable APIs
...

## 02. Language Specialists
...
```

### Search for "security":
```
Found 5 matching subagents:

## Security-Related Subagents
- security-engineer (03-infrastructure): Infrastructure security specialist
- security-auditor (04-quality-security): Security vulnerability expert
- ad-security-reviewer (04-quality-security): Active Directory security specialist
...
```

### Fetch api-designer:
```
# API Designer Subagent

---
name: api-designer
description: API architecture expert...
...

[Full markdown content]
```