---
name: use-subagents
description: Discover native agent definitions with a bundled helper and select roles by responsibility and authority. Does not invoke or install agents.
---

# Use Subagents

Read [requirements](references/requirements.md) before selecting external tools or
running helpers. Dependency setup is separately authorized.

Read [five custom roles](references/core-roles.md) for responsibility and boundaries.
Select responsibility first and discover relevant skills separately; this is not
automatic delegation. Built-in runtime roles may already cover the task; inspect
the actual delegation interface as well as custom definitions.

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
A workflow may explicitly support supplying the full role instructions to an
independent generic agent when custom-role selection is absent. This does not
claim native role loading or grant delegation authority. Preserve role metadata
through supported controls; never substitute prose for native restrictions.

For harness inspection, load [the focused reference](references/harness-inspection.md) only when relevant.
