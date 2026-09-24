# PRD: Coding Workflows, Review Architecture, and Project Guidance

Date: 2026-09-24

Status: Draft requirements synthesized from the agreed design discussion.
Saving this document does not authorize implementation, source deletion,
installation, external operations, or commits. Proposed details and unresolved
evaluation choices are identified below.

Base branch: `main`. The preceding producing-and-document-skills pull request
from `feat/producing-and-document-skills` has been merged into `main`, as confirmed
by the user. Prepare this revision against the current `main` baseline, not the
previous feature branch. The implementation branch remains to be selected and
prepared before execution; `main` is the base, not an authorized execution branch.

## 1. Overview

Revise the Craft coding plugin and relevant native agents to provide consistent,
evidence-driven engineering without imposing coding procedures on unrelated AI
work such as research, image generation, or creative writing.

Consolidate `implement-feature`, `develop-with-tests`, and `refactor-code` into
`develop-code`. Retain `review-code` as an independently discoverable, read-only
workflow. Organize review guidance by scope and conditional lenses. Provide a
portable project-level `AGENTS.md` example and reduce detailed coding guidance
in the personal policy without weakening authorization or safety boundaries.

The existing skills already contain useful test-first, characterization,
compatibility, and evidence requirements. Their inspected references do not
establish a circular dependency. The problem is overlapping lifecycle ownership,
incomplete task routing, and uneven guidance across skills and specialist roles.

The design adapts Ponytail's comprehension-first and reuse-first principles,
but rejects line count as a quality objective, fixed test-count limits, and
simplification that silently removes requested functionality.

## 2. Users and goals

Primary user: a developer using Codex and OpenCode for both engineering and
non-engineering tasks across new and existing repositories.

Goals:

- Make implementation and assessment independently discoverable by user intent.
- Establish clear ownership of standards, methods, expertise, and orchestration.
- Preserve meaningful testing and verification across features, fixes, refactors,
  and reviews while selecting detail proportionally to affected risks.
- Make architecture principles actionable without mandatory design ceremony.
- Keep personal policy concise and useful across domains.
- Make project guidance portable to agents without the Craft marketplace.
- Preserve existing native permissions, staged-review contracts, and installation
  safeguards during migration.
- Evaluate actual routing and work quality rather than claiming that shorter
  prompts or fewer skills necessarily improve results.

## 3. Agreed design and ownership

| Layer | Owns |
| --- | --- |
| `ai/AGENTS.md` | Cross-domain communication, truthful evidence, user-work preservation, authority boundaries, concise task routing |
| Project `AGENTS.md` | Applicable engineering expectations, verified project facts, commands, architectural constraints, documentation links |
| `develop-code` | Feature, diagnosis/fix, refactor, and cross-cutting testing methods |
| `review-code` | Read-only assessment, scope selection, conditional lenses, findings and coverage reporting |
| Canonical native agent TOMLs | Domain expertise, role-specific restrictions, bounded handoffs |
| Existing operational skills | Tests, formatting, interface verification, feedback disposition, Git delivery, and other distinct capabilities |
| Existing execution/review protocols | Planning formats, story state, review schemas, sessions, budgets, recovery, and delivery gates |

The two coding skills must be independently useful. Neither loads the other as
a prerequisite. A small shared baseline may appear in both entry points; detailed
procedures have one owner. Do not add a mandatory third standards skill or assume
that separately installed bundles can resolve sibling or plugin-root resources.

Discovery instructions are behavioral guidance, not automatic loading guarantees
or permission enforcement. Delegated agents must receive relevant task context;
parent skill-loading output must not be assumed to reach them.

## 4. Functional requirements

### FR-1: Development entry point and actions

Create `ai/plugins/coding/skills/develop-code/` with an action-oriented description
covering implementation, bug diagnosis/fixing, and behavior-preserving refactoring.
Exclude ordinary conceptual explanations, requirements drafting, and standalone
planning from automatic implementation routing.

The root selects scope and authority before any edit or command, then follows:
understand contracts, classify the action and risks, establish evidence, implement
or diagnose, verify, and report. Diagnosis-only and planning-only requests remain
non-mutating. Mixed tasks distinguish intended behavior changes from refactoring.

