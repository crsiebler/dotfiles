# Project agent guidance template

This is an example for a code repository, not an installed policy. Before use,
replace every `TODO` with verified project facts or remove the inapplicable item.
Do not assume sample commands exist. No personal skill collection is required.

For a new project, adapt this document to the actual architecture, supported
platforms and verification commands. For an existing project, merge relevant
guidance into its current instructions; preserve local rules and link established
guides instead of overwriting or duplicating them. Do not automatically synchronize
other repositories. In mixed-purpose repositories, scope engineering guidance to
code directories/tasks; research, writing and creative work need their own relevant
instructions rather than mandatory coding procedures.

## Verified project facts

| Fact | Maintainer-supplied value |
| --- | --- |
| Purpose and users | TODO: actual product and main outcomes |
| Stack and supported versions/platforms | TODO: languages, runtimes, frameworks, compatibility constraints |
| Package manager and dependency policy | TODO: authoritative lockfile/tool and approval rules |
| Module responsibilities and dependency direction | TODO: code directories, owners, allowed boundaries |
| Public interfaces and persisted formats | TODO: consumers, compatibility/evolution policy |
| Trust and resource boundaries | TODO: sensitive inputs, ownership and cleanup responsibilities; no secrets |
| Documentation | TODO: links to actual architecture, contribution and operational guides |

## Commands and environments

Verify commands against the repository before filling this table. State the
working directory, prerequisites, scope, side effects and whether external access
is needed. Mark unavailable checks explicitly; do not invent conventional script
names or install missing tools without authorization.

| Check | Verified command and directory | Scope / prerequisites / side effects |
| --- | --- | --- |
| Formatter | TODO or unavailable | TODO: changed-file invocation and configured rules |
| Lint | TODO or unavailable | TODO |
| Typecheck | TODO or unavailable | TODO |
| Focused tests | TODO or unavailable | TODO: selecting affected tests |
| Regression / integration | TODO or unavailable | TODO: isolated fixtures, external authorization |
| Build / schema | TODO or unavailable | TODO: relevant generated meaning or static validation |
| UI verification | TODO or not applicable | TODO: real routes/states/browser and accessibility evidence |

## Engineering principles

- Understand requested outcomes, affected code/callers and contracts before edits.
  Prefer supplied context and scoped inspection; do not map the entire repository
  for a local change. Make routine decisions within scope; ask for material unknowns
  or new authority. Preserve planning-only, diagnosis-only and read-only requests.
- Follow language idioms, existing architecture, package manager and configured
  lint/format rules. Prefer suitable project reuse, standard library, native
  platform/framework capability, installed dependencies, then minimal custom code.
  This does not authorize new dependencies or mandatory replacement of sound code.
- Make the smallest correct change satisfying all requested requirements. Keep
  modules cohesive and readable; separate responsibilities when they diverge.
  Judge reasoning/change cost and preserved contracts, not the fewest lines/files.
  Do not add abstractions merely because a checklist names them.
- Suggested review thresholds: roughly 300 lines for handwritten implementation;
  at 500, assess whether responsibilities should be separated. Customize these to
  project conventions; they are review prompts, not hard limits or quality targets.
  Permit justified cohesive/generated/declarative/fixture exceptions. Never split
  code solely to reach a number or introduce an unrelated refactor for file size.
  Let the configured language formatter determine line width.

## Contracts and decisions

Preserve applicable outputs, errors, defaults, side effects, ordering, precision,
encoding, public interfaces, persistence and resource lifecycle. Retain appropriate
validation, security, accessibility and data-loss prevention. Separate intended
behavior changes from refactoring; shorter replacements need equivalence evidence.

For material responsibility/interface/dependency/persistence/concurrency/trust or
performance changes, consider cohesion, information hiding, coupling, duplicated
knowledge, substitutability, state invariants, workload cost and reversibility.
Patterns and layers are conditional tools. A single implementation may justify an
interface when it isolates a useful contract; similar syntax may represent
independently evolving rules. Do not impose an architecture vocabulary as a goal.

For significant decisions, follow existing ADR conventions: context, constraints,
alternatives, trade-offs, verification and rollback/revisit conditions. Routine
local changes need no full design document or speculative infrastructure.

## Feature, fix and refactor methods

- New behavior: define observable outcomes and important failure paths. Add
  meaningful failing tests before implementation, confirm the intended failure,
  implement to green and run relevant regressions. Preserve every requirement.
- Fixes: establish expected/actual behavior and triggering conditions; distinguish
  hypotheses from confirmed causes. Before implementation, add a meaningful
  regression reproducing the confirmed defect and confirm it fails for the
  intended reason. Connect causal evidence to that regression, the repair and
  related paths. Do not mask symptoms with swallowed
  errors or unbounded retries. Diagnosis-only means no repair; source-only means
  no execution of reproductions or tests.
- Refactors: name the maintenance problem and preserved contracts; establish a
  passing baseline and missing characterization before transformation. Preserve
  existing tests and inspect consumers. Treat intentional incompatibilities as
  separate behavior changes, not incidental simplifications.

## Verification discipline

Use meaningful behavior assertions and realistic boundary doubles. Preserve real
logic under test, isolate nondeterministic/external boundaries and keep cleanup
with the resource owner. Distinguish product races from fixture/shared-state,
clock, ordering and environment failures. Do not weaken assertions, hide failures,
disable tests or blindly regenerate snapshots to get a passing run.

Existing work stays preserved: report actual test order and establish regression
sensitivity without discarding changes to reenact test-first development. Never
claim red/green runs that did not occur. No fixed test-count or coverage ceiling;
cover distinct required failure paths and material risks.

Use appropriate schema, lint, typecheck or build checks for static docs/config;
avoid low-value spelling tests. Generators and runtime configuration need checks
of generated meaning and selection behavior. Test critical integration paths in
authorized environments; unit doubles alone do not prove real boundary behavior.

Run configured formatters on changed files after edits and before final verification
or commit, preserving unrelated formatting. Then run required lint/typecheck and
relevant tests/schema/build checks. Always run the project's typecheck before a
commit when available; otherwise report its absence explicitly. Report missing
formatters likewise; do not install tools or change configuration implicitly.
Broaden or repeat checks only when new edits, failures or unresolved concerns
justify it. Respect external-service, migration and process approval boundaries.

For UI changes, inspect actual rendered behavior, important flows/states, relevant
viewports, keyboard/focus and accessibility evidence. Source-only inspection is not
browser verification; report missing tools or untested states honestly.

## Review and handoff

Establish review scope and evidence before judging changes. Read-only review means
inspection and recommendations, not tests, edits, formatting, staging or posting.
Findings need location, trigger, violated contract, impact, attribution, evidence,
remediation and proposed verification. Separate optional maintenance suggestions
from defects; respect supplied formats and required dedicated review gates.
No findings does not establish correctness or permission to ship.

Report actual changes and purpose, causal/equivalence evidence, exact checks and
results, test order, compatibility risks and unverified boundaries. Separate source,
model, integration and installed/runtime evidence. Preserve unrelated work and
follow existing commit conventions and authorization; implementation completion
does not authorize commits, pushes, deployments or external messages.
