# PRD: Claude Code configuration and skill marketplace support

Status: Draft requirements for review.
Revision: `claude-support-requirements-v1`.
Prepared: 2026-10-20.
Skill inventory and compatibility scope refreshed: 2026-11-08 against
`fd4874af9c7945e141276c10f115ebdceac45e06`, using the current
[47-skill dependency inventory](../docs/skill-dependencies.md).

## Problem and intended outcome

The repository distributes personal AI configuration, native specialist roles and
the Craft skill marketplace to Codex and OpenCode. Claude Code currently has no
repository-owned installation target or compatible marketplace index. Users
cannot adopt the same maintained skills and configuration policy through a
supported, repeatable Claude setup.

Add Claude Code as an explicitly selected consumer of these sources. Users must
be able to install Craft skills independently of personal configuration, and the
repository owner must be able to install Claude configuration with predictable
ownership, preservation, verification and rollback behavior.

The primary users are the repository owner, users installing Craft into Claude
Code, and assistants using its advertised skills and native roles. Support must
preserve existing Codex/OpenCode behavior and distinguish discoverable content
from runtime capabilities that have actually been verified.

## Sources and scope

The requested scope is Claude Code support for configurations and the skill
marketplace, informed by the earlier research into MCP connections, agents,
scripts and tools. Sources are:

- [Compatibility assessment](../docs/claude-code-support-assessment.md), including
  its official Claude documentation references and research limitations.
- [Existing implementation proposal](../PLAN.md), which remains a proposal and
  contains broader workflow qualification work.
- [AI configuration guide](../docs/ai-configuration.md),
  [personal policy](../ai/AGENTS.md), and repository `AGENTS.md`.
- [Marketplace inventory](../.agents/plugins/marketplace.json),
  [Codex configuration](../ai/codex/config.toml),
  [OpenCode configuration](../ai/opencode/opencode.json), and
  [agent authoring contract](../docs/agent-authoring.md).

Source baseline: `c6c48a64e83697ddf079578a54ad5594bc525457`, plus the existing
uncommitted assessment and plan. Their presence does not indicate approval to
implement their proposed mechanisms.

This document defines outcomes and acceptance. It does not authorize execution,
installation, dependency setup, authentication, configuration changes, commits,
external writes or cleanup, and it creates no execution state.

### Included

- Claude-compatible discovery, packaging and installation of the five existing
  Craft plugins and all 47 shared skills.
- Personal policy, Claude settings, MCP configuration, native agent definitions
  and agent discovery needed for supported configuration use.
- Explicit Claude installation, preview, validation, update and rollback behavior.
- Shared skill routing and documented native entry points, dependency boundaries,
  unsupported capabilities and regression protection.

### Scope assumptions for review

The initial supported environment is local Claude Code on the owner's macOS
development machine. Portable sources should remain reusable elsewhere, but
Windows, cloud sessions and other clients require separate verification.

The five maintained canonical roles are included as configuration. Full autonomous
delivery and team-workflow parity are a separate qualification scope, not a
prerequisite for the base configuration/marketplace release. Publishing a role
must not imply that every workflow using it is supported.

## Functional requirements and acceptance

### FR-01 — Preserve a single shared skill source

Craft must expose the existing plugin and skill identities to Claude without a
separate hand-maintained copy of each skill.

| Plugin | Baseline skill count |
| --- | ---: |
| `coding` | 25 |
| `reporting` | 4 |
| `researching` | 7 |
| `delegating` | 2 |
| `producing` | 9 |

Acceptance:

- All five plugins retain their names and ownership of the 47 existing skill
  identifiers. Each skill has one canonical source under `ai/plugins/`.
- Claude and Codex metadata refer to the same skill content; OpenCode continues
  consuming those sources through its existing supported installation path.
- Bundled references, scripts, dependency declarations, licenses and attribution
  remain available. Claude additions do not silently rename or retire skills.
- A shared-content change is reflected in each harness's distribution after its
  documented refresh, without maintaining independent skill-body forks.

