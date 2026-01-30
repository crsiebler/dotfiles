---
name: ralph
description: "Convert PRD to prd.json format for Ralph autonomous execution"
---

# Ralph Command

This command triggers the Ralph skill to convert an existing PRD to the JSON format required for autonomous execution.

## Usage

Run this command after creating a PRD to prepare it for the Ralph autonomous loop.

## What it does

1. Parses the markdown PRD file
2. Splits requirements into small, implementable user stories  
3. Creates `prd.json` with proper structure for Ralph execution
4. Ensures each story has verifiable acceptance criteria

**Note: This command ONLY prepares the JSON file. It does NOT start implementation or the autonomous loop. Run the `ralph` script separately for actual implementation.**

## Trigger phrases

- convert this prd
- turn this into ralph format
- create prd.json from this
- ralph json

## Requirements

- A PRD markdown file must exist (typically in `tasks/` directory)
- The PRD should follow the standard format with user stories and requirements