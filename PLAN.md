# Implementation plan: Claude Code support

## Objective and scope baseline

- Revision: `claude-support-v1`, prepared 2026-10-20 from commit
  `c6c48a64e83697ddf079578a54ad5594bc525457` and a clean initial worktree.
- User brief: research Claude Code compatibility for the skills marketplace,
  configurations, MCP servers, scripts and tools; generate an implementation plan.
- Evidence and design rationale:
  [Claude Code assessment](docs/claude-code-support-assessment.md).
- Current authority: research and planning only. All implementation stories below
  are proposed; no execution, installation, configuration changes, model spending,
  commits, cleanup or external writes are authorized by this document.
- Working branch: currently `main`; implementation branch/worktree preparation and
  delivery authority remain for a later execution request. No branch was created.
- Baseline target: local Claude Code on this macOS development machine. Keep
  portable source structure, but do not claim Windows/cloud-client verification.
- Outcome: the five Craft plugins load all 31 shared skills in Claude; optional
  personal integration preserves existing ownership and approval contracts.
- Non-goals: port Ralph to Claude, route Claude to GPT/Bonsai, replace helper
  runtimes, provision dependencies/models, add AWS/Elastic servers, enable
  experimental teams by default, or migrate installed caches automatically.
- Authorization-policy gap: the proposed MCP/staged-review guard adds
  authorization logic, which current project policy prohibits modifying.
  Explicitly reconcile that boundary before those stories execute. Other source
  packaging work is independent; do not weaken permission parity to avoid it.
- Native evidence gap: `claude` is unavailable on this session's PATH. A selected
  installed release and separately authorized native evaluation are required.

The recommended design keeps shared skill sources, adds Claude manifests and an
isolated installer adapter, and renders native agents from canonical TOML. It
preserves existing `make install-ai`/`all` behavior; Claude is an explicit target.
Full personal integration is a draft pending the policy/native gates above.

## Dependencies and acceptance ownership

| Story | Priority | Depends on | Integrated outcome owned |
| --- | ---: | --- | --- |
| CC-01 | 1 | none | Supported-version and ownership contract |
| CC-02 | 1 | CC-01 | Five-plugin marketplace and 31-skill packaging |
| CC-03 | 1 | CC-01 | Policy/settings preservation |
| CC-04 | 1 | CC-01 | MCP transport and permission parity |
| CC-05 | 2 | CC-01 | Native role rendering and static discovery |
| CC-06 | 2 | CC-02, CC-05 | Skill routing and command adaptation |
| CC-07 | 2 | CC-02, CC-03, CC-04, CC-05, CC-06 | Safe repeatable personal installation/rollback |
| CC-08 | 3 | CC-04, CC-05, CC-06, CC-07 | Qualified staged review/team execution |
| CC-09 | 2 | CC-07 | Base-support regression and release evidence |
| CC-10 | 3 | CC-08, CC-09 | Workflow release and final support documentation |

CC-02 can deliver marketplace-only compatibility before personal integration.
CC-09 owns the base-support release; CC-10 alone owns the full workflow claim.
CC-08 may be deferred explicitly, in which case CC-10/full workflow support stays
pending. Optional image/notifier parity is separately scoped below.
The graph permits independent work but does not authorize delegation or worktrees.

## Ordered stories

### CC-01 — Establish Claude support and ownership contracts

- [ ] Story complete
- Priority: 1
- Depends on: none
- Phase / requirements: all components in the user's assessment request;
  assessment sections on architecture, policy and evidence limits.
- User story: As the repository owner, I want a bounded Claude integration so
  adopting it preserves my existing harnesses and safety rules.
- Relevant paths: `docs/claude-code-support-assessment.md`,
  `docs/ai-configuration.md`, `docs/agent-authoring.md`, `AGENTS.md`.
- Recommended expertise: `cli-developer` for native CLI behavior;
  `security-auditor` for read-only assessment of permission equivalence.

Acceptance criteria:

- [ ] Record the actual supported Claude version, native CLI help/schema evidence
  and isolated-test environment; do not infer installation from documentation.
- [ ] Confirm five shared plugins, explicit `install-claude`, unchanged legacy
  `all`/shell-install scope, and independently opted-in personal integrations.
- [ ] Decide and document Claude settings ownership/reconciliation and backup
  scope; identify every native state file affected by CLI registration.
- [ ] Resolve authorization-control implementation scope before CC-04/CC-08;
  missing authority blocks those stories, not unrelated marketplace work.