### FR-02 — Provide a native Claude marketplace

A user must be able to register Craft from this repository and install selected
plugins using Claude's supported plugin interface.

Acceptance:

- Claude recognizes a valid marketplace and valid manifests for all five plugins.
  Source paths resolve correctly from a local checkout and a repository-backed
  distribution fixture; a raw index without its assets is not advertised as an
  equivalent distribution method.
- Installing only one plugin does not require installing the other four unless
  an actual, declared dependency requires it.
- Each installed skill is discoverable through its documented Claude identity
  and can be explicitly invoked. Duplicate copies are not installed through a
  second unmanaged skill-installation mechanism.
- Duplicate identities, invalid metadata, missing payloads and unsafe paths are
  rejected with useful diagnostics.
- Marketplace-only installation does not install personal policy, register MCP
  servers, change personal permissions or install the specialist collection.
- Installation and refresh behavior is documented and verified on the selected
  Claude release, including how local edits and distributed updates take effect.

### FR-03 — Preserve installed skill behavior and resources

Supported skill operations must use their installed resources and retain their
existing scope, dependency and approval boundaries.

Acceptance:

- Skills resolve references and helpers from their actual loaded location without
  hardcoded cache paths or dependence on the original dotfiles checkout.
- Helper outputs belong to the active project or another explicitly approved
  destination; installed bundles are not used as writable work directories.
- Portable document, GIF, audio, skill-authoring and archival helpers retain their
  existing data contracts and dependency ownership.
- Missing packages, models, renderers, provider tools or permissions produce an
  actionable limitation; installation does not download them automatically.
- Every skill has a documented supported or conditional Claude behavior. A
  missing backend must not result in fabricated tool calls or completion claims.
- Representative helper operations work from an installed/copied bundle, with
  fixture outputs inspected against their intended content. Extraction, rendering
  and recalculation limitations remain explicit.

### FR-04 — Load shared personal and project instructions

Claude must receive the intended repository and personal policy without creating
competing policy sources.

Acceptance:

- `ai/AGENTS.md` remains the canonical personal policy. Its installed Claude
  policy content preserves the source bytes without concatenated harness rules.
- Repository guidance is loaded through a documented, verified Claude mechanism,
  including applicable nested instructions and coexistence with Claude-specific
  instruction files. A prose suggestion to read policy is insufficient evidence.
- Claude-specific routing guidance does not duplicate or weaken shared rules.
- Installing policy preserves changed prior copies and reports conflicts according
  to the approved ownership rules.
- Documentation distinguishes personal-policy installation from marketplace-only
  use and project instruction loading.

### FR-05 — Manage Claude configuration with explicit ownership

The owner must be able to adopt maintained Claude settings without losing
unrelated personal settings, native application state or stronger restrictions.

Acceptance:

- Document which settings/files are repository-owned, native-CLI-owned or
  user-owned before installation writes occur.
- Preserve unrelated settings, third-party hooks/plugins, user model selection
  and stricter permission restrictions. Conflicting changes to owned settings
  stop for reconciliation rather than being silently overwritten.
- Honor supported absolute configuration-root overrides. Reject unsafe roots,
  symlinked managed destinations and unsupported layouts before modifying them.
- Back up changed managed content with a verifiable mapping to its destination.
  Preserve original bytes and relevant filesystem permissions for rollback.
- Verify effective settings where scope/precedence changes their behavior; a
  syntactically valid fragment alone is not successful configuration verification.
- Do not blindly copy Codex sandbox settings, OpenCode permission syntax, GPT
  profiles, provider settings or UI options into Claude configuration.
- Existing Codex/OpenCode configuration replacement contracts remain unchanged.

### FR-06 — Support the existing MCP connection inventory

Claude configuration must represent the current connections and their activation
boundaries. Authentication and external server provisioning remain separate.

