---
name: create-gif
description: Assemble and inspect animated GIFs from supplied images or procedural graphics, with explicit timing, palette, resizing, and background choices.
---

# Create GIF

Modified 2026-09-17 from Anthropic slack-gif-creator (Apache-2.0); see
[provenance](references/provenance.md) and [license](LICENSE.txt).

Identify the source frames or procedural motion, intended dimensions/background,
loop behavior, and destination. Supplied assets and procedural graphics work without
an AI provider. Do not require Slack or assume its limits apply to other destinations.

Read [authoring and JSON/CLI contracts](references/authoring.md) before assembly.
Resolve `scripts/create_gif.py` relative to this loaded skill. Check
[requirements](references/requirements.md), then work entirely in the active project:

```sh
python /loaded/create-gif/scripts/create_gif.py check
python /loaded/create-gif/scripts/create_gif.py --project /project assemble request.json output.gif
python /loaded/create-gif/scripts/create_gif.py --project /project inspect output.gif
```

Choose nearest sampling for pixel art and lanczos for continuous-tone artwork.
Preserve aspect ratio, decide between a solid background and binary transparency,
and set explicit durations. Reduction holds selected frames longer to preserve
time; it can change motion quality, so review the result rather than merely its size.

Follow [validation](references/validation.md): compare actual decoded timing and
metadata, inspect representative frames and loop continuity, and report which visual
checks were possible. For Slack requests only, read [destination guidance](references/slack.md).
Deliver the artifact with actual dimensions, byte size, timing, and remaining limits.
No provider calls, package installation, or automatic retry spending are performed.