Use bundled references for feature, bugfix, refactor, testing strategy, testing
anti-patterns, and conditional architecture decisions. Load only applicable
references relative to the advertised installed skill location.

### FR-2: Engineering and architectural reasoning

Preserve requested requirements and understand affected callers, behavior, and
constraints before choosing a solution. Prefer suitable project reuse, standard
library, native platform/framework capabilities, installed dependencies, then
minimal cohesive custom code. This order does not mandate replacing working code
or authorize adding dependencies.

Evaluate correctness, maintainability, compatibility, failure behavior, and
lifecycle rather than fewest files or lines. Preserve validation, security,
accessibility, and data-loss prevention appropriate to the affected behavior.

Explain theory through decision questions: cohesion and information hiding,
coupling and dependency direction, duplicated knowledge versus accidental
similarity, contracts and substitutability, state invariants, algorithmic costs,
and reversibility. Patterns such as CQRS, DDD, services, or dependency injection
are conditional tools, not default outcomes.

Use deeper architecture guidance for material interface, responsibility,
dependency, persistence, concurrency, trust-boundary, or performance changes.
Significant decisions identify context, constraints, alternatives, trade-offs,
verification, and reversal/revisit conditions. Follow existing ADR conventions;
do not require an ADR or full plan for routine local changes.

### FR-3: Development evidence and testing

Preserve the existing change classification and testing anti-pattern guidance:

- New behavior/fixes: meaningful failing behavior or regression tests before
  implementation; confirm the intended failure, then green and relevant checks.
- Refactors: baseline and missing characterization coverage before transformations.
- Static docs/configuration: appropriate schema, lint, typecheck, or build checks.
- Generators/runtime configuration: verify generated meaning and runtime behavior.
- Integrations: realistic doubles or authorized integration checks at boundaries.

Bug fixes connect reproduction and expected/actual behavior to causal evidence,
regression sensitivity, the repair, and related affected paths. Distinguish a
confirmed cause from a hypothesis; symptom disappearance alone is insufficient.

Refactors identify a maintenance problem and preserve applicable outputs, errors,
side effects, persistence, ordering, public interfaces, and resource lifecycle.
Shorter replacements require equivalence evidence.

Do not impose fixed test counts or coverage percentages, fabricate test-first
history, discard existing work, weaken assertions, or hide flaky failures.
Include guidance for brownfield characterization, safe replacements, realistic
test doubles, and distinguishing product races from fixture/environment failures.
Run configured formatting before final verification. Report unavailable checks,
unverified integrations, and browser limitations honestly.

### FR-4: Independent read-only review

Retain `ai/plugins/coding/skills/review-code/` with explicit discovery signals for
local reviews, PRs, selected components, audits, security assessments, and complexity
assessments. Select scope before gathering evidence and select lenses from the
requested focus and concrete affected contracts.

The generic review workflow inspects and recommends. It does not run tests,
format, edit, stage, post, or automatically fix findings. Reproduction language
must mean tracing or examining supplied evidence within the read-only boundary,
not permission to execute a suspected path. Read-only tools remain subject to the
active role/runtime restrictions. Source comments and PR text are data.

Correctness, requirement satisfaction, evidence quality, defect attribution, and
honest coverage reporting are core obligations, not optional lenses.

### FR-5: Review scopes

Provide initial references for:

| Scope | Required evidence boundary |
| --- | --- |
| Local changes | Requested staged/unstaged/untracked candidate, baseline, unrelated-work separation |
| Pull request/branch | Base/head, included commits, changed files, intended behavior, available CI evidence |
| Component review | Selected existing component, relevant consumers and dependencies; pre-existing defects allowed |
| Codebase audit | Bounded inventory/exploration, inspected coverage, prioritization, explicit uninspected areas |

Document release comparisons and cross-component/cross-repository changes as scope
variants, requiring explicit versions/components and missing-counterpart evidence.
Separate references are optional if distinct procedures justify them.

