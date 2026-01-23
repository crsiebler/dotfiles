---
name: jira-daily
description: "Generate daily Jira update string"
agent: project-manager
subtask: true
---

# Jira Daily Command

This command triggers the project-manager agent to generate daily update string for Jira task $1 using the jira-daily-update skill.

## Usage

Run this command when providing daily progress updates for Jira tasks.

## What it does

1. Invokes project-manager agent with jira-daily-update skill
2. Processes Jira task ID: $1
3. Generates structured daily update string with 5 required fields
4. Returns formatted update string ready to copy to Jira

## Trigger phrases

jira daily, jira-update, daily update, progress update, jira status, daily status

## Requirements

- Jira task ID as positional argument (e.g., `/jira-daily PROJ-123`)
- Jira MCP server access

## User Error Handling

- Invalid task ID format: Provide format example (e.g., PROJ-123)
- Jira access issues: Verify MCP server connectivity
- Missing task ID: Prompt for required Jira task ID