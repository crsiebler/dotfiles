# Coding workflows and review architecture execution journal

## 2026-09-24 - US-001 candidate

- Feature / task source: `PLAN.md`, coding workflows and review architecture.
- Branch: `refactor/coding-skills-for-ponytail`; verified symbolic HEAD and
  existing commit `a6c3b8f2ec7ee0b231eeeef11342f17b617a23a9`; initially clean.
- Approvals: user explicitly requested recording this prepared branch and
  proceeding with implementation. Explicit per-story commit authorization is
  still pending; no staging or commits performed. Installation, source deletion,
  paid/bulk evaluations and evaluation delegation remain separately scoped.
- Implemented / files changed: recorded branch/implementation authority and
  reconciled stale preparation-state notes in `PLAN.md`; created
  `docs/coding-workflow-design.md` and
  `tests/fixtures/coding_workflow_evals.json`.
- Ownership evidence: 12 Coding Standards and six Testing obligations mapped
  individually; global restrictions retained; retiring identifiers, actual
  consumers, directory discovery, validation owners and dedicated-review
  invariants documented. Baseline search used `git grep` at the starting commit.
- Baseline evidence: 38 Git artifact SHA-256 digests; 25 representative/reserved
  scenarios with positive and negative routing/behavior expectations. Every
  baseline/candidate scenario is unrun and results are empty. Reserved cases are
  visible specifications, not blind holdouts. Runtime/model, repetitions,
  evaluation budgets, graders and comparative thresholds await agreement.
- Intended commit message: `feat(US-001): map coding workflow ownership and evaluation baseline`.
- Commit status: not_attempted; candidate remains unstaged and story incomplete.
- Runtime: Codex desktop, standard mode, CodexGoalMarkdown; exact model and
  model source unavailable in trusted runtime metadata; iteration limit unknown.
- Implementation risk: trivial documentation/declarative fixture; no executable
  behavior changed. No test-first claim or new spelling-based regression tests.
- Checks: `make validate-ai` passed (local source structure and JSON/TOML syntax;
  no model/MCP started); `git diff --check` passed. Inline Python 3.11 validation
  parsed the fixture, verified 38 hashes against Git blobs, unique scenario IDs,
  both partitions, required nonempty fields, unrun status, empty results, local
  Markdown links and all 18 policy-map IDs; passed. These checks do not establish
  model behavior or semantic sufficiency of future implementation.
- Typecheck: unavailable; no standalone repository target. Formatting: no
  configured Markdown/JSON formatter found; JSON emitted with two-space
  indentation and trailing newline. No formatter or dependency installed.
- Browser evidence: not applicable. Broader implementation/regression suites
  not run for this documentation/fixture-only candidate; no runtime contracts
  or agent sources changed.
- Implementation advisors: optional prompt-engineer skipped; bounded source
  inventory handled directly. No agents invoked or evaluations run.
- Review: staged review not started; explicit commit authority is required before
  staging for delivery. No review pass consumed, no reviewer session, no findings
  or validated memory created. Planned mode-aware self-review for this trivial
  documentation/declarative candidate uses expanded-initial and initial pass.
- Blocker / next checkpoint: obtain explicit per-story commit authority for the
  approved plan sequence, then stage only these four files, inspect the staged
  candidate under the full installed review protocol, and finalize US-001 only
  after passing review and successful commit. All later stories depend directly
  or transitively on US-001 delivery. Preserve this candidate while awaiting that
  authority; do not mark complete or start dependent stories.
---

## 2026-09-24 - US-001 authorization resolved

- User explicitly granted: "execution and commit authorized". This covers implementation and one verified, reviewed commit per story in PLAN.md. Preserve separate evaluation, deletion and installation approval boundaries.
- Verified current branch still matches the plan and the four existing candidate files remain the only changes. Prior authorization blocker resolved; no review passes previously consumed.
- Proceed to staged self-review under standard mode for this documentation/declarative baseline story.
---

## 2026-09-24 - US-001 finalization

- Review profile: expanded-initial; Pass type: initial; attempt 1. Self-review selected for trivial documentation/declarative diff in standard mode, not independent review.
- Inspected staged inventory, complete PLAN/design/progress patches and complete staged fixture; all four paths covered. No actionable findings. Reviewer session: not applicable.
- Structured review result:

