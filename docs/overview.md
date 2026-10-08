# Repository overview

This repository owns Zsh configuration and the source configuration, portable
skills, native roles, and execution tooling for Codex and OpenCode. It is a
configuration distribution repository, not an application with a single runtime.
The [Makefile](../Makefile) separates source validation, shell installation,
AI installation, and backup cleanup.

## Find the relevant code

| Task or subject | Documentation owner | Source entry points |
| --- | --- | --- |
| Understand configuration flows and change impact | [Architecture map](architecture.md) | [Makefile](../Makefile), [AI installer](../scripts/install-ai.py), [Ralph](../bin/ralph) |
| Choose verification for a change | [Testing map](testing.md) | [Tests](../tests/), [Environment manifest](../environment.yml) |
| Change shell behavior or custom extensions | [README shell setup](../README.md#custom-zsh-plugins-and-theme), [shell flow](architecture.md#shell-configuration) | [Zsh configuration](../zsh/.zshrc), [shared environment](../zsh/.zshenv), [aliases](../aliases/), [extension registry](../scripts/install-zsh-extensions.py) |
| Install AI assets or change MCP connections | [AI configuration guide](ai-configuration.md) | [Installer](../scripts/install-ai.py), [Codex config](../ai/codex/config.toml), [OpenCode config](../ai/opencode/opencode.json) |
| Add or revise a native role | [Agent authoring](agent-authoring.md) | [Canonical TOML roles](../ai/codex/agents/), [renderer](../scripts/render-agents.py), [OpenCode-only roles](../ai/opencode/agents/) |
| Add or revise a portable skill | [Skill dependencies](skill-dependencies.md), [coding workflow design](coding-workflow-design.md) | [Plugin marketplace](../.agents/plugins/marketplace.json), [skill sources](../ai/plugins/), [create-skill](../ai/plugins/coding/skills/create-skill/SKILL.md) |
| Trace requirements, planning, and delivery | [Workflow flow](architecture.md#requirements-to-delivery), [Codex Goal guide](codex-goals.md) | [write-requirements](../ai/plugins/coding/skills/write-requirements/SKILL.md), [prepare-implementation](../ai/plugins/coding/skills/prepare-implementation/SKILL.md) |
| Diagnose Ralph or adjust its supervisor | [Ralph recovery](ralph-recovery.md) | [Runner](../bin/ralph), [native executor](../ai/opencode/agents/ralph.md), [control contract](../ai/plugins/coding/skills/prepare-implementation/references/ralph-control.md) |
| Retire installed assets or remove backups | [Removal and migration guide](remove-old-ai-files.md), [README cleanup](../README.md#removing-backup-files) | [Retirement logic](../scripts/ai_retirement.py), [backup cleanup](../scripts/clean-install-backups.py) |
| Work on media/document helpers or local models | [Document verification](document-skill-verification.md), [Bonsai setup](local-bonsai.md), [audio setup](../ai/plugins/producing/skills/create-audio/references/local-audio.md) | [Producing](../ai/plugins/producing/skills/), [researching](../ai/plugins/researching/skills/), [model shortcut](../aliases/.aliases) |

## Source and installed state

Edit canonical project sources, then follow the separately authorized installation
workflow. Installed copies, native plugin caches, and rendered OpenCode roles are
consumers of these sources. A source edit does not establish installed discovery
or runtime behavior. Root [AGENTS.md](../AGENTS.md) governs this repository;
[ai/AGENTS.md](../ai/AGENTS.md) is the separately installed personal policy.

## Inspection scope and provenance

Mapped on 2026-10-07 from working-tree source over revision
`142e2fa9b39ad6a91a6f1bb874a351e81bd60034`. The checkout was already dirty:
AGENTS.md had Conda guidance changes; prepare-implementation and its Markdown/Ralph
references had acceptance-coverage changes; the planning scenario fixture was
modified; implementation-acceptance-verification.md was untracked. This map includes
those changes; the revision alone does not reproduce the mapped state.

Inspection traced shell startup/install, AI installation/rendering/retirement,
requirements-to-delivery, and representative verification boundaries. Individual
specialist role bodies and every media/document helper were not exhaustively
reviewed. Existing subject guides retain their own verification dates and limits.
No credentials, personal environment files, legacy execution journals, external
services, or installed plugin caches were inspected for this map. No application
tests, installers, models, or services were run as part of mapping.
