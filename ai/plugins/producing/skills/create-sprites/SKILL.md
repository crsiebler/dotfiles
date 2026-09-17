---
name: create-sprites
description: Plans and generates pixel-art sprites and animation sheets, processes approved assets, and optionally integrates them into a project.
---

# Create Sprites

Use this workflow for asset-only delivery or optional engine integration. Read
[Godot integration](references/godot.md) only for Godot requests or relevant
Godot project context. Asset-only work requires neither `project.godot` nor a
Godot binary. Never install tools or change global settings implicitly.

## Provider boundary

The documented image provider is OpenCode-only until another harness is verified.
Calling a Codex backend internally does not expose a Codex image-generation tool.
In Codex, offer asset planning or integration of supplied images; do not promise
generation or invent tool names. Inspect the active schema even in OpenCode.
If the provider is unavailable, offer planning or integration of supplied images;
do not invent a provider or substitute code-drawn art.

Create original pixel-art assets through the `gpt_imagegen` tool, visually
validate the results, and deliver accepted assets or integrate them with the
active project when requested.

The image tool uses OpenCode's ChatGPT OAuth subscription. It produces one PNG
per call, supports reference images, and automatically versions an existing
output path instead of overwriting it.

## Preconditions

Before generation:

1. Verify `gpt_imagegen` is available. If it is absent, explain that
   `opencode-gpt-imagegen` must be loaded and OpenCode restarted. Do not replace
   the requested artwork with code-drawn placeholders.
2. Inspect existing sprite directories, reference images, and relevant animation
   code or scenes before choosing paths, dimensions, names, or integration targets.
3. Agree on frame dimensions, grid, anchors, actions, palette, and integration
   target, following the active project's patterns when present.
4. Keep all tool input and output paths relative to the current workspace.
5. Present the complete generation batch, prompts, paths, and subscription use;
   require explicit approval before invoking `gpt_imagegen`. `--plan-only`
   means no generation and no file changes.
6. Confirm additional spending before unapproved retries. Limit regeneration to
   the smallest failed asset; do not silently spend on broad retries.

## Asset Contract

Write a concise contract before generating:

```text
name: <lowercase-slug>
role: player | npc | enemy | boss | prop | projectile | impact | fx
view: top-down | side | three-quarter
style: pixel art description and palette
actions: <ordered list>
grid: <rows>x<columns per action>
frame size: <target runtime pixels>
anchor: feet | bottom-center | center
animations: <name, fps, loop or one-shot>
references: <project-relative paths and roles>
output root: assets/sprites/generated/<slug>/
integration target: asset-only | reusable scene | existing scene
```

Infer routine values from the request and project. Ask the user only when two
materially different interpretations would produce incompatible assets.

## Default Action Plans

| Action | Raw grid | Frames | Playback |
| --- | --- | ---: | --- |
| static | `1x1` | 1 | static |
| idle | `2x2` | 4 | loop |
| walk | `2x3` | 6 | loop |
| run | `2x3` or `2x4` | 6 or 8 | loop |
| attack | `2x2` or `2x3` | 4 or 6 | one-shot |
| cast | `2x3` | 6 | one-shot |
| hurt | `2x2` | 4 | one-shot |
| death | `2x3` | 6 | one-shot |
| projectile | `1x4` or `2x2` | 4 | loop when appropriate |
| impact | `2x2` | 4 | one-shot |
| four-direction walk | `4x4` | 16 | four loops |

Use a multi-row grid for animated bodies. Single-row body sheets are prone to
horizontal drift and cropping. A four-direction sheet is the exception because
all rows represent the same locomotion action.

For a player with multiple actions, generate and review separate idle, movement,
attack, hurt, and death sheets. Assemble a delivery atlas only after each action
passes review.

Keep wide slash arcs, projectiles, muzzle flashes, impacts, and detached dust in
separate effect sheets unless the existing runtime intentionally uses oversized
cells and explicit origins.

## Generation Prompt Contract

Write every prompt manually. Include all applicable constraints:

