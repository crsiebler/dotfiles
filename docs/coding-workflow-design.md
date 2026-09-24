# Coding workflow ownership and evaluation baseline

US-001 captures the source before instruction replacement. It specifies intended
ownership and evaluations; it does not establish model performance or activation.
Requirements: [PRD](../tasks/prd-coding-workflows-and-review-architecture.md).

## Immutable baseline

The baseline is Git commit `a6c3b8f2ec7ee0b231eeeef11342f17b617a23a9`, the
clean starting commit on `refactor/coding-skills-for-ponytail`. Read a baseline
artifact with `git show <revision>:<path>` without switching branches. The
[evaluation fixture](../tests/fixtures/coding_workflow_evals.json) records SHA-256
digests of the baseline policy, skills, roles, orchestration, and validation
sources. Digests identify bytes, not successful behavioral evaluations. Retain
this revision and fixture during migration; later runs record a separate exact
candidate revision and configuration.

No model runs, grading, latency/token/cost measurements, or installed-discovery
verification have occurred for this change. The existing
[planning scenarios](../tests/fixtures/implementation_planning_evals.json) are
also specifications, not observed results. They remain authoritative regression
scenarios for planning, execution, and recovery; do not rewrite them as passing
coding evaluations.

## Personal-policy obligation map

Source: baseline [personal policy](../ai/AGENTS.md). Row IDs enumerate each
Coding Standards and Testing bullet in source order. The destination names are
planned US-002/003/008 deliverables, not already installed capabilities.
The template means `docs/templates/code-repository-AGENTS.md`; development
references live inside `ai/plugins/coding/skills/develop-code/`.

| ID | Existing obligation | Future owner and preservation rule |
| --- | --- | --- |
| CS-01 | Run typecheck before commit; report unavailable | Template verification and development testing strategy; never label missing checks passing |
| CS-02 | Language idioms, architecture, package manager, lint/format rules | Template project facts and development root; repository configuration wins |
| CS-03 | Format changed files before final checks/commit; no unrelated formatting | Development testing strategy and `format-code`; template verification |
| CS-04 | Disclose unavailable formatter; no unauthorized installation/config changes | Development reporting; authorization restrictions remain personal policy |
| CS-05 | Focused, cohesive, readable modules; separate divergent responsibilities | Template principles and conditional architecture decisions; evidence of maintenance cost |
| CS-06 | Roughly 300 lines; assess separation at 500; project limits take precedence | Template editable review guidance, explicitly not quality gates or targets; architecture guidance preserves cohesion and project-specific limits |
| CS-07 | Exceptions for generated/declarative/fixture files; no arbitrary splitting | Template size guidance and architecture decisions; preserve justified cohesive artifacts |
| CS-08 | Configured formatter determines line width | Template conventions and `format-code` |
| CS-09 | Smallest correct change; no checklist-driven abstractions | Development root and architecture decisions; preserve all requested behavior |
| CS-10 | Complete authorized implementation/checks; preserve planning/read-only scope | Personal authority boundary retained; development scope selection supplies method |
| CS-11 | Supplied context first; relevant inspection, no whole-repo map by default | Personal proportional tool use retained; development action and review scope references specialize it |
| CS-12 | Routine scoped decisions; ask for material gaps/new authority | Personal authority and autonomy policy retained; no workflow may expand authority |
| T-01 | Meaningful failing tests before new behavior/fixes | Development feature/bugfix actions and testing strategy; confirm intended failure |
| T-02 | Relevant tests for logic; integration tests for critical paths | Development testing strategy; template risk-based checks; authorization still applies |
| T-03 | Preserve refactor tests; add missing characterization | Development refactor action and template compatibility expectations |
| T-04 | Schema/lint/build for static docs/config; no spelling tests | Development testing classification and template verification |
| T-05 | Required checks; broaden/repeat only with reason | Development testing strategy and `run-tests`; template command inventory |
| T-06 | No weakened assertions, hidden failures, or discarded work to reenact TDD | Development testing strategy/anti-patterns; personal truthfulness and preservation retained |

