---
name: subagents
description: "Search, list, and fetch configured subagents"
---

# Subagents Command

This command triggers the subagents tool to manage configured agents.

## Usage

Run this command to access the configured subagents:
- `/subagents list` - Show all configured subagents
- `/subagents search <query>` - Find subagents by keyword
- `/subagents fetch <name>` - Get full definition for a specific subagent

## What it does

1. Reads the local agent configuration
2. Processes your request (list/search/fetch)
3. Returns information about available subagents

## Examples

- `/subagents list` - Show all configured subagents
- `/subagents search react` - Find React-related subagents
- `/subagents fetch frontend-developer` - Get the full frontend-developer definition

## Trigger phrases

- list subagents
- search subagents
- fetch subagent
- show configured agents