# Implementation plan: Coding workflows and review architecture

## Objective and context

- Requirements: [PRD](tasks/prd-coding-workflows-and-review-architecture.md),
  FR-1 through FR-11 and US-001 through US-012.
- Objective: independently discoverable development and read-only review workflows,
  portable project guidance, concise personal policy, and aligned specialist roles.
- Scope: consolidate three development skills into `develop-code`; expand
  `review-code` with scopes/lenses; publish the project AGENTS template; align six
  native agents, helpers, consumers, validation, and migration documentation.
- Non-goals: PRD section 7; no installation, automatic retirement, deployments,
  external posts, renderer redesign, broad agent rewrite, or altered review gates.
- Base branch: `main`; planning baseline cb49f230b0f0a77ab8633e5d45f2092ebbbca0e1.
- Working branch: `refactor/coding-skills-for-ponytail`, prepared and selected by
  the user; verified at existing commit a6c3b8f2ec7ee0b231eeeef11342f17b617a23a9.
- Format: explicitly continued Markdown PLAN.md workflow; CodexGoalMarkdown adapter
  for later authorized execution. Planning occurred in OpenCode, not a Codex Goal.
- Mode: standard; use the shared risk-based advisor/self/native-review budgets.
- Authorization: plan branch update and implementation granted on 2026-09-24.
  Execution and per-story commits explicitly authorized on 2026-09-24. Installation, source
  deletions, evaluations with spending/delegation, and other sensitive operations
  require applicable approval.
- Delivery: one explicitly authorized commit per verified, reviewed story.
- Current status: US-001 through US-010 delivered; US-011 and US-012 pending. Prior run
  archived under `archive/2026-09-24-producing-and-document-skills/`.
- Preparation baseline is committed at a6c3b8f2ec7ee0b231eeeef11342f17b617a23a9;
  execution began with a clean worktree. Preserve any subsequent unrelated work.

## Common acceptance and verification requirements

Every story inherits these requirements; specific checks below supplement them.

- Read applicable repository instructions and affected contracts. Use installed
  skill-relative references; do not hardcode checkout or plugin-cache paths in
  generated runtime instructions. Keep skill bundles independently usable.
- Prose/configuration changes use source, structure, link, schema, and meaningful
  contract validation. Add failing regressions before executable behavior changes;
  do not manufacture test-first evidence for existing work or test prose spelling.
- Required source check: `make validate-ai`. Diff check: `git diff --check`.
- Focused Python checks use the existing pattern
  `python3.11 -m unittest discover -s tests -p '<filename>'`.
  Inspect each named suite before relying on its coverage.
- Agent checks: `python3.11 tests/agent_contract_test.py` and
  `python3.11 scripts/render-agents.py --harness opencode --check` plus
  `python3.11 scripts/render-agents.py --harness codex --check` when roles change.
- Protocol checks when affected: `python3.11 tests/story_execution_test.py`,
  `python3.11 tests/story_blocker_test.py`, `bash tests/ralph_review_test.sh`.
- Final relevant regression command:
  `python3.11 -m unittest discover -s tests -p '*test*.py'`.
  Missing optional dependencies/skips are recorded; distinguish unrelated baseline
  gaps from required changed-contract checks. Do not install tools without approval.
- Typecheck: no standalone repository target exists. Record it unavailable, never
  as passing; source validation and relevant tests provide separate evidence.
- Formatting/lint: no project Markdown/JSON formatter configuration was found.
  Reinspect applicable configuration at execution; run configured formatters on
  changed files before final verification and disclose missing tools/configuration.
- No product UI is planned. If UI is introduced within approved scope, use
  `verify-interface`; static instructions are not rendered/browser verification.
- Preserve native role metadata, all five plugin identities, 128 canonical agents,
  three OpenCode-only roles, byte/body rendering, permissions, and review contracts.
- Static checks and manual walkthroughs are not model-behavior evaluations. Record
  evidence provenance and unavailable live evaluation/activation independently.