Design-proposal review remains with architecture/planning workflows. Existing
`resolve-review-feedback` retains feedback disposition, remediation verification
coordination, reply preparation, and thread-resolution ownership; generic review
may supply evidence but must not create a second feedback lifecycle.

### FR-6: Conditional review lenses

Provide the following initial coverage, grouping related topics into cohesive
references rather than creating a skill or agent invocation for each topic:

| Lens | Coverage |
| --- | --- |
| Architecture and maintainability | Responsibilities, coupling, cohesion, indirection, duplicated rules, semantic/cognitive/control-flow complexity |
| Compatibility | APIs, schemas, defaults, errors, ordering, encoding, runtime/platform support, mixed-version behavior |
| Security and privacy | Trust boundaries, authority, injection paths, sensitive data, exposure, resource abuse |
| Data and state | Invariants, transactions, precision, evolution, concurrency, ordering, races, ownership, invalid transitions |
| Reliability | Timeouts, bounded retries, idempotency, cancellation, cleanup, partial failure, recovery |
| Performance | Relevant workloads, query counts, algorithmic cost, blocking operations, memory and resource growth |
| Testing quality | Behavior coverage, meaningful assertions, doubles, isolation, regression sensitivity, flakiness |
| Accessibility | Semantics, keyboard/focus behavior, assistive technology, error states, supplied rendered evidence |
| Operability and dependencies | Diagnostics, health/shutdown behavior, configuration, rollout/rollback, dependency suitability, packaging and reproducibility |

Treat internationalization, time zones, caching, licensing concerns, configuration,
logging, and documentation as applicable subtopics. Do not invent legal conclusions
or claim live behavior from static inspection. Active security testing, operational
changes, and deployment are not authorized by loading a lens.

Cyclomatic complexity is a diagnostic within maintainability, not a standalone
quality gate. Explain its control-flow focus and tool-dependent counting; it does
not determine a sufficient test count or prove understandability. Cognitive,
semantic, state, and coupling concerns supplement it. Report only actual measured
scores; respect configured checks while distinguishing metric violations from
evidenced defects. Do not game scores through arbitrary extraction.

### FR-7: Findings and review outcomes

Separate defects from optional simplifications. Defects include verified location,
severity, violated contract, triggering condition, impact, evidence, practical
remediation, and expected verification. Attribute issues as introduced, exposed,
pre-existing, or unresolved as appropriate to scope; deduplicate root causes.

Simplifications identify concrete maintenance cost, affected consumers, proposed
change, preserved contracts, trade-offs, verification, and benefit/risk priority.
Single-implementation interfaces and single-export files are investigation leads,
not automatic findings. Optional improvements do not automatically block delivery.

Report reviewed scope, evidence provenance, gaps, and open questions. No findings
does not establish correctness or permission to ship. Honor caller-supplied formats;
do not impose a new universal JSON schema on existing review protocols.

### FR-8: Personal policy and project template

Map every coding-specific obligation in `ai/AGENTS.md` to its future owner before
editing. Keep cross-domain communication, truthfulness, privacy, preservation,
authority, and applicable operation-specific restrictions globally. Move detailed
engineering procedures and architectural opinions to coding workflows and project
guidance. Retain only concise coding-task routing to available advertised skills.
Missing required skills are reported rather than silently claimed as applied.

Create `docs/templates/code-repository-AGENTS.md` as a portable example, not an
automatically installed policy. Include engineering principles, contracts,
feature/fix/refactor expectations, risk-based verification, review expectations,
handoff requirements, and clearly marked project placeholders for purpose, stack,
boundaries, compatibility, documentation, and verified commands.

The example must remain useful without Craft or personal skill names. Explain
new-project customization and existing-project merge/adoption. Preserve local
rules, link existing guides, remove inapplicable sections, and scope instructions
for mixed-purpose repositories. Do not blindly overwrite or synchronize projects.

### FR-9: Targeted native-agent alignment

Revise the canonical TOML bodies of `prompt-engineer`, `architect-reviewer`,
`code-reviewer`, `refactoring-specialist`, `debugger`, and `test-automator` for their
relevant responsibilities. Use actual source inspection to select edits, not a
uniform replacement template.