All other policy sections stay globally applicable: Communication Style (including
truthful evidence), Git Workflow (commit convention and explicit authority),
Boundaries (security, Git, filesystem, databases, packages, configuration, external
services, and process management), and Tool Usage (available tools, bounded
delegation, untrusted content, and no denial bypass). Condensing engineering
methods must not remove any operation-specific restriction. In particular,
moving test procedures grants no authority for dependencies, auth edits,
migrations, processes, source deletions, installations, or external writes.

US-008 must reconcile every row against the actual resulting text. Review lenses
assess these contracts but do not become their implementation owner. No mandatory
third standards skill or prerequisite loading between development and review.

## Skill obligations and identifier migration

| Baseline source | Obligations retained at destination |
| --- | --- |
| `implement-feature/SKILL.md` | `develop-code` root + feature action: scope, relevant code/tests, test-first, existing architecture, useful seams, compatibility/errors, focused checks, typecheck/UI evidence, gaps, no implicit delivery operations |
| `develop-with-tests/SKILL.md` | Development testing strategy: all five change classes, intended red/green, regression scope, honest pre-existing work/test order, no invented proof |
| `develop-with-tests/references/testing-anti-patterns.md` | Development bundled anti-patterns: observable behavior, legitimate interaction contracts, fixture-owned cleanup, boundary doubles, scoped patching/seams, parsed configuration, realistic fixtures, integration limits, focused assertions; preserve substantive examples |
| `refactor-code/SKILL.md` | Development refactor action: concrete maintenance problem, callers, passing baseline, characterization, small transformations, public/dependency contracts, separate intended behavior changes, final compatibility checks |
| `review-code/SKILL.md` | Same independently discoverable name; scope/lens references extend assessment. Preserve evidence, root-cause deduplication, severity, verified locations, constraints, untrusted-input treatment, and honest limits; clarify ambiguous reproduction language as tracing/supplied evidence only |

The three development identifiers map to `develop-code`. `review-code` stays
active. Keep old source trees through US-011; US-012 requires explicit exact-tree
deletion approval. Temporary source overlap does not prove unique discovery.
Independently installed bundles resolve their own references, never sibling
paths. Distinct helpers remain separate and are selected only when applicable.

## Consumer inventory

Baseline search: `git grep -n -E
'implement-feature|develop-with-tests|refactor-code|review-code' <revision>`.
Search all tracked files, including hidden manifests. Classify archives and
task-source mentions separately from active consumers; rerun before retirement.

| Consumer or surface | Baseline evidence and required action |
| --- | --- |
| `implement-feature/SKILL.md:10`, `refactor-code/SKILL.md:13` | Both reference `develop-with-tests`; replace internal method ownership in the new bundle; retire old roots only in US-012 |
| Four skill frontmatter names | Three names retire, review name remains; no permanent alias wrappers |
| `docs/ai-configuration.md:55` | Explicit coding skill inventory must reflect final discovery in US-012 |
| `PLAN.md`, `tasks/prd-coding-workflows-and-review-architecture.md` | Historical/planned names establish migration scope; preserve provenance rather than global search/replace |
| `.agents/plugins/marketplace.json`, `ai/plugins/coding/.codex-plugin/plugin.json` | Directory-based registration; keep five plugin identities and local paths unchanged |
| `scripts/install-ai.py:local_plugins`, `install_skills` | Directory discovery, matching frontmatter names, uniqueness, copy-safe paths; no hardcoded old-name migration needed |
| `scripts/ai_retirement.py` and `tests/ai_retirement_test.py` | Generic verified ownership/backup reconciliation; no manufactured inventory or special-case deletion |
| `ai/AGENTS.md` | No literal old skill identifiers; use obligation map, not name replacement |
| `run-tests`, `format-code` | No literal old identifiers; narrow descriptions/adapters need US-010 generalization while preserving repository-native command selection |
| `prepare-implementation` execution references, native reviewers, `/review-pr` | No literal old development consumers; preserve independent orchestration; any new method handoff must be one-way |
| Six targeted native role TOMLs | No literal old skill identifiers; inspect expertise/lifecycle statements individually in US-009, not bulk replacement |
| README, root AGENTS, authoring/removal guides | No baseline literal old-name consumers outside the inventory above; add migration/activation instructions in US-012 |