```json
{
  "verdict": "pass",
  "pass_type": "initial",
  "findings": [],
  "resolved_findings": [],
  "executor_feedback": {
    "priority_order": [],
    "recommended_checks": [],
    "avoid": []
  },
  "residual_risks": [
    "Static specification only; live model evaluation and installed discovery remain unrun.",
    "Reserved cases are visible, not blind holdouts."
  ],
  "learning_candidates": []
}
```

- Prior source/fixture/link/hash checks remain applicable; authorization bookkeeping introduced no implementation change. Final diff check passed. Typecheck unavailable; no configured Markdown/JSON formatter. No memory learning justified; memory remains absent.
- All US-001 criteria satisfied by ownership map, consumer/invariant inventory, unrun positive/negative specifications and immutable baseline evidence.
- Commit status: pending (not yet delivered); intended message `feat(US-001): map coding workflow ownership and evaluation baseline`. Next story after successful commit: US-002.
---

## 2026-09-24 - US-002 candidate

- Implemented unified develop-code root with feature, causal bugfix, refactor and testing-strategy references. Copied the complete testing anti-pattern reference byte-for-byte. Old skill trees remain intact until US-012; discovery overlap is temporary, not final activation.
- Added tests/coding_workflow_contract_test.py for unique matching metadata, reference closure/reachability from an isolated project-local copy, and baseline testing-reference preservation. Three tests first failed because the bundle/reference was absent; all three passed after implementation. These are structural regressions, not model-behavior evidence or brittle prose checks.
- Checks: python3.11 -m unittest discover -s tests -p 'coding_workflow_contract_test.py' passed 3 tests; make validate-ai passed; git diff --check passed. No standalone typecheck or configured Markdown/Python formatter found. No browser scope.
- Optional create-skill helper check could not run: PyYAML absent in python3.11, system python3 and bundled Python; validate under python3.11 exited 3 for the same missing dependency. No installation or packaging attempted. Required repository-native source validation and independent bundle tests passed; portable helper validation remains unavailable, not passing. Live evaluations deferred to separately scoped US-011.
- Runtime: Codex desktop; standard mode, CodexGoalMarkdown; exact model/source and iteration limit unknown. Implementation risk standard; staged review classified test-sensitive because new resource-contract tests and executable agent instructions require native review.
- Advisors: none. Native staged reviewer required: story-reviewer, expanded-initial, initial, attempt 1. Review packet will embed the complete installed protocol. No passes consumed yet.
- Intended commit message: feat(US-002): add unified development and testing workflow.
- Commit status: pending (not yet delivered). User execution and per-story commit authorization retained. Separate deletion/evaluation/installation authority unchanged.
---

## 2026-09-24 - US-002 finalization

- Native role selected through agent_type: story-reviewer. Returned runtime session handle: `/root/review_us002_attempt1` (runtime exposes canonical agent name, no separate opaque ID). Story US-002, attempt 1, initial pass; same worktree.
- Full protocol/schema embedded in packet. One-word transcription correction in Learning Discipline (to/in) sent within the same live initial pass; no candidate mutation or additional pass.
- Reviewer read authoritative staged evidence and returned schema-valid pass with no findings. Initial consumed; targeted unused.
- Exact review result:

```json
{
  "verdict": "pass",
  "pass_type": "initial",
  "findings": [],
  "resolved_findings": [],
  "executor_feedback": {
    "priority_order": [],
    "recommended_checks": [],
    "avoid": [
      "Keep model behavior and live activation claims within separately scoped US-011; the reported checks establish source and bundle contracts only."
    ]
  },
  "residual_risks": [
    "The optional create-skill helper validation was unavailable because PyYAML is missing; no dependency was installed. Live evaluations remain deferred to US-011."
  ],
  "learning_candidates": []
}
```

- No accepted-fix learning or suppression warranted; memory remains absent. All scoped criteria met; portable helper/model-evaluation limitations retained above. Typecheck unavailable, no configured formatter.
- Commit status: pending (not yet delivered); intended `feat(US-002): add unified development and testing workflow`. Next eligible story after successful commit: US-003.
---