Focus on progressive disclosure/evaluation, evidence-driven architecture, review
isolation, preservation-focused refactoring, causal debugging, and existing-system
test adequacy respectively. Remove universal improvement claims and implicit
authority to commit or build infrastructure. Keep useful conditional expertise.

Inspect representative coding-role descriptions for conflicting discovery cues;
document justified follow-up candidates rather than rewriting all 128 roles.
Keep agents independently useful and pass relevant constraints during delegation.
Do not introduce renderer includes, concatenation, overrides, or blanket skill
loading. Preserve native metadata, read-only policies, and byte/body preservation.

### FR-10: Preserve orchestration and focused capabilities

Keep `run-tests`, `format-code`, `verify-interface`, `resolve-review-feedback`,
`manage-changes`, `write-requirements`, `prepare-implementation`, `map-codebase`,
`recover-ralph`, `create-skill`, and `create-mcp-server` as distinct capabilities.
Broaden test/formatter descriptions and entry guidance beyond pytest/Vitest and
Python/JavaScript while retaining conditional adapters and repository-native tools.

The story execution owner may consume the development method, but the generic
skills must not start execution, create state, or call back into orchestration.
Preserve all prepared-branch/authorization guards, schemas, profiles, evidence
budgets, session identity, initial/targeted limits, blocker gates, journal/memory
ownership, recovery counters, and commit finalization rules.

Codex `story-reviewer` and native OpenCode `ralph-reviewer` remain the dedicated
staged reviewers with full supplied protocols. OpenCode `/review-pr` remains the
canonical owner of its orchestration and GitHub schema. General references explain
the boundary; they neither duplicate schemas nor substitute required reviewers.
Do not add another mandatory review cycle or automatic delegation per lens.

### FR-11: Migration and activation

Inventory all source consumers and identifiers before retiring the three old
skills. Preserve substantive testing guidance and update links, fixtures, skill
inventories, and relevant documentation. Explicitly approved source deletion is
required; do not leave permanent ambiguous wrappers without demonstrated need.

Keep the five plugin identities and native agent counts unchanged. Use existing
directory discovery and managed retirement instead of special-case installers.
Document activation/cleanup in README, repository AGENTS, configuration/authoring
guides, and removal guidance as applicable.

Installation, source retirement, model evaluation runs, and cleanup require their
applicable authorizations. Preview retirement effects, including shared-root
impact. Preserve customized, unverified, symlinked assets and rollback evidence.
Never hand-edit ownership inventories or delete plugin caches. Verify fresh-session
discovery and installed-relative references after separately authorized activation.

## 5. User stories and acceptance criteria

All stories use repository-native validation. This repository has no standalone
typecheck target: record that limitation explicitly, run relevant source/contract
validation, and do not claim typecheck passed. Run meaningful regression tests for
changed behavior; documentation-only work uses content/link/diff validation.
Configured formatters run before final checks when available. No UI is introduced
by this PRD; UI evaluation cases must require real browser evidence or disclose its
absence. Recommended agents are optional hints, not delegation authorization.

### US-001: Establish ownership and evaluation baseline

As a maintainer, I want a source-backed obligation/consumer inventory so migration
does not lose safeguards or duplicate workflow owners.

- [ ] Map current skill references and personal-policy obligations to new owners.
- [ ] Capture baseline discovery and behavior scenarios before changing instructions.
- [ ] Identify dedicated review invariants and affected validation fixtures.
- [ ] Validate paths and identifiers; apply the shared verification requirements.

### US-002: Consolidate development and testing methods

As a coding agent user, I want one development entry point that selects the correct
feature, bugfix, or refactor method.

- [ ] Implement FR-1 and FR-3 with independent, installed-relative references.
- [ ] Preserve testing anti-pattern substance and honest test-order reporting.
- [ ] Diagnosis-only, planning-only, and mixed behavior/refactor cases are explicit.
- [ ] Add relevant routing/reference checks and apply shared verification requirements.

### US-003: Add conditional architecture guidance

As a developer, I want design principles expressed as decisions so simpler work
does not trigger speculative architecture.

