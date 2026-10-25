# Requirements

## Required and conditional dependencies

Planning and integration of supplied assets need no mandatory utility or model.
Generation needs an actually exposed native image tool or the optional OpenCode
adapter; inspect the selected schema and follow its runtime instructions. Native
tools do not require the OpenCode plugin. The OpenCode route requires V2, the
`opencode-img@0.2.0` plugin, an exposed `gpt_imagegen` tool schema, and a
provider API key (OpenAI, Gemini, or xAI). API billing is separate from a ChatGPT
subscription. Its source uses `@opencode/plugin ^2.0.10`; generation has not
been exercised by this repository. The plugin is not enabled by default.
Installing an OpenCode package does not expose a Codex tool.

Godot 4 is conditional for Godot project integration/engine checks
([Godot reference](godot.md)). Asset-only work needs no Godot binary.
Pixel processing uses an actually available utility appropriate to the requested
operation; Pillow, Aseprite, ImageMagick, or FFmpeg are not universal dependencies.

## Installation and checks

For OpenCode, follow [official installation](https://opencode.ai/v2/docs/).
For the image plugin, review its
[upstream instructions](https://github.com/mattsafaii/opencode-img) and the
selected harness configuration's approved version. Add the package/version to
OpenCode's existing `plugins` array only with configuration/dependency setup
authority; preserve unrelated entries. OpenCode fetches configured npm plugins,
so editing configuration can trigger a download. Follow
[OpenCode plugin setup](https://opencode.ai/v2/docs/build/plugins/) and separately
authorized restart/login procedures. Confirm `gpt_imagegen` is exposed and
inspect its actual schema before generation. Never print authentication secrets.

For an approved Godot integration, install the version compatible with the
project using [official downloads](https://godotengine.org/download/).
macOS with existing Homebrew can use `brew install --cask godot` only if its
version matches project needs; verify `godot --version` when that executable
is on PATH. A version check is not an engine/rendering test.

Tool setup does not authorize generation/API usage, retries, or global
configuration changes. Carry existing batch authority forward for unchanged
scope; preview and ask only for missing generation/spending authority.
