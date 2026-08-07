---
name: godot-sprite
description: Generate and integrate pixel-art sprites for a Godot 4 project
agent: godot-sprite-artist
---

Use the `godot-sprite-forge` skill to create the following sprite asset:

$ARGUMENTS

Inspect the active workspace before choosing paths, frame dimensions, animation
names, or integration targets. Present the asset contract and planned
subscription-backed image calls before invoking `gpt_imagegen`. Use only
project-relative image paths, inspect each result, and validate any Godot
resource or scene changes with the installed `godot` command.

If `$ARGUMENTS` contains `--plan-only`, produce the asset contract, generation
prompts, expected output paths, and Godot integration plan without invoking
`gpt_imagegen` or changing project files.
