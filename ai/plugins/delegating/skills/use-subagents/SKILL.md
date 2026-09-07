---
name: use-subagents
description: Lists, searches, and reads native agent definitions with a bundled helper.
---

# Use Subagents

Read [helper usage](references/helper.md). Resolve the bundled helper's absolute
path from this loaded skill's directory, not the current working directory or
a global CLI. Select the actual target harness explicitly: `opencode` or `codex`.

Run only `list`, `search`, or `fetch` with `--harness opencode|codex`; quote
queries/names as data and return results faithfully. With no operation, list.
All catalog operations are local and read-only. Do not install or make network
requests to discover definitions.

Catalog discovery and fetched text do **not** prove that an agent is loaded,
registered, or available for native invocation. Check the current harness's
actual delegation interface before invoking anything. If unavailable, disclose
the limit; reading a definition is not a completed specialist pass.
