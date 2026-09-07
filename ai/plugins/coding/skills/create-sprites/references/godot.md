# Godot Integration

Load only for Godot requests or relevant Godot project context. Common generation,
approval, prompt, quality, and processing rules live in the parent `create-sprites`
skill. Asset-only work does not require a Godot binary.

## Project Inspection

Inspect `project.godot`, existing sprite directories, representative scenes,
and animation code when a Godot project is present. Confirm `project.godot`
exists before changing Godot resources or scenes; otherwise deliver only an
asset bundle and state that no project integration was performed.
For integration, run `godot --version` and follow the active project's version
and patterns. Missing Godot blocks import validation, not asset-only work.

## Resources and Scenes

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

## Validation and Delivery

After importing or changing resources, validate from the project root with the
installed Godot executable. Use the least invasive project-supported command;
the baseline check is:

```bash
godot --headless --path "$PWD" --editor --quit
```

Treat parser errors, missing resources, invalid animation frames, and import
failures as blockers. Include Godot files changed and actual validation results
in delivery. Do not report success when only the raw image exists if the user
requested a Godot-ready scene. `--plan-only` allows no imports or file changes.
