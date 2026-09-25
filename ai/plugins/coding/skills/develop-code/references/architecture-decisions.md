# Architecture decisions when a boundary changes

Use this guidance for material changes to interfaces, responsibilities,
dependencies, persistence, concurrency, trust boundaries or performance. Start
with requested outcomes and affected consumers. A small local fix does not need
an architecture inventory, new layering or a full ADR.

## Reuse before invention

Consider suitable project code first, then the standard library, native platform
or framework capabilities, installed dependencies, and minimal cohesive custom
code. Suitability includes behavior, lifecycle, supported versions, deployment
constraints and maintenance cost. This preference does not authorize installing
dependencies or replacing sound code merely because a built-in exists.

Before reuse or replacement, compare required success and failure behavior,
defaults, ordering, encoding, precision, side effects and resource ownership.
Document any intentional incompatibility separately. Retain validation, security,
accessibility and data-loss prevention; reducing lines is not equivalence proof.
Use characterization and boundary evidence for the actual consumers.

## Questions that select a design

| Concern | Decision questions and evidence |
| --- | --- |
| Cohesion and information hiding | What decision or invariant does this module own? Can its representation change without forcing unrelated consumers to change? Separate responsibilities that actually evolve independently. |
| Coupling and dependency direction | Which consumers change together and why? Are stable contracts depending on volatile mechanisms? Look for actual knowledge leaks, cycles and coordination cost before introducing a seam. |
| Duplicated knowledge | Do these sites encode the same business rule, or merely look similar? Shared syntax with different reasons to change may be safer left separate. Centralize one rule when drift has a concrete consequence. |
| Contracts and substitutability | Can a caller use either implementation with the same preconditions, outputs, errors and side effects? Does a replacement strengthen input requirements or weaken promised behavior? |
| State and ownership | What transitions are legal, who owns mutation and cleanup, and which invariants must survive retries or partial failure? Identify transaction boundaries, ordering, concurrency and cancellation. |
| Cost and workload | What input size, access pattern or measured bottleneck matters? Compare algorithmic/query cost, memory growth and blocking behavior for that workload; distinguish estimates from measurements. |
| Reversibility | How costly is rollback, schema evolution or a future substitution? Can the choice be contained behind an existing boundary? Avoid speculative options whose complexity exceeds the demonstrated need. |

An interface, adapter, service, dependency injection, CQRS or DDD pattern is useful
only when it addresses the observed constraint. Do not introduce all of them or
assume that the vocabulary establishes correctness. Conversely, do not delete
indirection solely because there is only one implementation today. Check what
knowledge and lifecycle the boundary isolates.

## Counterexamples to automatic simplification

- A single vendor adapter hides retry semantics, maps errors and owns shutdown.
  Its interface can protect callers and make contract tests realistic even with
  one implementation. Removing it may spread vendor assumptions and cleanup
  obligations. Inspect consumers and change cost before recommending removal.
- Two identical validation expressions serve independently evolving policies.
  A shared helper could couple unrelated changes. Similar syntax is insufficient
  evidence that they share one rule.
- A one-line parser drops empty fields, normalizes Unicode or changes error
  categories while the old parser promises preservation. A smaller implementation
  is incompatible unless those differences are explicitly accepted and verified.
- Replacing explicit cleanup with an early return may preserve normal outputs
  while leaking resources after partial setup. Equivalence includes lifecycle,
  not just the happy-path value.

## Record significant decisions proportionally

For a consequential or hard-to-reverse choice, explain context and constraints,
credible alternatives (including retaining the current design), selected trade-offs,
affected contracts, verification, and rollback or revisit conditions. Follow the
project's ADR conventions when applicable. A short decision note is enough when
no durable cross-team decision needs recording; do not require a new document for
every local change.

Judge the result by correctness, compatibility, reasoning/change cost, failure
behavior and lifecycle. Respect configured size/complexity checks while treating
metrics as signals rather than universal quality scores. Do not split cohesive
generated, declarative, fixture or handwritten code solely to reduce a metric.
State assumptions and unavailable evidence without inventing improvements.
