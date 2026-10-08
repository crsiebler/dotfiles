# Architecture and change map

Scope: source/configuration relationships sampled on 2026-10-07, at the dirty
snapshot described in the [overview](overview.md#inspection-scope-and-provenance).
This map routes changes to their owners; detailed procedures remain in the linked
guides and repository instructions.

## Shell configuration

[Makefile](../Makefile) defines `install` as the default goal. It first invokes
`install-zsh-extensions`, then copies the configured alias/Zsh files into the user
home, creates or synchronizes `.env`, sets the global Git excludes file, invokes
`install-opencode`, and installs `bin/ralph` with sudo. This is a mutating setup
path, not a verification command. AI-only targets do not traverse the shell path.

The source runtime flow is:

1. [zsh/.zshenv](../zsh/.zshenv) establishes shared locale, local executable PATH,
   and macOS Java discovery when JAVA_HOME is unset.
2. [zsh/.zshrc](../zsh/.zshrc) selects Powerlevel10k and the plugin list, loads
   Oh My Zsh (or completion fallback), then sources installed alias files.
3. The same interactive configuration initializes optional tool paths and Conda,
   sources Railway's environment file, and conditionally sources the personal
   `.env`. Source inspection does not prove these external files exist.

[scripts/install-zsh-extensions.py](../scripts/install-zsh-extensions.py) owns
`EXTENSIONS`: exact destinations, repository URLs, and readable entry points.
`main()` preflights all destinations, preserves existing valid copies, and clones
only missing extensions through a temporary sibling checkout before rename.
Changing the Zsh plugin list may also require changing that registry and the
[setup documentation](../README.md#custom-zsh-plugins-and-theme).

[scripts/sync-env.py](../scripts/sync-env.py) uses `extract_keys()` to compare the
example's key names with the existing personal file. `main()` appends missing blank
exports and export declarations for existing unexported keys, preserving values.
It does not load the file into the installer's environment. Tests belong in
`tests/test_sync_env.py`; inspect the template's names without exposing values.

Documentation discrepancy: AGENTS.md's environment-file style guidance says
JAVA_HOME defaults to `/usr/bin/java`, while the current `.zshenv` discovers it
through `/usr/libexec/java_home`. This map reports the source behavior and leaves
the existing guidance intact for a separately scoped correction.

## AI source distribution

| Owner | Transformation or consumer |
| --- | --- |
| [ai/AGENTS.md](../ai/AGENTS.md) | Installer copies unchanged bytes to both user-level instruction destinations |
| [ai/codex](../ai/codex/) and [ai/opencode](../ai/opencode/) configuration files | Managed JSON/TOML source bytes replace same-named installed files; changed files receive backups |
| [ai/codex/agents](../ai/codex/agents/) | Renderer copies native TOML to Codex and renders OpenCode Markdown |
| [ai/opencode/agents](../ai/opencode/agents/) | OpenCode-only Ralph, Ralph reviewer, and sprite artist copied unchanged |
| [ai/opencode/commands](../ai/opencode/commands/) | Native commands route to skills or own a specific workflow such as PR review |
| [Marketplace](../.agents/plugins/marketplace.json) and [plugin sources](../ai/plugins/) | Codex local plugin registration; OpenCode skill copies through the skills CLI |

In [scripts/install-ai.py](../scripts/install-ai.py), `main()` selects the target;
`local_plugins()` validates local marketplace ownership and skill names;
`check_agent_sources()` and `render_agents()` prepare native assets. The `validate`
branch parses sources and returns before installation, token checks, or native
plugin operations. Installation preflights destinations, calls `write_managed()`,
then installs/validates replacements before recording retirement ownership.

`install_plugins()` calls Codex marketplace registration and plugin add commands.
`install_skills()` calls `skills add ... --agent opencode --global --copy --yes`.
OpenCode copies are fingerprint-checked before retirement. These paths have
different activation mechanisms; a successful local parse is not activation.
Use [AI configuration](ai-configuration.md#installation-and-replacement-behavior)
for prerequisites, target roots, replacement semantics, and rollback.

[scripts/render-agents.py](../scripts/render-agents.py) owns `parse_source()` and
`render_opencode()`. The latter translates supported model metadata and maps
read-only roles to a deny-by-default read/glob/grep tool policy. That mapping is
not equivalent to the Codex runtime sandbox or MCP enforcement. Role additions
must remain representable in both harnesses; consult [agent authoring](agent-authoring.md).

[scripts/ai_retirement.py](../scripts/ai_retirement.py) owns `Skills` and `Plugins`
with prepare/apply/record stages, fingerprints, inventories, and archived copies.
[scripts/clean-install-backups.py](../scripts/clean-install-backups.py) separately
selects recognized backup names through `candidates()` and rejects unsafe roots.
Retirement and backup cleanup are different operations; preserve their inventories
and active assets. See [removal guidance](remove-old-ai-files.md).

## Requirements to delivery

[define-requirements.md](../ai/opencode/commands/define-requirements.md) loads
write-requirements; [plan-work.md](../ai/opencode/commands/plan-work.md) loads
prepare-implementation with the OpenCode JSON default. The planning skill selects
Markdown for trusted Codex context unless explicitly overridden. Its current
acceptance-coverage section maps source outcomes into bounded stories and assigns
integrated verification ownership before handoff. This guidance is present in the
uncommitted source snapshot, not verified as installed behavior.

The execution and persistence contracts are centralized in prepare-implementation:

| Responsibility | Canonical source / consumer |
| --- | --- |
| Story selection, authorization, checks, review budget, finalization | [story-execution.md](../ai/plugins/coding/skills/prepare-implementation/references/story-execution.md), consumed by both adapters |
| Review protocol and result schema | [story-review.md](../ai/plugins/coding/skills/prepare-implementation/references/story-review.md), supplied to native staged reviewers |
| Ralph executor | [ralph.md](../ai/opencode/agents/ralph.md), reads the installed shared contracts and writes the structured iteration outcome |
| Ralph scheduling and recovery state | [bin/ralph](../bin/ralph), `main()`, `execute()`, `validate_delivery()` and `status_report()` |
| Codex Goal adaptation | [Markdown plan reference](../ai/plugins/coding/skills/prepare-implementation/references/markdown-checklist.md), [story-reviewer.toml](../ai/codex/agents/story-reviewer.toml), [Goal guide](codex-goals.md) |
| Completed-run preservation | [archive_run.py](../ai/plugins/coding/skills/prepare-implementation/scripts/archive_run.py), under the [archive contract](../ai/plugins/coding/skills/prepare-implementation/references/completed-run-archive.md) |

Ralph's `execute()` persists `running`, launches `opencode run --agent ralph`,
then validates the iteration's identity, outcome, exact selected-story plan
transition, and committed delivery before continuing. Its state and lock live
in per-worktree Git metadata; outcome and stop files live at project root. Goal
uses native continuation rather than this supervisor. Neither a final message nor
a checkbox alone replaces committed delivery evidence. Recovery belongs to the
[Ralph runbook](ralph-recovery.md), not a fresh execution loop.

Task sources own completion; root `progress.md` owns append-only execution
evidence; root `memory.json` owns bounded operational knowledge; PRDs own approved
requirements. `archive_run.py` reads the PRD work-run manifest, checks committed
story-result evidence and runner state, then preserves declared artifacts under
its own lock and removal authorization. Mapping does not read or mutate run state.

## External boundaries and change impact

MCP definitions live under Codex `mcp_servers` and OpenCode `mcp`, with
harness-specific tool approval rules. The [connection guide](ai-configuration.md#connecting-applications)
owns authentication, trusted-project opt-in, and local mcp-suite integration.
The local PostgreSQL/Jev servers, model weights, credentials, and provider runtimes
are external dependencies; dotfiles installation does not build/provision them.

For a skill change, inspect its local references/scripts, plugin owner, matching
native command, and focused tests; keep the [dependency inventory](skill-dependencies.md)
aligned if prerequisites change. For shared delivery contracts, inspect both task
adapters and reviewer wrappers. For installer changes, inspect retirement,
backup cleanup, and renderer consumers together. The [testing map](testing.md)
identifies representative verification for these boundaries.