## 2026-09-24 - US-003 candidate

- Added conditional architecture-decisions reference and root trigger: material interface, responsibility, dependency, persistence, concurrency, trust-boundary or performance choices. Includes reuse order, theory as decision questions, useful single-adapter and unsafe replacement examples, proportional ADRs, workload evidence and reversal criteria.
- Added one unrun representative architecture evaluation scenario; immutable baseline untouched, all model results still empty. Existing bundle-closure test traverses the new reference from an isolated copy.
- Checks: python3.11 -m unittest discover -s tests -p 'coding_workflow_contract_test.py' passed 3; make validate-ai passed; git diff --check passed. JSON remains generated with two-space indentation. Typecheck unavailable; no configured Markdown/JSON formatter. Optional PyYAML helper limitation unchanged; no browser or live evaluations.
- Runtime: Codex desktop, standard mode, CodexGoalMarkdown; exact model/source and iteration limit unknown. Advisors: optional architect-reviewer skipped; requirements and contract counterexamples sufficient for this bounded guidance change.
- Review selection: self, trivial documentation/declarative change with no executable test or tool changes; expanded-initial, initial, attempt 1. Inspect all four staged files under the shared protocol, no independent-review claim.
- Intended commit: feat(US-003): add conditional architecture decision guidance. Commit status pending (not delivered); existing execution/commit authorization retained.
---

## 2026-09-24 - US-003 self-review initial

- Reviewed all staged paths. One fixture intent ambiguity requires correction; no architecture-content findings.

```json
{
  "verdict": "changes_requested",
  "pass_type": "initial",
  "findings": [
    {
      "id": "architecture-eval-implementation-intent",
      "severity": "medium",
      "lens": "qa",
      "title": "Make the implementation request explicit",
      "body": "The new scenario says Design while expecting develop-code:feature, which can reward routing a planning-only request into implementation. The skill explicitly excludes standalone planning.",
      "path": "tests/fixtures/coding_workflow_evals.json",
      "line": 630,
      "acceptance_criterion": "Architecture evaluation fixture remains consistent with planning-only scope",
      "remediation": "Request implementation explicitly in this positive case; retain the separate planning-only negative case.",
      "verification": "Parse the fixture and inspect positive/negative requests and expected routes.",
      "confidence": "high"
    }
  ],
  "resolved_findings": [],
  "executor_feedback": {
    "priority_order": [
      "architecture-eval-implementation-intent"
    ],
    "recommended_checks": [
      "Inspect positive/negative intent and parse fixture"
    ],
    "avoid": []
  },
  "residual_risks": [
    "Live model evaluation remains unrun."
  ],
  "learning_candidates": []
}
```
---

## 2026-09-24 - US-003 targeted self-review and finalization

- Same self-review context, expanded-initial, targeted; one initial and one targeted pass consumed. Accepted_fixed architecture-eval-implementation-intent. Inspected only fixture remediation and its routing implications; no regressions found.

```json
{
  "verdict": "pass",
  "pass_type": "targeted",
  "findings": [],
  "resolved_findings": [
    {
      "id": "architecture-eval-implementation-intent",
      "evidence": "Staged positive request now explicitly says Implement; existing planning-only negative case is unchanged. Fixture parses and all 3 bundle tests pass."
    }
  ],
  "executor_feedback": {
    "priority_order": [],
    "recommended_checks": [],
    "avoid": []
  },
  "residual_risks": [
    "Model behavior remains unrun."
  ],
  "learning_candidates": []
}
```

- No reusable memory promotion for this local wording correction. All US-003 criteria satisfied. Typecheck/formatter unavailable as recorded. Final branch/staged consistency and diff checks required before commit.
- Commit status pending; intended feat(US-003): add conditional architecture decision guidance.
---

## 2026-09-24 - US-004 candidate