```text
Create an original pixel-art <asset role> animation sheet.

Subject: <identity, silhouette, costume, palette, equipment>.
View: <top-down, side, or three-quarter>, fixed camera and fixed distance.
Action: <ordered animation phases>.
Layout: exactly <rows>x<columns> equal invisible cells, read left-to-right and
top-to-bottom. No borders, labels, guides, text, UI, or separators.

The same subject identity appears in every cell. Keep identical anatomical
scale, palette, outline weight, lighting direction, and camera distance. Keep
the body root and <feet/bottom/center> anchor stable. Every body part, weapon,
tail, wing, particle, and effect must remain fully inside its own cell with
generous margin. Nothing may cross a cell edge.

Use crisp deliberate pixel clusters, a limited readable palette, hard edges,
and no antialiasing, blur, gradients, painterly texture, or subpixel detail.
Background must be uniformly solid #FF00FF with no shadow, texture, gradient,
or transparency. No text.
```

For grounded characters, require the full body to occupy approximately 60% to
70% of each cell and lock the feet to one shared horizontal line. For floating
effects and projectiles, use a stable center anchor instead.

For four-direction locomotion, specify rows explicitly:

```text
row 1: down
row 2: left
row 3: right
row 4: up
```

Use an accepted project image as a reference when identity or style continuity
matters. Pass it in `images` and describe it in the prompt, for example:

```text
Image 1 is the exact identity, palette, costume, proportions, outline weight,
and material reference. Preserve those properties; change only the requested
animation poses.
```

## Tool Invocation

Use a high-resolution generation canvas because the hosted image tool does not
produce native 16x16, 32x32, or 64x64 game textures directly.

Typical invocation arguments:

```json
{
  "prompt": "<complete prompt>",
  "out": "assets/sprites/generated/<slug>/raw/<action>.png",
  "quality": "medium",
  "size": "1024x1024",
  "images": ["assets/sprites/references/<reference>.png"]
}
```

Use `medium` for normal iteration. Use `high` only for a final difficult asset
after the contract and composition are proven. Generate one asset per call.

The documented plugin versions existing paths, but verify installed behavior.
Do not rely on versioning to protect assets; select unused paths and capture
the actual returned path, such as `<action>-v2.png`.

## Visual Quality Gate

Open or read the generated PNG and check:

- exact row and column count
- complete silhouettes with no cell-edge crossings
- stable identity, proportions, camera, and palette
- stable body scale and anchor
- ordered poses that communicate the requested motion
- seamless first-to-last transition for loops
- no grid lines, labels, UI, shadows, or background variation
- uniform `#FF00FF` background suitable for deterministic removal
- separate effect elements where the runtime expects separate layers

Reject and regenerate only the failed action. Tighten the prompt around the
observed defect. Do not hide generation defects by stretching individual frames
or assigning different scales to each pose.

## Pixel Processing

The generated PNG is source art, not the final runtime texture. Process it
deterministically before integration:

1. Split the image into the contracted equal grid.
2. Remove the solid magenta background and despill edge pixels.
3. Trim or align frames against one shared anchor without changing per-frame
   anatomical scale.
4. Downscale with nearest-neighbor sampling to the target runtime frame size.
5. Preserve integer pixel scaling and hard alpha edges.
6. Export a transparent sheet, individual frames when useful, and metadata that
   records grid, frame size, anchor, FPS, loop behavior, source path, and prompt.

Use an existing project processor when available. If no processor exists, stop
after accepted source generation unless the user approves adding deterministic
processing code. Do not use lossy JPEG intermediates.

## Delivery

Return the actual generated paths and distinguish raw, accepted, processed, and
integrated assets. Include frame dimensions, animation timing, loop behavior,
reference lineage, project files changed, validation results, and known visual
limitations.

Do not report success when only the raw image exists if the user requested a
processed asset bundle or an engine-ready scene. Validate requested engine
integration before claiming game-ready delivery; report unavailable checks.

## Plugin Limitations

`opencode-gpt-imagegen` is an unofficial plugin that reads OpenCode's ChatGPT
OAuth data and calls the Codex backend. It consumes subscription capacity, may
be affected by backend changes, and can occasionally return an orientation
different from the requested size. Always inspect actual dimensions and never
assume the requested path or orientation was honored.
