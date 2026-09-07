---
name: create-sprite
description: Generate pixel-art sprites and optionally integrate approved assets
agent: sprite-artist
---

Load and follow the `create-sprites` skill for the following sprite asset:

$ARGUMENTS

Inspect the active workspace before choosing paths, frame dimensions, animation
names, or integration targets. Present the asset contract and planned
subscription-backed image calls and require explicit approval before invoking
the exposed OpenCode `gpt_imagegen` provider. Use only
project-relative image paths and inspect each result. Load the skill's Godot
reference only for Godot requests or relevant Godot project context; validate
any Godot resource or scene changes with the installed `godot` command.
Asset-only work does not require a Godot project or binary.

If `$ARGUMENTS` contains `--plan-only`, produce the asset contract, generation
prompts, expected output paths, and any requested integration plan without invoking
`gpt_imagegen` or changing project files.