- [ ] Establish capability checks for instruction loading, plugin validation,
  guard failure behavior and reviewer continuation. Documentation currently
  places `onFailure: block` at v2.1.295; verify rather than assume that baseline.
- [ ] Record unsupported/deferred features and acceptance owners without inventing
  runtime evidence or changing existing Codex/OpenCode policies.

### CC-02 — Package the five plugins for Claude

- [ ] Story complete
- Priority: 1
- Depends on: CC-01
- Phase / requirements: compatible skills marketplace; all 31 skills retain
  scripts, references, dependencies and explicit capability limitations.
- User story: As a Claude user, I want to install Craft from this checkout and
  invoke its skills without a separate fork of their content.
- Relevant paths: new `.claude-plugin/marketplace.json`,
  `ai/plugins/*/.claude-plugin/plugin.json`, `tests/plugin_test.py`, new
  `tests/claude_plugin_test.py`; retain `.agents/plugins/marketplace.json`.
- Recommended expertise: `tooling-engineer`.

Acceptance criteria:

- [ ] Both marketplace indexes name the same five bundles and shared source
  paths; Claude entries have correct relative sources and owner metadata.
- [ ] Manifests validate on the selected native release. Duplicate names,
  traversal, missing resources and mismatched plugin identities fail validation.
- [ ] An isolated local install exposes all 31 skill identities exactly once;
  representative namespaced invocations resolve expected content.
- [ ] A copied/cached-layout fixture resolves bundled references and helpers
  without reaching into the original checkout or writing plugin directories.
- [ ] Repeated registration/install has defined behavior and preserves unrelated
  plugins. Marketplace-only installation writes no personal policy or MCP config.
- [ ] Existing Codex plugin contract tests retain their assertions; record native
  skips separately. Verify resource hashes where shared bytes should be identical.

### CC-03 — Add personal policy and bounded settings reconciliation

- [ ] Story complete
- Priority: 1
- Depends on: CC-01
- Phase / requirements: configurations and preservation of project guidance.
- User story: As the repository owner, I want Claude to load the same personal
  and project instructions while retaining my unrelated settings.
- Relevant paths: new `ai/claude/settings.json`, proposed root `CLAUDE.md`,
  `ai/AGENTS.md`, new settings adapter/tests under `scripts/` and `tests/`.
- Recommended expertise: `cli-developer`.

Acceptance criteria:

- [ ] User `CLAUDE.md` receives exact `ai/AGENTS.md` bytes; root `CLAUDE.md` imports
  `AGENTS.md` without duplicating policy. Verify nested instruction behavior.
- [ ] Owned settings reconciliation preserves unrelated entries, existing
  restrictions, third-party hooks and CLI-managed plugin state; conflicts stop
  with safe diagnostics and no partial overwrite.
- [ ] Root validation rejects unsafe/relative/symlinked destinations and respects
  supported absolute configuration overrides. Fixtures cover paths with spaces.
- [ ] Preserve user model choices; no GPT/Bonsai translation or global subagent
  model pin. Document the effective shell/file/network permission boundaries.
- [ ] Backup/restore fixtures preserve previous bytes and permissions without
  exposing credential values. Existing harness replacement behavior is unchanged.

### CC-04 — Translate MCP configuration and approval behavior

- [ ] Story complete
- Priority: 1
- Depends on: CC-01
- Phase / requirements: all 12 configured MCP connections; existing enablement,
  exact read exceptions, unknown-tool behavior and credential handling.
- User story: As the repository owner, I want Claude MCP connections to retain
  their existing scopes and approval requirements.
- Relevant paths: new `ai/claude/mcp/`, approved guard implementation if permitted,
  `tests/mcp_configuration_test.py`, `tests/mcp_permissions_test.py`, new
  `tests/claude_mcp_test.py`.
- Recommended expertise: `mcp-developer`; `security-auditor` for bounded assessment.

Acceptance criteria:

- [ ] Only GitHub, Exa and Context7 are registered globally by the explicit
  personal-install operation. All nine optional definitions remain unregistered
  templates until trusted-project activation is separately authorized.
- [ ] Retain all names, endpoints, toolsets, local Node entry points, required
  environment references and timeouts with verified Claude-native semantics.
- [ ] Exact approved reads run without approval unless a stricter existing policy
  applies; mixed-server writes/new tools ask; PostgreSQL arbitrary SQL always
  asks; unknown Exa/Context7 tools are blocked; always-ask servers remain so.