| Connection | Required activation scope | Required tool policy |
| --- | --- | --- |
| GitHub | Global after explicit personal installation | Exact approved reads allowed; writes and unknown tools ask |
| Exa | Global after explicit personal installation | Only the four currently approved research tools allowed |
| Context7 | Global after explicit personal installation | Only the two currently approved research tools allowed |
| Vercel | Explicit trusted-project opt-in | Every tool asks |
| Jira / Rovo | Explicit trusted-project opt-in | Exact approved reads allowed; writes and unknown tools ask |
| PostgreSQL | Explicit trusted-project opt-in | Safety-status read allowed; arbitrary SQL and other tools ask |
| Jev | Explicit trusted-project opt-in | Every tool asks |
| Docker gateway | Explicit trusted-project opt-in | Every tool asks; gateway/profile lifecycle separately authorized |
| Chrome DevTools | Explicit trusted-project opt-in | Preserve the existing enabled-server allow policy only within the authorized activation scope |
| Playwright | Explicit trusted-project opt-in | Same enabled-server allow boundary as Chrome |
| Jam | Explicit trusted-project opt-in | Same enabled-server allow boundary as Chrome |
| ElevenLabs | Explicit trusted-project opt-in | Every tool asks |

Acceptance:

- Only GitHub, Exa and Context7 are globally activated by the authorized personal
  configuration operation. Optional definitions remain inactive until explicitly
  selected, including in noninteractive sessions.
- Preserve logical names, intended transports, endpoints, toolsets, required
  environment references and timeout intent using verified Claude semantics.
- PostgreSQL and Jev use their existing separately built local Node entry points;
  setup does not clone/build `mcp-suite`, create databases or run evaluations.
- Preserve unrelated MCP registrations and native state. Do not replace an
  entire mixed-purpose Claude state file to add repository-owned connections.
- Missing credentials or executables produce safe, specific diagnostics.
  Credential values never appear in generated configuration, command previews,
  logs or errors. Use references rather than interpolated secrets.
- AWS and Elastic remain absent. Optional browser/audio tools are not implicitly
  downloaded or launched while validating configuration.

### FR-07 — Preserve permission outcomes across harnesses

Permission migration must preserve observable approval behavior rather than
merely translate configuration keys.

Acceptance:

- Exact read exceptions and unknown-tool behavior match FR-06, subject to any
  stricter user, project, managed or runtime restriction.
- Unlisted Exa/Context7 tools cannot execute; PostgreSQL `execute_query` requires
  approval regardless of whether a particular query appears read-only.
- Newly introduced mixed-server tools do not inherit blanket approval. Existing
  broad rules cannot accidentally suppress approved read exceptions or allow
  writes through precedence differences.
- A required permission-enforcement mechanism cannot fail into wider access when
  it is missing, malformed, crashes or times out. Unsupported enforcement leaves
  the affected integration unavailable with a precise explanation.
- Tests use independently specified expected outcomes and exercise approved
  reads, writes, unknown tools, stronger restrictions and failure paths.
- No permission bypass, security-feature disabling or modification of prohibited
  authorization logic is implied by this requirement. Any proposed new control
  must first satisfy the project-policy boundary described under open questions.

### FR-08 — Make native specialists and discovery available

Claude users must be able to discover and select the maintained specialist
collection with its supported restrictions intact.

Acceptance:

- The canonical TOML collection contains `researcher`, `planner`, `reviewer`,
  `auditor` and `operator`. Claude definitions preserve their responsibility,
  instructions, review contracts and names from this single authoring source.
- Supported metadata is translated deliberately; unsupported fields, invalid
  identities and collisions produce errors rather than silent capability changes.
- Roles inherit supported session/model choices unless the user explicitly chooses
  otherwise. Existing GPT preferences do not create Claude model pins.
- Only `auditor` has native read-only sandbox metadata. Preserve its prohibition
  on edits, tests, builds, active scans, mutation, delegation and external posts.
  Document and verify evidence-reading capabilities and runtime/MCP controls.
- The other four roles inherit supported runtime permissions. Preserve
  `reviewer` candidate protection and authorized focused verification.
  Explicit inspection-only requests prohibit tests, builds and browser actions.