- [ ] Cover FR-2's reuse order, equivalence, theory questions, and decision triggers.
- [ ] Include useful-abstraction and unsafe-shorter-replacement counterexamples.
- [ ] Routine changes require neither ADRs nor unrelated redesign.
- [ ] Validate examples and references; apply shared verification requirements.

### US-004: Establish review routing, scopes, and findings

As a reviewer, I want independently discoverable assessment with explicit evidence
boundaries and no implementation side effects.

- [ ] Implement FR-4, FR-5, and FR-7 with four initial scope references.
- [ ] Document release/cross-component variants and feedback/design-review boundaries.
- [ ] Distinguish defects, optional simplifications, scope, and evidence gaps.
- [ ] Validate read-only and native-review exclusions; apply shared verification requirements.

### US-005: Add architecture, compatibility, and test review lenses

As a reviewer, I want to assess structural and verification risks without treating
metrics or stylistic preferences as defects.

- [ ] Add architecture/maintainability, compatibility, and testing-quality coverage.
- [ ] Include cyclomatic/cognitive/semantic limitations and behavior-equivalence evidence.
- [ ] Reject one-implementation deletion and fixed-test-count heuristics.
- [ ] Validate lens routing and counterexamples; apply shared verification requirements.

### US-006: Add security, data/state, and reliability lenses

As a reviewer, I want to trace protected assets, invariants, and failure transitions
without performing unauthorized operational testing.

- [ ] Cover FR-6 security/privacy, data/state, and reliability topics.
- [ ] Findings require relevant triggering paths and affected contracts.
- [ ] Active testing, migrations, and infrastructure changes remain outside review.
- [ ] Validate applicable boundaries and scenarios; apply shared verification requirements.

### US-007: Add performance, accessibility, and operational lenses

As a reviewer, I want resource, user-access, and operational concerns assessed with
accurate evidence limitations.

- [ ] Cover performance, accessibility, and operability/dependency topics in FR-6.
- [ ] Distinguish measured workloads and rendered evidence from source assumptions.
- [ ] No lens automatically invokes agents, installs tools, or changes services.
- [ ] Validate references and provenance expectations; apply shared verification requirements.

### US-008: Publish portable project guidance and slim personal policy

As a multi-domain agent user, I want coding guidance available in code repositories
without loading detailed engineering procedures into unrelated sessions.

- [ ] Create the FR-8 template with marked placeholders and verified-command guidance.
- [ ] Document new/existing/mixed-purpose repository adoption and preservation.
- [ ] Use US-001's map to relocate coding details without weakening global boundaries.
- [ ] Keep the template independent of Craft; preserve byte-identical personal-policy
  installation to both harnesses.
- [ ] Validate policy/template contents and installation contracts; apply shared
  verification requirements.

### US-009: Align targeted specialist roles

As a delegating agent user, I want specialists to reinforce the selected method
without introducing another lifecycle or mandatory architecture.

- [ ] Align the six FR-9 roles and document any further source-backed candidates.
- [ ] Preserve names, native settings, reviewer restrictions, and domain expertise.
- [ ] No universal performance gains, framework creation, or commit authority claims.
- [ ] Pass relevant rendering/body-preservation and contract tests; apply shared
  verification requirements.

### US-010: Integrate helpers and preserve execution protocols

As a user of both harnesses, I want the new methods to fit existing tools and story
execution without changing delivery gates.

- [ ] Generalize test/formatter entry guidance while retaining applicable adapters.
- [ ] Update actual callers without recursive skill loading or orchestration callbacks.
- [ ] Preserve all FR-10 staged/PR review invariants and dedicated reviewer ownership.
- [ ] Pass affected protocol/helper regression checks; apply shared verification requirements.

### US-011: Evaluate routing and engineering outcomes

As a maintainer, I want evidence that discovery and work quality improved or were
preserved before promoting the revised workflows.

- [ ] Implement the evaluation specification in Section 8, including held-out cases.
- [ ] Keep static contract results separate from authorized model-behavior results.
- [ ] Record actual provenance, findings, limitations, and unresolved evaluation gaps.
- [ ] Do not claim model validation or activation if unavailable or unauthorized.
- [ ] Apply shared verification requirements to evaluation tooling changes.