- [ ] Test allow/ask/deny precedence with independent expected outcomes. Do not
  copy OpenCode's last-match evaluator or infer expectations from generated data.
- [ ] If authorized guards are needed, failures/missing files/malformed input/
  timeouts block affected calls; guards cannot override stricter settings. Prove
  behavior through a fake local MCP server before live connection tests.
- [ ] Fake Node fixtures prove arguments/env forwarding without starting real
  PostgreSQL/Jev, Docker, browser downloads or evaluations. Missing credentials
  produce safe errors; no secret is written or logged.
- [ ] User/local registration preserves unrelated native state. Optional
  templates stay inactive in interactive and noninteractive sessions.
- [ ] Real authentication/connectivity is a separately authorized smoke check;
  static success is never reported as live server compatibility.

### CC-05 — Render Claude agents and extend discovery

- [ ] Story complete
- Priority: 2
- Depends on: CC-01
- Phase / requirements: canonical agent collection and bundled discovery tool.
- User story: As a Claude user, I want the existing specialists available with
  their contracts and restrictions intact.
- Relevant paths: `scripts/render-agents.py`, `ai/codex/agents/*.toml`,
  `ai/plugins/delegating/skills/use-subagents/`, `tests/agent_contract_test.py`,
  `tests/subagents_test.py`.
- Recommended expertise: `python-pro`.

Acceptance criteria:

- [ ] Claude target renders 128 roles from canonical TOML with faithful parsed
  bodies, valid metadata and inherited model choice; audit harness-specific
  references instead of blindly substituting tool names.
- [ ] Unknown fields, unsupported future model/provider/effort/sandbox fields,
  invalid names, collisions and unsafe output paths fail explicitly.
- [ ] Eight restricted roles have explicit minimal native tool allowlists;
  Write/Edit/Bash/MCP/delegation are unavailable in the baseline rendering.
  Explain lost shell capability; do not claim an equivalent Codex sandbox.
- [ ] `story-reviewer` does not satisfy staged delivery until CC-08 qualifies
  its evidence access. OpenCode's three native-only roles stay OpenCode-only.
- [ ] Discovery supports explicit `--harness claude`, root override, project/user
  scopes, duplicate errors and exact-byte fetch; output remains static evidence.
- [ ] Existing Codex bytes and OpenCode rendering/restriction tests still pass.

### CC-06 — Adapt skill routing and command entry points

- [ ] Story complete
- Priority: 2
- Depends on: CC-02, CC-05
- Phase / requirements: reusable workflows and existing command/tool interfaces.
- User story: As a Claude user, I want entry points that select the correct shared
  skills without silently starting another harness or unsupported capability.
- Relevant paths: `ai/plugins/coding/skills/prepare-implementation/`,
  `ai/plugins/delegating/skills/use-subagents/`, new `ai/claude/commands/`,
  `ai/opencode/commands/review-pr.md`, `tests/coding_workflow_contract_test.py`.
- Recommended expertise: `prompt-engineer`, `cli-developer`.

Acceptance criteria:

- [ ] Trusted Claude context defaults planning to Markdown `PLAN.md`; explicit
  user formats win. Planning creates no execution journal, memory or runner state.
- [ ] Requirements/plan/ship/find-agents shortcuts load the intended shared skills;
  arguments are handled as data and explicit approvals persist within scope.
- [ ] Any review-pr adapter derives its complete review contract from the existing
  canonical command; tests guard schema and exact-payload posting approval.
  Its Claude context-gathering syntax is independently verified.
- [ ] All 31 skills have a documented supported/conditional behavior; sprite
  generation reports the missing Claude backend, recovery remains OpenCode,
  and advanced team execution remains gated until CC-08.
- [ ] Verify representative document read/create, audio dry-run and skill-helper
  calls from installed locations with available dependencies; report missing
  renderers/models/packages rather than installing them automatically.
- [ ] No duplicate legacy skill copies, implicit upstream Claude eval downloads,
  broad tool preapprovals or unexplained workflow schema renames are introduced.

### CC-07 — Integrate explicit installation, preview and rollback

- [ ] Story complete
- Priority: 2
- Depends on: CC-02, CC-03, CC-04, CC-05, CC-06
- Phase / requirements: installation scripts, backups, retirement and repeatability.
- User story: As the repository owner, I want an explicit Claude installation
  with inspectable changes and a reliable rollback path.