- Optional implementation advisors are read-only, at most two under the shared
  budget. Suggestions below are not delegation authority or proof of availability.
  The executor implements/tests. No agent per lens or automatic delegation chain.
- Native staged reviewer: `story-reviewer` when the mode/risk budget requires it;
  general reviewers are advisors only and cannot replace that gate.

### Shared execution checklist (applies to each story)

- [ ] Verify execution/commit authority, exact prepared branch, and existing state.
- [ ] Inspect relevant code/contracts; implement only the story's scoped candidate.
- [ ] Apply appropriate test-first or source validation and configured formatting.
- [ ] Run required checks; record unavailable typecheck and other limitations.
- [ ] Stage intended files and satisfy the mode-aware staged review contract.
- [ ] Resolve actionable findings, rerun affected checks, and use at most one
  targeted same-session follow-up where permitted.
- [ ] Append progress, update only validated memory, finalize completion metadata,
  and deliver through the authorized story commit. This reusable checklist is not
  a substitute for individual story evidence in the journal.

## Ordered stories

### US-001 - Map ownership and define baseline evaluations
- [x] Story complete
- Priority: 1
- Depends on: none
- PRD: US-001; FR-8 through FR-11 and evaluation section.
- Benefit: preserve obligations and establish observable migration criteria.
- Paths: proposed `docs/coding-workflow-design.md`, existing source skills and
  `ai/AGENTS.md`, `tests/fixtures/implementation_planning_evals.json`, proposed
  `tests/fixtures/coding_workflow_evals.json`.
- Advisors: optional @prompt-engineer; question: discovery boundaries and useful
  held-out cases, without introducing unnecessary mandatory loading.
- [ ] Map every moved policy obligation and old identifier to its new owner.
- [ ] Inventory consumers and document preserved dedicated-review invariants.
- [ ] Specify positive/negative discovery cases and evaluation evidence fields,
  including noncoding tasks and read-only requests; mark results unrun.
- [ ] Capture an immutable baseline by source revision/artifact references before
  replacing instructions. Set runtime/budget/criteria only with authorization.
- [ ] Source/fixture parsing and common verification requirements satisfied.

### US-002 - Add unified development and testing workflow
- [x] Story complete
- Priority: 2
- Depends on: US-001
- PRD: US-002; FR-1 and FR-3.
- Benefit: one development entry point selects feature, diagnosis/fix, or refactor.
- Paths: new `ai/plugins/coding/skills/develop-code/`, existing
  `develop-with-tests/references/testing-anti-patterns.md`, proposed
  `tests/coding_workflow_contract_test.py`, `tests/plugin_test.py` as applicable.
- Advisors: none by default.
- [ ] Add root routing plus feature, bugfix, refactor, testing-strategy, and
  anti-pattern references; preserve substantive existing testing guidance.
- [ ] Preserve planning/diagnosis-only boundaries and actual test-order reporting.
- [ ] Require causal evidence for fixes and compatibility evidence for refactors;
  do not impose test-count ceilings or drop requested requirements.
- [ ] Keep old bundles intact until the approved retirement story; document the
  temporary source overlap rather than claim final unique discovery.
- [ ] Meaningful resource/metadata/independent-bundle checks and common gates pass.

### US-003 - Add conditional architecture decision guidance
- [x] Story complete
- Priority: 3
- Depends on: US-002
- PRD: US-003; FR-2.
- Benefit: apply engineering theory without speculative architecture ceremony.
- Paths: `develop-code/SKILL.md`, `develop-code/references/architecture-decisions.md`,
  coding workflow evaluation/contract fixtures.
- Advisors: optional @architect-reviewer; question: when a boundary or replacement
  is justified and which invariants establish behavioral equivalence.
- [ ] Cover reuse order, responsibilities, coupling, contracts, state, workload,
  reversibility, and decision-triggered ADR guidance.