### US-012: Prepare source retirement and activation documentation

As a maintainer, I want a reversible migration without duplicate discoveries or
loss of customized assets.

- [ ] After explicit approval, retire only the three superseded source skill trees
  and reconcile consumers; keep `review-code` active.
- [ ] Update FR-11 documentation and relevant inventory/retirement tests.
- [ ] Document exact activation, fresh-session verification, cleanup, and rollback
  steps; executing them is separately authorized.
- [ ] Pass relevant source/installation/retirement checks and apply shared
  verification requirements. Record live activation as pending until performed.

## 6. Proposed file organization

```text
ai/plugins/coding/skills/develop-code/
  SKILL.md
  references/
    architecture-decisions.md
    testing-strategy.md
    testing-anti-patterns.md
    actions/{feature,bugfix,refactor}.md
ai/plugins/coding/skills/review-code/
  SKILL.md
  references/
    scopes/{local-changes,pull-request,component-review,codebase-audit}.md
    lenses/{architecture-and-maintainability,compatibility,testing-quality}.md
    lenses/{security-and-privacy,data-and-state,reliability}.md
    lenses/{performance,accessibility,operability-and-dependencies}.md
docs/templates/code-repository-AGENTS.md
```

Brace notation abbreviates separate files. Reference grouping is a proposed
implementation detail; preserve required coverage and conditional loading if
cohesion justifies a different split. Do not generate runtime prompt concatenation.

## 7. Non-goals and constraints

- No Ponytail installation, runtime mode flags, every-turn hooks, or intensity modes.
- No consolidation of `review-code` into `develop-code`.
- No global engineering handbook, required third standards skill, or blind project
  AGENTS replacement. No automated onboarding generator in this revision.
- No rewrite of all 128 agents, new agent collection, or renderer architecture.
- No new universal finding schema, review budget, permission policy, or autonomous
  review/implementation loop. Preserve stricter role restrictions.
- No automatic installs, dependency upgrades, commits, deployments, external posts,
  active security tests, or paid/bulk evaluations.
- No execution plan, journal, memory, archive, or runner state created by PRD drafting.
- No universal LOC, coverage, cyclomatic, latency, token, or cost success targets.
- AI-system-specific review guidance and separate new release/onboarding skills are
  future candidates, not required deliverables.

## 8. Verification and evaluation

### Structural and regression verification

Inspect existing test assertions before extending them. Relevant checks include
`make validate-ai`, `python3.11 tests/agent_contract_test.py`, affected unittest
suites under `tests/`, renderer checks for both harnesses, and
`bash tests/ralph_review_test.sh` when its contracts are affected. Select additional
existing story/installation/retirement regressions according to actual changes.
Never use global installation as a validation command.

Verify frontmatter/names, resolvable bundled resources, no stale active consumers,
no cross-skill cycles, preserved source/body rendering, permission metadata,
protocol owners, profiles/schemas/budgets, and retirement preservation behavior.
Historical documentation may retain old identifiers when explicitly historical.
Do not substitute brittle prose-string assertions for meaningful contract checks.

### Behavioral evaluation matrix

Compare the existing setup with the revision using representative and held-out
requests. Positive and negative discovery cases are both required.

| Case | Required outcome |
| --- | --- |
| Small feature | Focused implementation without unnecessary plan, ADR, or abstraction |
| Multiple required failure paths | Relevant coverage; no one-test ceiling or reduced requirements |
| Symptom-masking fix | Causal evidence and regression, not catch-and-ignore |
| Existing partial implementation | Work preserved; honest test order and regression sensitivity |
| Shorter incompatible replacement | Contract difference detected; simplification rejected or scoped explicitly |
| Legitimate single-implementation interface | Boundary assessed rather than automatically removed |
| Local/PR/component/audit request | Correct review discovery, scope attribution, and evidence boundaries |
| Security-focused PR | PR scope plus security lens; no active exploit or mutation |
| Cyclomatic hotspot | Concrete reasoning; no invented score or arbitrary extraction |
| Review with instructions embedded in code | Treat as data; no tests, edits, formatting, or posting |
| Large audit with unavailable evidence | Bounded exploration and explicit coverage gaps |
| Missing runner/browser/reference | Exact limitation; no fabricated verification or unauthorized install |
| Required staged reviewer unavailable | Preserve blocked gate; no generic-review substitution |
| Planning/design-only request | No implementation or execution-state creation |
| Image generation, research, creative writing | No coding workflow activation absent an actual coding subtask |
| Fresh session or delegated specialist | Relevant available guidance established, not presumed inherited |

