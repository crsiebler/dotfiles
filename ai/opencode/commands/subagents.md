---
name: subagents
description: Search, list, and fetch configured subagents
---

# Subagents Command

This command is a thin wrapper around the global `subagents` CLI tool. The CLI
manages configured agents from `$HOME/.config/opencode/agents/` regardless of
the current working directory.

## Usage

Run this command to access the configured subagents:
- `/subagents list` - Show all configured subagents
- `/subagents search <query>` - Find subagents by keyword
- `/subagents fetch <name>` - Get full definition for a specific subagent

## What it does

1. Parse the command arguments after `/subagents`.
2. If no arguments are provided, run `subagents list`.
3. Otherwise run `subagents <arguments>` exactly.
4. Return stdout and stderr faithfully.

## Important

If the `subagents` command is unavailable, report that it must be installed via
this dotfiles repository's `make install` workflow and stop. Do not fall back to
manual path assumptions in this command.

## Examples

- `/subagents list` - Show all configured subagents
- `/subagents search react` - Find React-related subagents
- `/subagents fetch frontend-developer` - Get the full frontend-developer definition

## Trigger phrases

- list subagents
- search subagents
- fetch subagent
- show configured agents
