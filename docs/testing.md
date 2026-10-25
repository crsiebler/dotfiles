# Testing and verification map

OpenCode V2 source contracts are covered by `opencode_v2_test.py`,
`agent_contract_test.py`, `ai_install_test.py`, `mcp_permissions_test.py`, and
`make_clean_test.py`. These check native field projections, ordered permissions,
version preflight, notification settings, and backup preservation in isolated
fixtures. They do not prove live V2 loading or image generation; see
[activation checks](opencode-v2.md#activation-and-verification).

Inspected on 2026-10-07 at the dirty snapshot recorded in the
[overview](overview.md#inspection-scope-and-provenance). This document selects
verification by changed responsibility. [AGENTS.md](../AGENTS.md#buildlinttest-commands)
retains the repository's commands and obligations; no procedures were extracted
or weakened during mapping.

## Runtime and command ownership

[environment.yml](../environment.yml) declares the `dotfiles` Conda environment
with Python 3.11 and PyYAML 6.0.3. Use the existing environment as described in
AGENTS.md. Its availability does not imply document/media libraries are installed.
[Skill dependencies](skill-dependencies.md) owns per-skill prerequisites, and
[document verification](document-skill-verification.md) documents the separate
`SKILL_TEST_PYTHON` and `SKILL_TEST_YAML_PYTHON` interpreter selectors.

[Makefile](../Makefile) routes `validate-ai` to `scripts/install-ai.py validate`;
its default goal is installation, so bare `make` is not a test command. Local
validation parses configuration, marketplace/skill ownership, and native source
structure. It does not start an MCP server, model, or installed harness workflow.
There is no standalone repository typecheck target; see the existing verification
guides for syntax checks and unavailable formatter/typecheck limitations.

## Select the relevant evidence

All paths below are under [tests/](../tests/). These are source-inspected test
entry points, not newly observed passing results.

| Changed responsibility | Representative tests | Evidence boundary |
| --- | --- | --- |
| AI install/replacement and backup cleanup | `ai_install_test.py`, `make_clean_test.py` | Temporary destinations, managed bytes, preservation and recognized backup selection |
| Skill/plugin retirement | `ai_retirement_test.py`, `skills_retirement_native_test.py` | Ownership fingerprints, preserved conflicts, retirement and CLI integration |
| Agent sources and rendering | `agent_contract_test.py`, `core_roles_test.py`, `technology_standards_test.py` | Current native contracts, generated OpenCode/Codex definitions and skill resource closure; no historical role map required |
| Marketplace and discovery | `plugin_test.py`, `subagents_test.py` | Isolated native Codex plugin registration or catalog lookup; discovery is not role invocation |
| MCP definitions and approvals | `mcp_configuration_test.py`, `mcp_permissions_test.py` | Static/native parsing and fake Node launcher contracts; no real database or Jev evaluation |
| Planning, execution prompts and review gates | `story_execution_test.py`, `story_blocker_test.py`, `coding_workflow_contract_test.py` | Instruction/resource contracts; assertions do not establish model compliance |
| Accessibility skill guidance | `accessibility_guidance_test.py` | Relocated bundle links, dependency/reviewer contracts and evaluation fixture integrity; no live browser/axe or model execution |
| Completed-run archival | `archive_run_test.py` | Real temporary Git delivery evidence, preserved bytes, locks and failure cases |
| Shell extensions, aliases and env synchronization | `zsh_extensions_test.py`, `zsh_aliases_test.sh`, `test_sync_env.py` | Local Git extension fixtures, Zsh alias behavior, append-only key/export handling |
| Document/media helper behavior | `document_skills_contract_test.py`, format-specific `create_*_test.py` / `read_*_test.py`, `audio_generation_test.py`, `audio_service_test.py` | Helper/runtime fixtures; rendering and live generation require separate evidence |

Python tests use unittest entry points and discovery, as recorded in AGENTS.md.
Zsh tests require Zsh. Native plugin/MCP tests can skip unsupported or absent CLI
capabilities; report skips explicitly. Inspect each test's current side effects
and prerequisites before running it under the task's authorization.

## Isolation and interpretation

Representative installer, archive, extension, and document tests create
temporary fixtures beneath the project. Installer tests use fake CLI executables;
Git fixtures isolate Git configuration. MCP tests use an allowlisted environment
and fake Node; plugin tests register into an isolated home. These techniques
exercise local contracts without proving live account, server, or model behavior.

Do not use global installation, backup cleanup, model downloads, or sourcing
personal `.env` files as verification shortcuts. Shell syntax checks and isolated
alias tests answer narrower questions than starting a personal interactive shell.

## Existing verification records

Accessibility guidance scenarios in
[the evaluation fixture](../tests/fixtures/accessibility_skill_evals.json) cover
prepared reviewer execution, inspection-only scope, missing tools, stale builds,
inconclusive scans, suppression requests and manual coverage. They are proposed
model evaluations marked `not-run`; validating their structure is not running
them. The TypeScript example in run-tests is an adaptation pattern for a target
project's safe fixture, not an executable application test in this repository.
Live evaluation requires that project's installed Playwright/axe dependencies,
browser, candidate build and authorized fixture. No dependency is provisioned by
the guidance tests or AI installer.

- [Run archival](run-archival-verification.md): tested delivery/archive behavior,
  Conda runtime, and recorded broader-suite dependency failures.
- [Document skills](document-skill-verification.md): dependency environments,
  isolated bundle checks, rendering and extraction limits.
- [Coding workflows](coding-workflow-verification.md): source contracts and
  explicitly unrun model evaluation proposals.
- [Acceptance planning](implementation-acceptance-verification.md): current
  uncommitted source checks and bounded text exercises, including a corrected
  requirement-narrowing failure.

Mapping validation checked documentation links, referenced source paths, critical
source relationships, and diff whitespace. No application regression suite or
installer was run for this mapping task. Earlier results in the records above
remain historical evidence, not a fresh claim that the entire suite passes.