- [ ] Include useful-abstraction and unsafe-shorter-replacement counterexamples.
- [ ] Root loads guidance conditionally; routine local changes need no full ADR.
- [ ] Resource closure, source validation, and common gates pass.

### US-004 - Establish review scopes and evidence contract
- [x] Story complete
- Priority: 4
- Depends on: US-001
- PRD: US-004; FR-4, FR-5, FR-7.
- Benefit: discover read-only assessment independently from development.
- Paths: `review-code/SKILL.md`, `review-code/references/scopes/`, coding fixtures
  and contract tests; read existing `/review-pr` and feedback skill for boundaries.
- Advisors: optional @code-reviewer; question: mutation-free scope routing and
  evidence requirements without duplicating native staged/PR schemas.
- [ ] Provide local, PR/branch, component, and bounded audit scope references.
- [ ] Cover release/cross-component variants and missing evidence; distinguish
  introduced/exposed/pre-existing defects and optional maintenance suggestions.
- [ ] Tests, edits, formatting, posting, and automatic fixes remain outside review.
- [ ] Preserve feedback ownership, dedicated reviewer exclusions, and caller schemas.
- [ ] Source/resource and applicable protocol checks plus common gates pass.

### US-005 - Add maintainability, compatibility, and testing lenses
- [x] Story complete
- Priority: 5
- Depends on: US-004
- PRD: US-005; FR-6 and FR-7.
- Benefit: assess reasoning/change cost without superficial size heuristics.
- Paths: `review-code/references/lenses/{architecture-and-maintainability,compatibility,testing-quality}.md`,
  review routing and evaluation fixtures.
- Advisors: none by default.
- [ ] Cover coupling, cohesion, semantic/cognitive/cyclomatic/state complexity and
  duplicated rules; actual maintenance evidence determines findings.
- [ ] Explain metric limitations, project thresholds, and prohibition on invented
  scores or arbitrary extraction merely to lower a metric.
- [ ] Preserve compatibility/error/lifecycle contracts and meaningful test adequacy.
- [ ] Wire conditional loading and verify fixture/resource coverage; common gates pass.

### US-006 - Add security, data/state, and reliability lenses
- [x] Story complete
- Priority: 6
- Depends on: US-004
- PRD: US-006; FR-6.
- Benefit: inspect authority, invariants, concurrency, and failure transitions.
- Paths: `review-code/references/lenses/{security-and-privacy,data-and-state,reliability}.md`,
  review routing/evaluation fixtures.
- Advisors: none by default; specialized advice only for a concrete material gap.
- [ ] Cover trust boundaries, sensitive data, transactions, precision, races,
  retries, idempotency, cancellation, cleanup, and evolution compatibility.
- [ ] Require triggering paths and contract evidence; do not authorize active
  testing, auth changes, migrations, or infrastructure operations.
- [ ] Conditional references and no-mutation scenarios validate; common gates pass.

### US-007 - Add performance, accessibility, and operations lenses
- [x] Story complete
- Priority: 7
- Depends on: US-004
- PRD: US-007; FR-6.
- Benefit: evaluate workload, user access, deployment, and dependency risks honestly.
- Paths: `review-code/references/lenses/{performance,accessibility,operability-and-dependencies}.md`,
  review routing/evaluation fixtures.
- Advisors: none by default.
- [ ] Cover resources/query cost, UI semantics/focus/errors, observability,
  shutdown/configuration, rollout/rollback, packaging, and reproducibility.
- [ ] Separate supplied rendered/runtime evidence from source inspection; no
  automatic tools, browser actions, installs, or specialist delegation in review.
- [ ] Resource/routing and evidence-provenance cases validate; common gates pass.

### US-008 - Publish project guidance and refine personal policy
- [x] Story complete
- Priority: 8
- Depends on: US-001, US-003, US-004
- PRD: US-008; FR-8.
- Benefit: portable project standards without engineering bloat in noncoding work.
- Paths: `ai/AGENTS.md`, new `docs/templates/code-repository-AGENTS.md`,
  `docs/coding-workflow-design.md`, relevant `tests/ai_install_test.py` contracts.