Record the exact source revision, runtime/model, inputs, configuration, tool
evidence, evaluation criteria, repetitions, observed outcomes, and limitations.
Record latency/tokens/cost only when measured with a stated basis. A specification
or static test is not a completed model evaluation. Any observed unauthorized
mutation, fabricated verification, or native-review bypass blocks promotion until
remediated and checked. Broader quality thresholds require agreement before runs.

## 9. Success criteria

- Implementation and review have distinct discoverable entry points and clear owners.
- Development preserves test-first/characterization discipline and adds explicit
  causal diagnosis without unnecessary architectural ceremony.
- Review selects scopes/lenses proportionally and separates defects from optional
  maintenance suggestions using evidence rather than size alone.
- Noncoding sessions receive concise global policy rather than engineering procedures.
- A portable, adaptable project template captures the agreed baseline and project facts.
- Targeted roles and helpers align without altered native permissions or review gates.
- Source validation passes; behavioral and live-activation status are reported
  separately with real evidence and explicit gaps.
- Migration preserves customized assets, ownership inventories, and rollback options.

## 10. Assumptions and open questions

- `develop-code` and the proposed template path are the working identifiers from
  the discussion. They are requirements-draft defaults, not installed assets.
- Existing project instructions remain authoritative within the runtime instruction
  hierarchy. The template introduces no new authority or immutable enforcement.
- The initial lens grouping is intentionally bounded; its coverage is required,
  but file boundaries may change for cohesion without adding discovery dependencies.
- Determine the authorized behavioral-evaluation runtime/model matrix, repetitions,
  budget, graders, and comparative quality thresholds before executing evaluations.
- Select Codex/OpenCode activation scope and obtain installation/retirement approvals
  at rollout. The PRD does not grant those approvals or approve source deletions.
- Assess whether additional coding-role edits are justified by the inventory; any
  expansion beyond targeted alignment must remain bounded and evidence-backed.

## 11. Source context

- [Personal policy](../ai/AGENTS.md)
- [Coding plugin](../ai/plugins/coding/)
- [Canonical native agents](../ai/codex/agents/)
- [Agent authoring and rendering](../docs/agent-authoring.md)
- [AI configuration and installation](../docs/ai-configuration.md)
- [Installed-file removal guidance](../docs/remove-old-ai-files.md)
- [Shared story execution](../ai/plugins/coding/skills/prepare-implementation/references/story-execution.md)
- [Shared staged review](../ai/plugins/coding/skills/prepare-implementation/references/story-review.md)
- [OpenCode PR review](../ai/opencode/commands/review-pr.md)
- Ponytail research baseline: [revision e3ba2aa](https://github.com/DietrichGebert/ponytail/tree/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156).
  Principles are adapted, not installed. Preserve applicable attribution/license
  notices if implementation copies substantial upstream material.

Earlier read-only consultations with `prompt-engineer`, `architect-reviewer`, and
`code-reviewer` informed this draft. Their recommendations were advisory, not test
results. Later user decisions supersede the initial proposal to merge review into
development and the proposal to expand global coding policy.

## Approved scope revision

The user requested closing US-011 and proceeding to US-012 after the evaluation
implications were explained. Live comparative evaluations are waived for this
delivery; their unrun specifications are not observed results or evidence of
model quality. US-012 may proceed on source checks and staged review. Its three
listed source-tree removals are within the requested continuation. Installation
and post-install discovery remain separate, unauthorized operations.
