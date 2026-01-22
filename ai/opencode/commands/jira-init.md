---
name: jira-init
description: "Generate initial Jira comment"
agent: project-manager
subtask: true
---

# Jira Init Command

This command triggers the project-manager agent to generate initial comment for Jira task $1 using the jira-task-init skill.

## Usage

Run this command when assigned new Jira tasks requiring initial overview.

## What it does

1. Invokes project-manager agent with jira-task-init skill
2. Processes Jira task ID: $1
3. **Enhanced technical analysis**: Automatically coordinates with fullstack-developer subagent for:
   - Codebase complexity and technical debt evaluation
   - Implementation approach recommendations
   - Code-level dependency identification
   - Integration points and API contract analysis
   - Development effort estimation based on actual code
4. Generates structured initial comment with enhanced technical context
5. Returns technically accurate comment ready for posting to Jira

## Trigger phrases

jira init, jira-initial, risk analysis, impact analysis, initial jira comment, jira overview, project overview

## Requirements

- Jira task ID as positional argument (e.g., `/jira-init PROJ-123`)
- Jira MCP server access

## User Error Handling

- Invalid task ID format: Provide format example (e.g., PROJ-123)
- Jira access issues: Verify MCP server connectivity
- Missing task ID: Prompt for required Jira task ID