---
name: subagents
description: Tool for listing, searching, and fetching subagents through the global subagents CLI. Use when browsing configured OpenCode agents.
---

# Subagents CLI Catalog Tool

Manage and access subagents through the globally installed `subagents` CLI. The
CLI handles `$HOME/.config/opencode/agents/` path resolution from any working
directory.

---

## The Job

1. Receive user request for subagent operations (`list`, `search`, `fetch`)
2. Run the matching global `subagents` CLI command
3. Return the CLI output faithfully, with concise explanation only when useful

**Important:** All operations are local. Do not make network requests.

---

## Step 1: Parse User Request

Identify the operation type:
- **list**: Show all categories and their subagents
- **search <query>**: Find subagents matching keywords in name or description
- **fetch <name>**: Get the full markdown content for a specific subagent

---

## Step 2: Run the CLI

Use the global CLI as the source of truth:

- `subagents list`
- `subagents search <query>`
- `subagents fetch <name>`

If the CLI is unavailable, report that `subagents` must be installed through
the dotfiles `make install` workflow and stop. Manual filesystem scanning is a
fallback only when the user explicitly asks for debugging the CLI itself.

When fallback scanning is explicitly requested:

1. Use glob with absolute path: `glob` with `path="$HOME/.config/opencode/agents"` and `pattern="*.md"`
2. Handle missing directory with setup instructions
3. Parse YAML frontmatter and filenames for metadata

### Frontmatter Extraction Pattern
Use read to get file contents, then parse YAML between `---` markers:
```
---
name: backend-developer
description: Senior backend engineer for scalable APIs
tools: postgresql_execute_query, jira_search_issues
---
```

### Categorization Logic
Extract category from filename prefixes:
- `backend-*` → Backend Development
- `frontend-*` → Frontend Development  
- `devops-*` → DevOps & Infrastructure
- `qa-*` → Quality & Testing
- `security-*` → Security
- `data-*` → Data & Analytics
- `ui-*` → UI/UX Design
- `mobile-*` → Mobile Development
- `cloud-*` → Cloud & Platform
- `docs-*` → Documentation
- Other → General

---

## Step 3: Process Request

### For List Operation
Run `subagents list`. The CLI handles collection, categorization, and
formatting.

Expected shape:
```
## Backend Development
- backend-developer: Senior backend engineer for scalable APIs
- database-architect: Database design and optimization expert

## Frontend Development  
- frontend-developer: React/Vue/Angular specialist
- ui-designer: User interface and experience designer
...
```

### For Search Operation
Run `subagents search <query>`. The CLI searches names, descriptions, tools,
and available metadata.

Expected shape:
```
Found 3 matching subagents:

## Security-Related Subagents
- security-engineer (Infrastructure): Security specialist for cloud infrastructure
- security-auditor (Quality): Security vulnerability assessment expert
- backend-security (Backend): API security and authentication specialist
```

### For Fetch Operation
Run `subagents fetch <name>`. The CLI returns the full definition or suggestions
for similar names.

---

## Output Format

- Use markdown formatting for readability
- Include category names for organization
- Show brief descriptions in lists
- Return full content for fetches
- Include tool lists for context

---

## Error Handling

### No Agents Directory Found
```
No subagents found in $HOME/.config/opencode/agents/

To set up subagents:
1. Create the directory: mkdir -p $HOME/.config/opencode/agents
2. Add agent definition files as .md files with YAML frontmatter
3. Example agent file:
   ---
   name: backend-developer
   description: Senior backend engineer for scalable APIs
   tools: postgresql_execute_query, jira_search_issues
   ---
   
   # Backend Developer
   
   Expert in building scalable backend systems...
```

### No Search Results
```
No subagents found matching "keyword"

Try these alternatives:
- Search for different keywords
- Use `/subagents list` to see all available agents
- Check for typos in your search query
```

### Agent Not Found for Fetch
```
Subagent "agent-name" not found

Did you mean:
- similar-agent-name (Backend Development)
- agent-name-alt (Infrastructure)

Use `/subagents list` to see all available agents.
```

---

## Examples

### List all subagents:
```
## Backend Development
- backend-developer: Senior backend engineer for scalable APIs
  Tools: postgresql_execute_query, jira_search_issues
- database-architect: Database design and optimization expert
  Tools: postgresql_execute_query

## Frontend Development  
- frontend-developer: React/Vue/Angular specialist
  Tools: chrome_click, chrome_fill, playwright_browser_evaluate
```

### Search for "security":
```
Found 3 matching subagents:

## Security-Related Subagents
- security-engineer (Infrastructure): Security specialist for cloud infrastructure
  File: security-engineer.md
  Tools: jira_search_issues, bash
  
- security-auditor (Quality): Security vulnerability assessment expert  
  File: qa-security-auditor.md
  Tools: jira_search_issues, grep
```

### Fetch backend-developer:
```
# Backend Developer

---
name: backend-developer
description: Senior backend engineer for scalable APIs
tools: postgresql_execute_query, jira_search_issues
category: backend
---

## Overview

Expert in building scalable backend systems with focus on API design, database architecture, and performance optimization.

## Capabilities

- Database design and optimization
- API development and documentation
- Performance troubleshooting
- Security best practices
- System architecture design

## Tools Available

- PostgreSQL database operations
- Jira issue tracking and management
- Code review and analysis
- Deployment automation

## Usage

Perfect for tasks involving backend development, database work, and API design.
```

---

## File Structure Requirements

Agents should be stored as `.md` files in `$HOME/.config/opencode/agents/` with:

1. **YAML Frontmatter** with required fields:
   - `name`: Human-readable agent name
   - `description`: Brief description of capabilities
   - `tools`: Comma-separated list of available tools
   - `category` (optional): Override auto-categorization

2. **Filename** following naming convention:
   - Use hyphens for spaces: `backend-developer.md`
   - Include category prefix for auto-categorization: `backend-`, `frontend-`, etc.

3. **Markdown Body** with sections like:
   - Overview
   - Capabilities  
   - Usage examples
   - Tool documentation