- Advisors: none by default.
- [ ] Publish the standalone template with verified-fact/command placeholders,
  principles, contracts, methods, review, and handoff expectations.
- [ ] Explain merge/adoption for existing and mixed-purpose projects; no global
  installation, blind replacement, or mandatory personal skill names.
- [ ] Relocate policy details using the obligation map; retain global authority,
  privacy, preservation, and concise advertised-skill routing without weaker rules.
- [ ] Validate byte-identical personal-policy installation contracts and common gates.

### US-009 - Align six native specialist roles
- [x] Story complete
- Priority: 9
- Depends on: US-003, US-005, US-006, US-007
- PRD: US-009; FR-9.
- Benefit: focused expertise reinforces methods without conflicting lifecycles.
- Paths: `ai/codex/agents/{prompt-engineer,architect-reviewer,code-reviewer,refactoring-specialist,debugger,test-automator}.toml`,
  `docs/agent-authoring.md`, `tests/fixtures/agent_evals.yml` if relevant.
- Advisors: optional @architect-reviewer; question: conditional specialist detail
  versus universal outcome claims and lifecycle duplication.
- [ ] Align discovery descriptions and core role bodies using actual source evidence.
- [ ] Remove unwarranted universal gains/framework/commit expectations; preserve
  native metadata, read-only restrictions, domain knowledge, and independent use.
- [ ] Document justified additional-role candidates without broad rewriting.
- [ ] Agent contracts and both renderer checks pass; common gates satisfied.

### US-010 - Integrate helper routing and execution handoffs
- [x] Story complete
- Priority: 10
- Depends on: US-002, US-004, US-008, US-009
- PRD: US-010; FR-10.
- Benefit: new methods fit both harnesses without changing delivery controls.
- Paths: `run-tests/SKILL.md`, `format-code/SKILL.md`, actual inventoried consumers,
  `prepare-implementation/references/story-execution.md`, related tests.
- Advisors: none by default.
- [ ] Generalize helper entry descriptions while retaining conditional adapters
  and project-native command selection; do not add runtime dependencies.
- [ ] Update genuine consumers without cyclic loading, new schema ownership,
  mandatory second reviews, or reviewer discovery dependencies.
- [ ] Preserve profiles, packets, branch/authorization guards, sessions, budgets,
  blocker/resume state, memory/journal ownership, and finalization rules.
- [ ] Story execution/blocker and Ralph review checks plus common gates pass.

### US-011 - Evaluate discovery and engineering outcomes
- [ ] Story complete
- Priority: 11
- Depends on: US-003, US-005, US-006, US-007, US-008, US-009, US-010
- PRD: US-011; Section 8 and FR-11.
- Benefit: promotion decisions use actual evidence rather than shorter-prompt claims.
- Paths: coding evaluation/contract fixtures, proposed
  `docs/coding-workflow-verification.md`; existing create-skill evaluation helpers
  only if suitable and authorized.
- Advisors: none unless evaluation scope explicitly authorizes independent graders.
- [ ] Finalize agreed runtime/model, repetitions, held-out cases, grading criteria,
  spending/delegation scope, and baseline/candidate isolation before live runs.
- [ ] Exercise PRD positive/negative cases with permitted harness capabilities;
  include noncoding requests, review-mode discovery, unsafe simplification,
  pre-existing edits, unavailable tools, and required-reviewer blockers.
- [ ] Record exact provenance and observed artifacts; distinguish static checks,
  manual walkthroughs, live model evaluations, and post-install verification.
- [ ] Unauthorized mutation, fabricated evidence, or gate bypass blocks promotion.
  Missing authorized evaluation capability keeps required criteria pending; do
  not mark the story delivered by writing an unrun evaluation specification.
- [ ] Affected static tests and common gates pass; limitations are explicit.

