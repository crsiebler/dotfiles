---
name: godot-sprite-forge
description: Generate pixel-art sprites, animation sheets, characters, enemies, props, projectiles, and effects with gpt_imagegen, then integrate approved assets into Godot 4. Use when a request mentions Godot sprites, sprite sheets, pixel art, AnimatedSprite2D, SpriteFrames, character animation, or game-ready 2D assets.
compatibility: OpenCode with opencode-gpt-imagegen and Godot 4
metadata:
  audience: game-developers
  engine: godot-4
---

# Godot Sprite Forge

Create original pixel-art assets through the `gpt_imagegen` tool, visually
validate the results, and integrate accepted sprites with the active Godot 4
project.

The image tool uses OpenCode's ChatGPT OAuth subscription. It produces one PNG
per call, supports reference images, and automatically versions an existing
output path instead of overwriting it.

## Preconditions

Before generation:

1. Verify `gpt_imagegen` is available. If it is absent, explain that
   `opencode-gpt-imagegen` must be loaded and OpenCode restarted. Do not replace
   the requested artwork with code-drawn placeholders.
2. Inspect `project.godot`, existing sprite directories, representative scenes,
   and animation code when a Godot project is present.
3. Run `godot --version` and follow the active project's version and patterns.
4. Keep all tool input and output paths relative to the current workspace.
5. Present the complete generation batch before invoking `gpt_imagegen`.

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

The plugin never overwrites an existing path. Capture and use the actual path
it returns, such as `<action>-v2.png`.

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

## Godot Integration

Follow the existing project structure. Otherwise use:

```text
assets/sprites/generated/<slug>/
  raw/
  processed/
  frames/
  previews/
  sprite-manifest.json
  <slug>_frames.tres
  <slug>_sprite.tscn
```

Godot rules:

- Never write into `.godot/`.
- Prefer `AnimatedSprite2D` with a `SpriteFrames` resource for ordinary 2D
  character animation.
- Use `AtlasTexture` regions for a processed sheet or individual textures when
  the project already follows that convention.
- Set nearest-neighbor filtering on the generated sprite node or resource. Do
  not change the project-wide filter unless requested.
- Preserve one origin and offset across compatible actions.
- Mark idle and locomotion loops as looping. Mark attack, cast, hurt, impact,
  and death as one-shot unless project behavior says otherwise.
- Match existing animation names and state-machine expectations.
- Prefer creating a reusable `<slug>_sprite.tscn`. Modify an existing gameplay
  scene only when the integration target is explicit and understood.
- Do not invent collision shapes from artwork unless requested and reviewed.

After importing or changing resources, validate from the project root with the
installed Godot executable. Use the least invasive project-supported command;
the baseline check is:

```bash
godot --headless --path "$PWD" --editor --quit
```

Treat parser errors, missing resources, invalid animation frames, and import
failures as blockers.

## Delivery

Return the actual generated paths and distinguish raw, accepted, processed, and
integrated assets. Include frame dimensions, animation timing, loop behavior,
reference lineage, Godot files changed, validation results, and known visual
limitations.

Do not report success when only the raw image exists if the user requested a
Godot-ready scene.

## Plugin Limitations

`opencode-gpt-imagegen` is an unofficial plugin that reads OpenCode's ChatGPT
OAuth data and calls the Codex backend. It consumes subscription capacity, may
be affected by backend changes, and can occasionally return an orientation
different from the requested size. Always inspect actual dimensions and never
assume the requested path or orientation was honored.