- Reworked review-code discovery/root and added four bundled scopes: local, PR/branch/release, existing component, bounded audit. Findings distinguish attribution, evidence and optional simplifications; review forbids execution/mutation/posting. Dedicated staged/PR/feedback owners remain separate.
- Added isolated review-copy resource test. Before implementation 1/4 tests failed for absent scope links; after implementation all 4 pass. Existing evaluation fixture already covers each scope, missing evidence, injection, security and release variants; no model results fabricated.
- Checks: python3.11 -m unittest discover -s tests -p 'coding_workflow_contract_test.py' passed 4; make validate-ai passed; python3.11 tests/story_execution_test.py passed 11; python3.11 tests/story_blocker_test.py passed 6; bash tests/ralph_review_test.sh passed; git diff --check passed. Typecheck unavailable; no configured Markdown/Python formatter. Browser not applicable. Optional PyYAML helper limitation remains, no installation.
- Runtime: Codex desktop, standard mode, CodexGoalMarkdown; exact model/source and iteration limit unknown. No advisors. Native review required for test-sensitive routing/scope change: story-reviewer, expanded-initial, initial, attempt 1. No staged protocol/role permission changes.
- Intended commit feat(US-004): establish independent review scopes and evidence contract. Commit status pending; execution/commit authorization retained.
---

## 2026-09-24 - US-004 finalization

- Native role story-reviewer; returned session handle `/root/review_us004_attempt1`, same worktree, US-004 attempt 1. Full protocol/schema supplied; expanded-initial initial pass consumed, targeted unused. Reviewer inspected staged evidence and returned schema-valid pass.

```json
{
  "verdict": "pass",
  "pass_type": "initial",
  "findings": [],
  "resolved_findings": [],
  "executor_feedback": {
    "priority_order": [],
    "recommended_checks": [],
    "avoid": []
  },
  "residual_risks": [
    "Model evaluations are deferred to US-011 and are not claimed for this candidate."
  ],
  "learning_candidates": []
}
```

- No findings or memory promotion. All story criteria met; typecheck/formatter and live evaluation limits retained. Existing execution/commit authority applies.
- Commit status pending; intended feat(US-004): establish independent review scopes and evidence contract.
---

## 2026-09-24 - US-005 candidate

- Added conditional architecture/maintainability, compatibility and testing-quality lenses; root links by actual risk trigger. Covers semantic/cognitive/control-flow/state/coupling complexity, project metric limits, preserved interfaces/errors/lifecycle and meaningful test adequacy. No scope, role permission or executable-tool changes.
- Added unrun mock-only review scenario; existing interface/complexity/replacement cases cover other counterexamples. JSON parsed by construction; live evaluations remain pending.
- Checks: coding_workflow_contract_test passed 4 (isolated bundle and link checks include new references); make validate-ai passed; git diff --check passed. Typecheck unavailable, no configured Markdown/JSON formatter; optional PyYAML validation still unavailable. No UI.
- Runtime Codex desktop, standard, CodexGoalMarkdown; exact model/source/iteration limit unknown. No advisors. Trivial documentation/declarative scope: self-review, expanded-initial, initial attempt 1; inspect all staged paths, not an independent review.
- Intended commit feat(US-005): add maintainability compatibility and testing lenses. Commit pending; existing execution/commit authorization applies.
---

## 2026-09-24 - US-005 finalization

- Self-review expanded-initial initial attempt 1 inspected inventory and all six staged paths; correctness/QA criteria met, no findings. Session not applicable; targeted unused; no memory promotion.

```json
{
  "verdict": "pass",
  "pass_type": "initial",
  "findings": [],
  "resolved_findings": [],
  "executor_feedback": {
    "priority_order": [],
    "recommended_checks": [],
    "avoid": []
  },
  "residual_risks": [
    "Source guidance and scenario specification only; live evaluation remains unrun."
  ],
  "learning_candidates": []
}
```

- Commit pending; intended feat(US-005): add maintainability compatibility and testing lenses. Required source/resource checks pass; typecheck/formatter unavailable as above.
---

## 2026-09-24 - US-006 candidate

