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
