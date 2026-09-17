# Provenance

Adapted from Anthropic [skills](https://github.com/anthropics/skills),
`skills/slack-gif-creator`, commit `34040c9c568585f6929bedeaad110ad08f079624`.
Only this Apache-licensed source bundle supplied GIF implementation material.
[LICENSE.txt](../LICENSE.txt) is retained unchanged; no separate NOTICE file exists
in the selected upstream bundle.

Modified 2026-09-17: SKILL.md is rewritten for portable non-Slack use;
core/gif_builder.py is adapted under scripts/gif_builder.py, replacing NumPy/ImageIO
with Pillow and preserving elapsed time during reduction/deduplication;
core/frame_composer.py is adapted as a focused Pillow procedural helper.
Each modified source carries a change notice. GIF inspection replaces upstream
validators that inferred elapsed time from frame count/FPS. Unneeded easing and
text/emoji helpers are omitted; the initial procedural operation uses an explicit
periodic orbit and needs no fonts. CLI/path-boundary code and references are new.

Directory changes, removed dependencies, shared-palette binary transparency,
aspect-preserving fitting, fresh output publication, and decoded validation are
intentional adaptations. No upstream document skill code or assets were consulted.