- Agent discovery supports explicit Claude selection, user/project scopes,
  supported root overrides, exact-definition reads and duplicate detection.
  Static definition discovery is never reported as proof of native invocation.
- The single OpenCode-only role, `sprite-artist`, stays native to OpenCode.
  Qualify the generic `reviewer` for delivery through demonstrated independent
  binding, required evidence access and same-session targeted continuation.
  Use native role selection when supported. Otherwise supply the complete
  discovered reviewer instructions and applicable review contract to a fresh
  independent generic agent and record the actual binding.

### FR-09 — Provide correct Claude workflow entry points

Users must be able to select shared workflows in Claude without accidental
execution, unsupported harness switching or loss of approval requirements.

Acceptance:

- Document and verify native entry points for the supported skills. Separate
  short command aliases are optional unless explicitly selected for this release.
- Claude planning defaults to Markdown `PLAN.md`; explicit user format requests
  take precedence. Planning does not create execution journals, memory or runners.
- Requirements, reviews and shipping retain their scope boundaries and exact
  write-approval contracts. Supplied arguments are treated as data.
- If a Claude PR-review shortcut is provided, it retains the canonical review
  schema and exact-payload posting approval from the existing command contract.
- Sprite generation reports an unavailable backend until a Claude adapter is
  separately verified.
- Advanced team/delivery entry points refuse unsupported operation rather than
  waive evidence or reset consumed review budgets. Routine stories use focused
  checks and lightweight staged self-review. High-risk stories and explicit early
  gates require independent staged review with the complete `review-story`
  contract. Independent integrated review gates final local delivery and shipping.

### FR-10 — Install and update Claude through an explicit target

Claude personal setup must be a separately selected, repeatable operation with a
readable preview and clear prerequisites.

Acceptance:

- Provide an explicit Claude installation entry point and a read-only preview of
  intended destinations, owned changes, prerequisites and conflicts.
- Existing `make install-ai`, its current `all` selection, and shell-install
  behavior do not silently expand to install Claude.
- Claude-only setup does not require unrelated harness executables or a skill-copy
  utility merely because existing installation paths use them.
- Preflight required sources and destinations before changes. Missing or
  unsupported Claude capabilities stop with actionable diagnostics.
- Repeated installation preserves unrelated state and verifies the resulting
  configuration/plugin/agent content instead of relying only on CLI exit status.
- Failures identify partial changes truthfully and retain recovery evidence;
  success is not reported after an incomplete install or verification failure.
- No implicit dependency installation, login, shell/global Git changes, sudo,
  model provisioning, service restart or live MCP action occurs during setup.

### FR-11 — Preserve rollback and cleanup boundaries

Users must be able to recover from an update without losing unrelated work or
native Claude data.

Acceptance:

- Document and verify restoration of previously managed settings, instructions,
  role files and plugin registrations after an interrupted or unsuccessful update.
- Ownership records distinguish repository-managed assets from customized,
  unverified or unrelated content; installation does not manufacture ownership.
- Claude-only installation/retirement does not remove shared global skill copies
  or modify Codex/OpenCode installations.
- Any retirement or cleanup requires existing scoped authority, exact ownership
  and retained rollback evidence. A preview alone performs no removal.
- If cleanup is extended, it recognizes only approved installer backup patterns
  and preserves credentials, conversations, active files, native caches,
  unrelated backups and runner controls.
- Native plugin lifecycle operations use supported interfaces; manual cache
  deletion is not an update or rollback strategy.

### FR-12 — Publish verifiable support and operating guidance

Support claims must identify the tested configuration and distinguish source,
installation and live behavioral evidence.

Acceptance:

- Record the tested Claude version, platform, configuration scope and installed
  source revision. Unsupported versions fail or report a precise limitation.
- Document marketplace-only use, personal installation, refresh, optional MCP
  activation, dependencies, permissions, conflicts, recovery and rollback.