- Added conditional security/privacy, data/state and reliability lens references. Covers input/authority/sink tracing, sensitive-data lifecycle, transactional/concurrent invariants, precision, evolution, retries, idempotency, cancellation, cleanup and recovery. These are read-only inspection questions, not changed authorization or security enforcement.
- Existing security-pr, bounded-audit, retry-cancellation and embedded-instructions scenarios specify evidence and no-mutation expectations; model runs remain unrun. No role metadata, production logic, infrastructure or executable tests changed.
- Checks: coding_workflow_contract_test passed 4; make validate-ai passed; git diff --check passed. Root links and every bundled local reference checked from isolated copy. Typecheck unavailable; no configured Markdown formatter; optional PyYAML helper unavailable. No browser scope.
- Runtime Codex desktop, standard, CodexGoalMarkdown; exact model/source/iteration limit unknown. No advisors. Review: self for trivial documentation-only conditional references, expanded-initial initial attempt 1, no independent review claim. Security topics do not themselves authorize operations.
- Intended commit feat(US-006): add security state and reliability review lenses; pending. Existing execution/commit authorization retained.
---

## 2026-09-24 - US-006 finalization

- Self-review expanded-initial initial attempt 1 inspected inventory and all five staged files against scope; no findings. Session not applicable, targeted unused, no memory promotion.

```json
{
  "verdict": "pass",
  "pass_type": "initial",
  "findings": [],
  "resolved_findings": [],
  "executor_feedback": {
    "priority_order": [],
    "recommended_checks": [],
    "avoid": []
  },
  "residual_risks": [
    "Static review guidance does not prove enforcement or live review behavior."
  ],
  "learning_candidates": []
}
```

- All US-006 criteria satisfied by references, conditional routing, existing no-mutation scenario specifications and passing source/resource checks. Commit pending; intended feat(US-006): add security state and reliability review lenses. Typecheck and formatter unavailable.
---

## 2026-09-24 - US-007 candidate

- Added conditional performance, accessibility and operability/dependency lenses. Covers workload/query/resource costs, semantics/focus/errors, evidence limits, diagnostics/configuration/shutdown, rollout/rollback, provenance/packaging and reproducibility; no automatic tools, installs or delegation.
- Existing performance-accessibility and missing-tools scenarios specify source/runtime/browser provenance gaps; no live results added. Root routes all nine lenses independently by actual risk surface.
- Checks: coding_workflow_contract_test passed 4 including copied reference closure; make validate-ai passed; git diff --check passed. Typecheck unavailable; no configured Markdown formatter. Optional PyYAML limitation unchanged. No product UI or browser check required for these instructions.
- Runtime Codex desktop, standard, CodexGoalMarkdown; exact model/source/iteration limit unknown. No advisors. Self-review chosen for trivial documentation-only references; expanded-initial initial attempt 1. Existing root read-only scope preserved, no permission/protocol/tool code modified.
- Intended commit feat(US-007): add performance accessibility and operations lenses; pending under existing authority.
---

## 2026-09-24 - US-007 finalization

- Self-review expanded-initial initial attempt 1 inspected inventory and all five staged paths; all scope criteria met, no findings. Session not applicable; targeted unused; no memory promotion.

```json
{
  "verdict": "pass",
  "pass_type": "initial",
  "findings": [],
  "resolved_findings": [],
  "executor_feedback": {
    "priority_order": [],
    "recommended_checks": [],
    "avoid": []
  },
  "residual_risks": [
    "No measured workload, rendered UI or operational behavior was evaluated by these source checks."
  ],
  "learning_candidates": []
}
```

- Source/resource checks passed, typecheck/formatter unavailable. Commit pending; intended feat(US-007): add performance accessibility and operations lenses.
---

## 2026-09-24 - US-008 candidate

- Added standalone docs/templates/code-repository-AGENTS.md with verified-fact/command placeholders, manual merge/adoption and mixed-purpose scope, principles/contracts, feature/fix/refactor methods, verification/review/handoff. No personal skill dependency in template.
- Replaced detailed Coding Standards/Testing sections of source ai/AGENTS.md with concise cross-domain scope/truthfulness and advertised-skill routing; relocated all 18 mapped obligations to template and development references. Added source-backed reconciliation table in docs/coding-workflow-design.md.
- Checks: python3.11 -m unittest discover -s tests -p 'ai_install_test.py' passed 35 (isolated fixture/fake-CLI installation contracts, no global installation); make validate-ai passed; git diff --check passed. Inline parsed section comparison verified Communication Style, Git Workflow, Boundaries and Tool Usage byte-identical to immutable baseline; local design links resolve.
- No new executable behavior or spelling tests. Existing installation suite establishes byte-copy behavior for source policy. Typecheck unavailable; no configured Markdown formatter. No UI. Optional PyYAML helper limitation unchanged; no dependencies installed.
- Runtime Codex desktop, standard, CodexGoalMarkdown; exact model/source/iteration limit unknown. Advisors none. Native review selected for cross-file personal-policy obligation relocation, expanded-initial initial attempt 1; source only, no global installation or authorization-rule weakening.
- Intended commit feat(US-008): publish portable project guidance and refine personal policy; pending under existing execution/commit authority.
---