### US-012 - Retire superseded sources and document activation
- [ ] Story complete
- Priority: 12
- Depends on: US-011
- PRD: US-012; FR-11.
- Benefit: safe migration to unique final discovery with recoverable assets.
- Paths: `ai/plugins/coding/skills/{implement-feature,develop-with-tests,refactor-code}/`,
  README.md, AGENTS.md, docs/{ai-configuration,agent-authoring,remove-old-ai-files}.md,
  affected `tests/{plugin,ai_install,ai_retirement}_test.py` and contract fixtures.
- Advisors: none by default.
- [ ] Obtain explicit approval for the exact three source-tree deletions. Retain
  relocated testing content and `review-code`; reconcile all active consumers.
- [ ] Keep plugin identities/counts and directory-based installation unchanged;
  do not add permanent wrappers or manufactured ownership records.
- [ ] Test intended final source discovery and generic retirement preservation of
  custom/unverified/symlinked assets. Run final relevant regression checks.
- [ ] Document coordinated activation, shared-root effects, backups, fresh-session
  discovery, and rollback. Never manually delete caches or install for validation.
- [ ] Live activation remains separately authorized and pending unless actually
  performed; source delivery does not claim installed discovery has changed.
- [ ] Final requirements audit and all common gates pass before authorized commit.

## Execution blockers and handoff

- Prepared branch and implementation authorization are established above.
  Execution and per-story commit authorization are established above.
- Agree evaluation scope before US-011; approve source deletions before US-012.
  Global activation remains a separate operation after source delivery.
- Installed planning instructions may be older than the checked-in archival-policy
  revision. Source edits do not establish refreshed live discovery; do not install
  during planning or claim the old installed copy was updated.

## Resume and delivery

- For authorized execution, load the installed `prepare-implementation` skill and
  read `references/story-execution.md` and `references/story-review.md` in full
  relative to its advertised base. Follow CodexGoalMarkdown. Missing discovery,
  required references, or native `story-reviewer` capability blocks execution;
  do not substitute checkout paths, general reviewers, or weaker protocols.
- Select the lowest numeric priority eligible incomplete story. Recheck the exact
  prepared branch before writes, staging, and commits; never create/switch branches
  or accept main/master/detached HEAD for implementation.
- Read relevant latest worktree-root `docs/progress.md` entries and `memory.json`
  when present. Keep this plan for scope, criteria, dependencies, concise status,
  and completion only. Append actual commands/results, review findings/dispositions,
  blockers, approvals, advisor use, commits, and resumption checkpoints to the
  journal; create it only at a permitted execution checkpoint.
- Missing memory is normal: use empty version-1 memory in process. Invalid memory
  blocks without overwrite. Create/update it only after passing review; retain
  at most 20 patterns and 20 evidenced suppressions. Do not reuse archived memory.
- Apply shared fast/standard/deep budgets, default standard. Self-review is allowed
  only by the risk budget and is not independent review. Native review requires
  the full protocol/schema embedded in every invocation, packet preflight,
  explicit `Review profile: expanded-initial` and `Pass type`, a fresh reviewer
  session per story, and recorded actual role/session ID rather than just a label.
- Permit one initial and at most one targeted pass in that same actual session
  per attempt. Preserve bounded evidence recovery, findings, and consumed passes.
  A final blocked/malformed review stops delivery; resumption requires verified
  material resolution, not continuation, compaction, or reviewer replacement.
- Stage provisional completion only after required checks/review pass. Delivery
  requires the authorized story commit to succeed; on failure restore only the
  provisional marker and append the exact blocker under the shared procedure.
- No implicit push, external post, installation, sensitive operation, or additional
  delegation. Native Goal continuation does not introduce Ralph loops or hooks.
- [ ] Final report lists actual delivered scope, commits, checks/reviews, unresolved
  evaluation/activation gaps, and any remaining limitations.
- After delivery, archival is separately approved under the applicable completed-run
  procedure. Do not reset journals, remove active state, or commit archives under
  story-commit authorization alone.