- Relevant paths: new `scripts/install-claude.py`, `scripts/install-ai.py`,
  `Makefile`, `scripts/ai_retirement.py`, `scripts/clean-install-backups.py`,
  `tests/ai_install_test.py`, `tests/ai_retirement_test.py`,
  `tests/make_clean_test.py`, new Claude installer fixtures.
- Recommended expertise: `python-pro`, `cli-developer`.

Acceptance criteria:

- [ ] `make install-claude`/explicit Claude target use native plugin registration
  with scoped settings/agents/MCP installation and no dependency bootstrap.
  Missing Claude blocks clearly; a missing `skills` CLI does not block Claude-only.
- [ ] Read-only preview names owned destination changes and conflicts without
  contacting servers or invoking mutating native commands.
- [ ] Preflight all destinations before writes; back up changed owned state and
  native CLI side effects; report partial failures conservatively.
- [ ] Repeat install is idempotent and verifies installed payloads and effective
  state. It does not adopt unrelated/customized assets as managed ownership.
- [ ] Claude-only operations never retire shared `~/.agents/skills` trees or
  modify Codex/OpenCode roots. Preserve current `all` and shell-install behavior.
- [ ] Rollback restores owned state without deleting new unrelated native state.
  Any removal needs exact ownership, preservation and existing scoped authority.
- [ ] Cleanup recognizes only approved installer backups, with preview coverage;
  native caches, credentials, sessions and unrecognized backups survive.
- [ ] Isolated-home fixtures cover overrides, conflicts, unavailable CLI, changed
  native output, symlinks, repeat install and interrupted operations.

### CC-08 — Qualify staged review and team execution

- [ ] Story complete
- Priority: 3
- Depends on: CC-04, CC-05, CC-06, CC-07
- Phase / requirements: optional full workflow compatibility; preserve current
  review, concurrency, delivery and archive invariants.
- User story: As the repository owner, I want Claude delivery workflows to meet
  the same evidence gates before they are advertised as supported.
- Relevant paths: `ai/plugins/coding/skills/run-agent-team/references/`,
  `ai/codex/agents/story-reviewer.toml`, approved Claude reviewer adapter,
  `tests/story_execution_test.py`, `tests/story_blocker_test.py`,
  `tests/agent_team_contract_test.py`, `tests/runtime_selection_test.py`.
- Recommended expertise: `tooling-engineer`; `story-reviewer` for later authorized
  native staged review, only after callable-role preflight succeeds.

Acceptance criteria:

- [ ] Resolve the authorization-control boundary before adding staged-Git
  enforcement. No broad Bash access is used to simulate a read-only reviewer.
- [ ] Demonstrate exact native reviewer selection, permitted staged evidence,
  required JSON schema and same-session targeted continuation on the selected
  release. Inspect actual native tool schemas; do not assume old resume APIs.
- [ ] Preserve expanded-initial/targeted budgets, blocked verdicts, history and
  candidate freeze. New agents, compaction or continuation cannot reset passes.
- [ ] Demonstrate dependency-ready workers using explicit authorized worktrees,
  clean committed bases and owned paths, with one lead controlling Git/trackers.
  Verify cwd/isolation rather than trusting role names.
- [ ] Ordinary subagents suffice where supported; experimental teams remain off
  by default. Respect supported model inheritance and explicit user limits.
- [ ] A disposable, separately authorized run demonstrates worker handoff,
  bounded initial/targeted review, delivery evidence and existing archival format.
  No production data, remote writes or real repository cleanup is needed.
- [ ] If required native controls cannot satisfy the contract, keep this story
  pending and publish the exact limitation; do not weaken gates or port Ralph.

### CC-09 — Verify and document base Claude support

- [ ] Story complete
- Priority: 2
- Depends on: CC-07
- Phase / requirements: integrated marketplace/configuration/MCP/tool support;
  regression protection for existing harnesses.
- User story: As a user, I want support claims backed by observed installation
  and behavior, with clear capability limits.
- Relevant paths: `README.md`, `AGENTS.md`, `docs/ai-configuration.md`,
  `docs/agent-authoring.md`, `docs/skill-dependencies.md`, `docs/testing.md`,
  `docs/remove-old-ai-files.md`, new Claude verification record.
- Recommended expertise: `qa-expert`, `technical-writer`.

Acceptance criteria:

- [ ] From an isolated configuration root, verify five installed plugins, 31
  skill identities, policy loading, generated agents, commands and bundled
  resource paths with recorded Claude version and exact observed outcomes.
- [ ] Verify safe MCP read/ask/deny cases against fake servers and optional
  nonactivation; distinguish separately authorized real connection results.
- [ ] Relevant existing and new tests pass; record native skips, missing packages
  and historical failures without weakening assertions or claiming full success.
- [ ] Document setup, explicit activation, ownership, scopes, rollback, version
  support, source-versus-installed distinctions and known feature limitations.
- [ ] Optional sprite generation, notifier parity and advanced delivery are not
  advertised as complete merely because skills are discoverable.

### CC-10 — Publish workflow qualification and close the support matrix

- [ ] Story complete
- Priority: 3
- Depends on: CC-08, CC-09
- Phase / requirements: complete integrated workflow acceptance and final limits.
- User story: As the repository owner, I want to know exactly which Claude
  workflows have been demonstrated and which remain deferred.
- Relevant paths: `docs/runtime-selection.md`, `docs/agent-team-verification.md`,
  `docs/run-archival-verification.md`, Claude verification record and setup guide.
- Recommended expertise: `qa-expert`, `technical-writer`.

Acceptance criteria:

- [ ] Tie native execution/reviewer evidence to tested source and installed
  versions; report both successful flows and exercised blocked paths.
- [ ] Verify planning → implementation → bounded review → authorized delivery →
  evidence-preserving archival in the disposable qualification project.
- [ ] Preserve `CodexGoalMarkdown` serialized compatibility, Ralph's unchanged
  contracts, journal/memory limits and all existing historical evidence.
- [ ] Update the support matrix without overstating model quality, immutable
  security boundaries, runtime isolation or support on untested platforms.

## Verification plan

These are future implementation checks, not commands executed during planning.
Use the existing Conda `dotfiles` environment. There is no repository typecheck
target; use local Python syntax/source validation and focused contract tests.

Existing commands selected by affected responsibility:

```sh
make validate-ai
python -m unittest discover -s tests -p 'agent_contract_test.py'
python -m unittest discover -s tests -p 'subagents_test.py'
python -m unittest discover -s tests -p 'mcp_*test.py'
python -m unittest discover -s tests -p 'ai_*test.py'
python -m unittest discover -s tests -p 'make_clean_test.py'
python -m unittest discover -s tests -p 'plugin_test.py'
python -m unittest discover -s tests -p '*contract_test.py'
python tests/runtime_selection_test.py
python tests/archive_run_test.py
bash tests/ralph_model_test.sh
bash tests/ralph_review_test.sh
git diff --check
```

New Claude tests should follow the existing `unittest` conventions; select them
with `python -m unittest discover -s tests -p 'claude_*test.py'` once implemented.
Native validation includes `claude plugin validate .` and each of the five plugin
directories, after confirming CLI support. Exercise registration/install only
in approved project-local fixtures with isolated home/config/temp paths and an
allowlisted environment. Native session tests require their own execution/model
grant; no automatic logins, server downloads or live-write tests.

Run focused checks as each responsibility changes, then a relevant combined
regression pass. Broaden to `python -m unittest discover -s tests -p '*test*.py'`
when integration changes justify it and prerequisites are available. Report
dependency/native skips as unavailable evidence. Never run `make install` or
global `make clean` as validation.

## Optional follow-ups and handoff

Sprite generation requires a separately selected Claude-accessible image provider,
verified schema, project-output behavior and spending approval. Notifier parity
requires an explicit selection of Claude events, privacy-preserving payloads and
notification approval. LSP/UI preferences can be assessed independently. None
requires changing the five-plugin packaging or porting Ralph.

Coverage: CC-02 covers marketplace compatibility; CC-03 covers configurations;
CC-04 covers all MCP definitions; CC-05–CC-07 cover roles, commands, helpers and
lifecycle tooling; CC-09 owns base integration and CC-08/CC-10 own advanced
workflow qualification. Shared helpers/shell/local models are assessed for reuse,
with explicit limits rather than unsupported rewrites.

Open handoff decisions are the authorization-control policy boundary, actual
Claude release/native capabilities, acceptance of the proposed settings ownership
policy, and whether to include advanced workflow qualification in the first
release. Proposed scope is concrete for review; these decisions and installation
authority are not implied by the request to generate this plan.