## 2026-09-24 - US-008 initial review and remediation

- Native role story-reviewer, runtime session `/root/review_us008_attempt1`; expanded-initial initial attempt 1. Complete schema-valid response:

```json
{
  "verdict": "changes_requested",
  "pass_type": "initial",
  "findings": [
    {
      "id": "code-repository-template-fix-test-first",
      "severity": "medium",
      "lens": "correctness",
      "title": "Require a failing regression before bug fixes",
      "body": "The template\u2019s \u201cNew behavior\u201d guidance requires a meaningful failing test before implementation, but its separate \u201cFixes\u201d guidance only says to connect causal evidence to a sensitive regression and the repair. A project adopting this standalone template could miss the mapped T-01 requirement to establish that the regression fails for the defect before implementing a fix.",
      "path": "docs/templates/code-repository-AGENTS.md",
      "line": null,
      "acceptance_criterion": "Relocate all coding-specific personal-policy obligations using the docs/coding-workflow-design.md map.",
      "remediation": "In the Fixes guidance, explicitly require adding a meaningful regression reproducing the confirmed defect before implementation and confirming it fails for the intended reason.",
      "verification": "Inspect the template\u2019s fix guidance and confirm it states the regression must fail for the intended reason before the repair; ensure the reconciliation table still maps T-01 to this guidance.",
      "confidence": "high"
    }
  ],
  "resolved_findings": [],
  "executor_feedback": {
    "priority_order": [
      "code-repository-template-fix-test-first"
    ],
    "recommended_checks": [
      "Inspect the revised template fix guidance and T-01 reconciliation."
    ],
    "avoid": [
      "Do not broaden the change into unrelated template or personal-policy edits."
    ]
  },
  "residual_risks": [],
  "learning_candidates": []
}
```

- Disposition accepted_fixed: template fix method now explicitly requires a meaningful regression before implementation and confirmation of intended failure. T-01 mapping remains intact. Only the reported wording gap changed; existing-work/test-order preservation still applies.
- Verification: inspected changed fix guidance and T-01 row, make validate-ai and git diff --check passed. Initial consumed; targeted follow-up in same actual session next.
---

## 2026-09-24 - US-008 finalization

- Same actual native session `/root/review_us008_attempt1`, story-reviewer, expanded-initial targeted attempt 1; initial and targeted consumed. Schema-valid pass resolves the sole finding.

```json
{
  "verdict": "pass",
  "pass_type": "targeted",
  "findings": [],
  "resolved_findings": [
    {
      "id": "code-repository-template-fix-test-first",
      "evidence": "The staged Fixes guidance now requires adding a meaningful regression before implementation and confirming it fails for the intended reason. The previously reviewed T-01 reconciliation maps the template\u2019s fix guidance to that obligation. The remediation preserves the surrounding regression and symptom-handling guidance."
    }
  ],
  "executor_feedback": {
    "priority_order": [],
    "recommended_checks": [],
    "avoid": []
  },
  "residual_risks": [],
  "learning_candidates": []
}
```

- Accepted fix verifies the standalone template explicitly retains failing-before-fix behavior, not just a cross-reference. Promoted bounded memory pattern `standalone-policy-obligation-parity`; event key `coding-workflows-and-review-architecture|US-008|standalone-policy-obligation-parity|code-repository-template-fix-test-first|accepted_fixed`, counted once. No suppression.
- All US-008 criteria met; existing checks and unavailable typecheck/formatter recorded above. Commit pending; intended feat(US-008): publish portable project guidance and refine personal policy.
---