- Keep the skill dependency inventory and agent/configuration documentation
  aligned with the supported implementation.
- Report each conditional capability honestly, including unavailable renderers,
  providers, credentials and advanced execution controls.
- Existing historical verification records remain intact; source changes do not
  become claims of successful installed discovery or live integration.

## Verification and release acceptance

Release acceptance requires a complete user path: register Craft, install a
selected plugin, discover/invoke its skill, then separately adopt personal
configuration and verify instructions, agents and MCP policy. Repeating and
recovering that installation must preserve unrelated state.

The following evidence is required:

- Local source/configuration validation and relevant syntax checks pass. The
  repository has no standalone typecheck target; report that fact rather than
  inventing a passed check.
- Relevant installer, marketplace, discovery, agent, permission, rollback and
  existing Codex/OpenCode regression tests pass without weakening assertions.
- Isolated fixtures cover paths with spaces, root overrides, symlinks, missing
  prerequisites, conflicting/customized state, repetition and partial failures.
- Native Claude verification demonstrates plugin discovery, representative skill
  invocation, instruction loading, auditor restrictions and reviewer qualification.
- Fake MCP servers exercise permission behavior and local launcher contracts.
  Live authentication/connectivity tests are separately authorized and reported;
  client configuration success is not proof of a working external server.
- Tests and fixtures use project-local temporary paths and controlled environments
  without reading personal credentials or changing real user configuration.
- Missing native tools/dependencies and skipped checks are disclosed. Missing
  required native evidence prevents a full support claim.

This is configuration/CLI work, so browser verification is not a blanket release
gate. If a supported browser integration is exercised, verify that selected flow
through its available backend and report its actual limits.

## Non-goals

- Adding an alternate execution runner or porting OpenCode's native sprite role.
- Qualifying full Claude team execution or autonomous story delivery in the base
  release. Their existing skills remain discoverable with explicit capability gates.
- Adding a Claude sprite-generation provider, OpenCode notifier parity, new LSP/UI
  preferences or experimental team enablement by default.
- Routing Claude to existing GPT/Bonsai profiles or provisioning local models.
- Installing dependencies, browser binaries, external MCP servers or credentials
  as a side effect of marketplace/configuration support.
- Replacing skill helpers or changing existing serialized archival/evidence
  formats, including `CodexGoalMarkdown`, solely because another harness uses them.
- Publishing the marketplace remotely, changing CI/CD, or modifying production
  services as part of requirements authoring or automatic installation.

## Design constraints and unresolved decisions

Requirements prescribe behavior, not a mandatory new framework. The earlier
assessment proposes separate Claude manifests, a dedicated installer adapter,
bounded settings reconciliation and generated role definitions. Those remain
design recommendations until selected during implementation planning.

1. **Claude version and capability baseline:** select an actual available release
   and verify the required CLI, instruction, permission and agent behavior.
   Earlier research found no `claude` executable on the session PATH; no native
   compatibility has yet been established.
2. **Settings ownership:** choose the exact managed keys/files and reconciliation
   policy that satisfies FR-05 while preserving native and unrelated user state.
   Whole-file replacement of mixed-purpose state is not an acceptable shortcut.
3. **Authorization-control policy:** current instructions prohibit modifying
   authentication/authorization logic. If preserving FR-07 requires new guards,
   resolve that scope explicitly before implementation. This PRD does not approve
   such a change or prescribe the previously proposed hook as the only solution.
4. **Initial-release boundary:** this draft assumes base agent configuration and
   discovery are included, with full team/delivery qualification deferred. An
   expanded scope needs explicit acceptance for staged evidence, same-session
   targeted review, worktree ownership and existing delivery gates.
5. **Convenience commands:** namespaced skill entry points satisfy FR-09; exact
   legacy command aliases may be selected separately without duplicating policy.

The existing plan includes advanced workflow qualification beyond this draft's
base release. A later planning revision must reconcile that difference explicitly
and preserve its existing content; requirements authoring does not replace or
archive it.
