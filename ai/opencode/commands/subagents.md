---
name: subagents
description: Search, list, and fetch configured subagents
---

# Subagents Command

This command triggers the global `subagents` CLI tool to manage configured agents from `$HOME/.config/opencode/agents/`.

## Usage

Run this command to access the configured subagents:
- `/subagents list` - Show all configured subagents
- `/subagents search <query>` - Find subagents by keyword
- `/subagents fetch <name>` - Get full definition for a specific subagent

## What it does

1. Calls global `subagents` command installed to `/usr/local/bin/subagents`
2. The CLI tool scans `$HOME/.config/opencode/agents/` for agent definitions
3. Processes your request (list/search/fetch)
4. Returns information about available subagents

## Important

The subagents skill calls globally installed `subagents` CLI tool, which provides access to agent files from `$HOME/.config/opencode/agents/` regardless of the current working directory where the command is invoked.

## Examples

- `/subagents list` - Show all configured subagents
- `/subagents search react` - Find React-related subagents
- `/subagents fetch frontend-developer` - Get the full frontend-developer definition

## Trigger phrases

- list subagents
- search subagents
- fetch subagent
- show configured agents