## 2026-09-24 - US-009 candidate

- Individually revised six native role descriptions/bodies: prompt-engineer progressive disclosure/discovery/evaluation; architect-reviewer conditional evidence-based design; code-reviewer independent scope/attribution and dedicated-gate isolation; refactoring-specialist contract preservation without universal gains or implicit commits; debugger causal evidence and diagnosis-only boundaries; test-automator existing-system adequacy without framework/ROI mandates. Conditional domain expertise retained.
- docs/agent-authoring.md documents role ownership and bounded follow-up candidates from inspected backend/frontend/QA/fullstack descriptions; no broad role edits.
- Parsed TOML comparison before/after verified all native fields except description/developer_instructions unchanged. Checks: python3.11 tests/agent_contract_test.py passed 20; render-agents.py --harness opencode --check and --harness codex --check each reported 128 sources/rendered, 0 writes; make validate-ai passed; git diff --check passed.
- Documentation/TOML prose change, no new executable behavior. Typecheck unavailable; no configured TOML/Markdown formatter found. No installed copies changed or UI checks needed. Optional PyYAML limitation unchanged.
- Runtime Codex desktop, standard, CodexGoalMarkdown; exact model/source/iteration limit unknown. Optional architect advisor skipped: inspected targeted sources directly. Native staged review for cross-role contract alignment, expanded-initial initial attempt 1. Existing memory contains one validated standalone-policy parity pattern; no suppression.
- Intended commit feat(US-009): align specialist roles with scoped coding methods; pending under existing execution/commit authority.
---

## 2026-09-24 - US-009 finalization

- Native story-reviewer session `/root/review_us009_attempt1`, same worktree/story/attempt, expanded-initial initial. Complete supplied protocol; schema-valid pass, no findings. Initial consumed, targeted unused; memory unchanged.

```json
{
  "verdict": "pass",
  "pass_type": "initial",
  "findings": [],
  "resolved_findings": [],
  "executor_feedback": {
    "priority_order": [],
    "recommended_checks": [],
    "avoid": []
  },
  "residual_risks": [
    "Reported static checks do not establish runtime role-routing behavior; the packet records that no live evaluations were performed."
  ],
  "learning_candidates": []
}
```

- All US-009 criteria met. Typecheck/formatter unavailable, no live routing claims. Commit pending; intended feat(US-009): align specialist roles with scoped coding methods.
---

## 2026-09-24 - US-010 candidate

- Generalized run-tests and format-code entry discovery to project-native tools across languages, retaining conditional existing adapters. Both preserve caller scope, unavailable-tool reporting, and independent review boundaries.
- Added an optional advertised develop-code method handoff after executor guards. Executor retains all state, authorization, review, recovery, and finalization ownership. Removing the inserted paragraph reproduces HEAD's execution reference byte-for-byte; no existing protocol text changed.
- Inventoried remaining old development identifiers: only superseded skill trees and docs/ai-configuration.md inventory remain, intentionally deferred to approved US-012 retirement.
- Passed: story_execution_test.py (11), story_blocker_test.py (6), ralph_review_test.sh, coding_workflow_contract_test.py (4), make validate-ai, git diff --check, isolated helper resource-link closure, and exact execution-contract comparison.
- Broader regression: TMPDIR="$PWD/tests" SKILL_TEST_PYTHON=/Users/corysiebler/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 python3.11 -m unittest discover -s tests -p '*test*.py' ran 261 tests in 71.463 seconds, exit 1, seven failures and one skip. Five create_skill_test cases and two document_skills_contract_test checks fail because PyYAML is unavailable (helper exit 3). These test/helper sources are unchanged from the prepared baseline; docs/create-mcp-server-verification.md already records the same missing dependency. No install performed. This is not a passing full-suite claim. Skip reason not captured by the nonverbose run.
- No standalone typecheck or configured Markdown formatter. Prose-only edits use existing protocol/source/resource checks. No browser/UI work, live model evaluations, or installed-copy changes.
- Runtime Codex desktop, standard, CodexGoalMarkdown; exact model/source/iteration limit unknown. No advisor. Native staged story-reviewer required for execution handoff, expanded-initial initial attempt 1, with existing standalone-policy parity memory and no suppressions.
- Intended commit feat(US-010): integrate coding helpers and execution handoff, under existing execution/commit authority; pending review and finalization.