No baseline executable test directly hardcodes the three retiring names. Generic
tests still constrain discovery, installation, preservation, and rendering.
Archived runs are historical evidence and must not be rewritten. Installed
private/shared roots and plugin caches are outside this source inventory and have
not been inspected or changed.

## Dedicated review and execution invariants

- `prepare-implementation/references/story-execution.md` owns adapter selection,
  exact prepared-branch guards, explicit execution/commit authority, risk budgets,
  staging, session provenance, blocker resumption, memory/journal, and finalization.
- Sibling `story-review.md` owns the full packet protocol and exact JSON schema.
  Codex `story-reviewer` requires `expanded-initial` (up to 40 small initial evidence
  calls); native OpenCode `ralph-reviewer` requires `three-step` with `steps: 3`.
  Targeted passes retain two evidence-gathering turns. Profiles grant no tools.
- Preserve one initial and at most one targeted pass in the same actual story
  session, required full protocol delivery, staged evidence, and persistent
  blockers. Generic review and advisors cannot substitute for required reviewers.
- Preserve project-local read/staged-Git-only review, no tests/edits/browser/MCP,
  native metadata, eight read-only roles, 128 canonical roles and three native
  OpenCode-only roles. Runtime overrides and MCP permissions remain independent.
- `ai/opencode/commands/review-pr.md` owns PR orchestration and GitHub schema;
  exact posting preview and explicit approval remain required. Generic review
  does not post. `resolve-review-feedback` retains disposition/reply/resolution
  lifecycle; architecture/planning retains design-proposal review.
- Methods do not start story execution, create journals/memory, reset review
  budgets, or invoke orchestration recursively. No extra mandatory review cycle.

## Validation ownership and limitations

| Evidence source | What it can establish |
| --- | --- |
| `make validate-ai` / `scripts/install-ai.py` | Local structure, skill names/uniqueness, JSON/TOML parsing; no model or MCP startup |
| `tests/ai_install_test.py` | Parsed discovery contracts and isolated byte-identical personal-policy copying, preservation, CLI sequencing; no live personal installation proof |
| `tests/plugin_test.py` | Isolated native plugin registration, pinned CLI dependent; not model skill selection |
| `tests/agent_contract_test.py`, renderer `--check` | Role counts, metadata, read-only mapping, byte/body preservation; not immutable runtime containment |
| `tests/story_execution_test.py`, `tests/story_blocker_test.py`, `tests/ralph_review_test.sh` | Existing protocol/profile/schema/session/blocker regression contracts; not actual reviewer quality |
| `tests/fixtures/implementation_planning_evals.json`, `tests/fixtures/agent_evals.yml` | Baseline scenario specifications; no inferred observed results |
| New coding evaluation fixture | Baseline artifact identity, positive/negative cases and evidence requirements; US-011 runs remain pending |

No standalone typecheck target or configured Markdown/JSON formatter was found
in the baseline Makefile or tracked project configuration. Record unavailable
checks separately. JSON parsing, local link/artifact checks and `git diff --check`
are appropriate for this story; prose spelling tests would not prove behavior.

## Evaluation protocol awaiting authorization

Each fixture case specifies context, request, expected route, observable outcomes,
and prohibited outcomes. Reserved cases are held back from tuning; because they
are visible in the repository, they are not blind holdouts. Before US-011 runs,
agree whether independently prepared unseen variants are required, along with
runtime/model, repetitions, tool configuration, grading, budget and delegation.
Do not fabricate that agreement or run paid/bulk evaluations to fill this table.

Use isolated baseline and candidate sessions with the same approved inputs and
capabilities. Record exact revisions, configuration, prompts, relevant outputs,
tool traces and artifact changes per run. Separate static checks, manual
walkthroughs, live model behavior and post-install discovery. Never infer live
behavior from fixture parsing or prompt wording. Unknown measurements stay null.
Unauthorized mutation, fabricated evidence or required-review bypass blocks
promotion; comparative quality thresholds remain unagreed until authorized.
