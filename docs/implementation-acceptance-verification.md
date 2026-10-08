# Implementation acceptance coverage verification

## Scope

The 2026-10-07 revision strengthens prepare-implementation's planning handoff:
source acceptance coverage, observable outcomes, integration ownership, and a
coverage audit before delivery. Markdown and Ralph use their existing source
reference fields. No execution lifecycle, Ralph schema, PRD completion tracking,
installation, or commit behavior changes. write-requirements already requires
verifiable criteria and did not need modification.

The native prompt-engineer was consulted before editing and inspected the candidate.
The create-skill authoring, evaluation-schema, and validation guidance informed
the work. This is source delivery, not installed activation.

## Observed consultation exercises

Two candidate-only text exercises ran in the same prompt-engineer session through
Codex native delegation. They were non-blind, with no baseline comparison, project
implementation, real artifact generation, or full planning-harness execution.
Runtime model/token telemetry was not recorded. These observations do not establish
skill discovery accuracy or reliable execution across harnesses.

### A: split export acceptance

Source: tasks/prd-export.md US-1 requires exactly the filtered rows in displayed
order as CSV, a header-only file for no results, an inclusive maximum of 500 rows,
and explanatory rejection above 500. The request splits backend and UI stories.

The returned Markdown excerpt assigned backend work to US-001 and integrated
acceptance to dependent US-002. Its criteria included:

> When export is requested, the downloaded CSV contains exactly the rows matching
> the current filters, in their displayed order.

It also retained header-only output and accepted 500 rows while rejecting larger
exports with a user-facing explanation. The handoff mapped those outcomes to
US-1 and named US-002 as their integration owner. Parent inspection found the
specified outcomes covered; project commands and implementation remained unverified.

### B: ambiguous performance and reload persistence

Source: tasks/prd-draft.md FR-1 says draft edits survive reload; FR-2 says saving
should feel fast without defining observable acceptance. Cross-device sync is
explicitly excluded; storage is unspecified.

The first Ralph story excerpt correctly left speed unresolved, preserved the
exclusion, and chose neither storage nor a numeric target. However, it narrowed
FR-1 to saved edits and omitted the browser gate. Parent inspection rejected
that narrowing, despite the consultant's initial positive assessment. The shared
guidance was refined to prohibit added preconditions that weaken a source outcome.

A targeted repeat of B returned:

> After editing draft content and reloading the page, the draft edits remain available.

It included browser verification and kept FR-2 unresolved with the plan explicitly
a draft. No storage choice, manual-save precondition, or latency target was added.
The correction is observed evidence for this one repeated case, not a held-out
generalization result or a complete generated plan.

## Checks and remaining limits

- `make validate-ai`: passed local structure and JSON/TOML validation.
- `PYTHONDONTWRITEBYTECODE=1 python3.11 tests/story_execution_test.py`: 11 passed.
- `PYTHONDONTWRITEBYTECODE=1 python3.11 tests/coding_workflow_contract_test.py`: 5 passed.
- One-off Python inspection: changed skill links resolve inside the bundle;
  shared acceptance anchor exists; both Ralph plan examples parse with unchanged
  key sets and false completion flags; scenario IDs are unique.
- `git diff --check`: passed.
- Initial create-skill `check` under the default Python 3.11 returned exit 3
  because that interpreter lacks PyYAML. After activating the existing Conda
  `dotfiles` environment, `check` reported Python 3.11.16 and PyYAML 6.0.3;
  `validate` passed for prepare-implementation's frontmatter and bounded file
  tree. No dependency was installed and no package was produced. The activation
  instruction is now recorded beside the repository's test commands in AGENTS.md.

Five new cases in
[implementation_planning_evals.json](../tests/fixtures/implementation_planning_evals.json)
specify split export, ambiguous performance, combined source criteria, omitted
integrated acceptance, and scoped refinement of an existing plan. The fixture
remains a specification, not model-run evidence. Exercises A/B used equivalent
supplied text only; the remaining cases have not run through a model harness.
No quantitative benchmark, controlled comparison, or installed-skill test is claimed.