## 2026-09-24 - US-010 finalization

- Native story-reviewer session `/root/review_us010_attempt1`, expanded-initial initial, attempt 1, received the complete installed protocol and returned schema-valid pass. Initial consumed, targeted unused. No memory change.

```json
{
  "verdict": "pass",
  "pass_type": "initial",
  "findings": [],
  "resolved_findings": [],
  "executor_feedback": {
    "priority_order": [],
    "recommended_checks": [],
    "avoid": ["Keep follow-up review scoped to this handoff and the two helper routing changes."]
  },
  "residual_risks": [
    "A typecheck and Markdown formatter were unavailable; the packet reports the focused protocol and common checks passed.",
    "The broad suite had seven failures attributed to missing PyYAML in an unchanged helper and tests; this does not establish a regression in the reviewed scope."
  ],
  "learning_candidates": []
}
```

- US-010 changed-contract criteria passed; broad baseline environment limitation remains explicit. Provisional completion under existing commit authority. Intended feat(US-010): integrate coding helpers and execution handoff. Separate untracked US-011 proposal is excluded from this story commit.

## 2026-09-24 - US-011 preparation and authorization checkpoint

- US-010 commit succeeded: 305226d. US-001 through US-010 now delivered on the recorded prepared branch. PLAN completion markers reflect ten completed stories.
- Prepared docs/coding-workflow-verification.md with actual source evidence, broad-suite limitations and a concrete proposed comparative evaluation scope. Verified document links, all 38 baseline SHA-256 hashes against a6c3b8f, 27 unrun scenarios and empty observed results. Six visible reserved cases are not blind holdouts.
- Proposal: native fresh Codex subagents, gpt-6-sol medium, one run per variant for each of 27 scenarios, maximum 54 sessions, at most two concurrently, no further delegation or independent model graders; parent evidence grading. Existing account usage only, no paid external services. Behavioral per-session limits are not a hard token/dollar cap. No launch until user agrees runtime/model, scope and thresholds.
- Candidate evaluation catalog would omit old development entries only in project-local evaluation copies; repository trees retained. Ambient installed skill/context contamination must be checked and prevents claims of isolated/native installed discovery. Required unavailable capabilities remain incomplete; no simulated gate success.
- US-011 remains pending, no staged review or story commit attempted. The proposal is an uncommitted preparation artifact; journal checkpoint is also uncommitted. No live model evaluations/results fabricated. US-012 remains dependent on US-011 and exact source-tree deletion approval. Activation remains separately authorized.
- User execution and story-commit authority is preserved. Remaining decision is evaluation scope, not repeat implementation/commit permission. PLAN US-011 explicitly requires agreed runtime/model, repetitions, held-out cases, grading criteria and spending/delegation scope before live runs.

## US-011 user scope revision and closure

- User explicitly requested: "Mark as complete and proceed to US-012" after being told that US-011 is the evaluation gate and could lead to fixes. This waives live comparative evaluation for delivery; it does not authorize fabricated passing results. PLAN and PRD record this revision; 27 scenarios remain unrun and results empty.
- The continuation authorizes US-012's specifically listed implement-feature, develop-with-tests and refactor-code source-tree removals. No installed cleanup or activation authorized.
- US-011 changes are documentation/evidence bookkeeping only. Standard mode trivial self-review, CodexGoalMarkdown expanded-initial initial, no native session needed. Reviewed staged-intended diff for scope and honest provenance. make validate-ai and git diff --check passed. Typecheck/formatter unavailable as previously recorded. No live evaluations or new dependency install. No memory changes.

```json
{"verdict":"pass","pass_type":"initial","findings":[],"resolved_findings":[],"executor_feedback":{"priority_order":[],"recommended_checks":[],"avoid":[]},"residual_risks":["Live model behavior remains unevaluated under explicit user waiver; closure is not a passing evaluation."],"learning_candidates":[]}
```

- Intended commit docs(US-011): record user waiver of live evaluations. Completion marker means administratively closed under revised scope. Commit pending under existing authority; US-012 next.
