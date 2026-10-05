# Requirements

## Required and conditional dependencies

Planning and integration of supplied assets need no mandatory utility or model.
The documented generation route requires OpenCode, the
`opencode-gpt-imagegen` plugin, exposed `gpt_imagegen` tool schema, and the
user's eligible ChatGPT OAuth subscription. This route is OpenCode-only until
another harness is verified; installing the package does not expose a Codex tool.

Godot 4 is conditional for Godot project integration/engine checks
([Godot reference](godot.md)). Asset-only work needs no Godot binary.
Pixel processing uses an actually available utility appropriate to the requested
operation; Pillow, Aseprite, ImageMagick, or FFmpeg are not universal dependencies.

## Installation and checks

For OpenCode, follow [official installation](https://opencode.ai/docs/).
For the image plugin, review its
[upstream instructions](https://github.com/yuji-hatakeyama/opencode-gpt-imagegen) and the
selected harness configuration's approved version. Add the package/version to
OpenCode's existing `plugin` array only with configuration/dependency setup
authority; preserve unrelated entries. OpenCode fetches configured npm plugins,
so editing configuration can trigger a download. Follow
[OpenCode plugin setup](https://opencode.ai/docs/plugins/) and separately
authorized restart/login procedures. Confirm `gpt_imagegen` is exposed and
inspect its actual schema before generation. Never print authentication secrets.

For an approved Godot integration, install the version compatible with the
project using [official downloads](https://godotengine.org/download/).
macOS with existing Homebrew can use `brew install --cask godot` only if its
version matches project needs; verify `godot --version` when that executable
is on PATH. A version check is not an engine/rendering test.

Tool setup does not authorize generation/subscription usage, retries, or global
configuration changes. Keep the skill's batch preview/approval boundary.
