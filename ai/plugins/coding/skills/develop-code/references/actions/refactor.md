# Behavior-preserving refactor

Identify a concrete maintenance cost: repeated knowledge, conflicting
responsibilities, hard-to-trace state or a fragile boundary. Fewer files/lines,
one implementation or one export alone does not justify a transformation.
Read the implementation, affected consumers and tests before choosing structure.

Write down the applicable equivalence contract: outputs, errors and timing
guarantees, side effects, persistence, ordering, public APIs, defaults, encoding,
platform support and resource acquisition/cleanup. Treat intended behavior
changes separately using the feature or bugfix method; do not relabel them as
refactoring. Preserve security, accessibility and data-loss protections.

Establish a passing baseline using [testing strategy](../testing-strategy.md).
Add missing characterization before transforming brownfield code. Existing
undesirable behavior may be part of the compatibility baseline; do not bless it
as desirable or fix it silently. Resolve required baseline failures explicitly.

Refactor in small coherent steps, retaining dependency direction and public
contracts. Prefer existing patterns over mandatory Strategy, CQRS or layers.
Use explicit dependencies only where useful, without assuming a domain directory
or rewriting all object creation. Keep a useful abstraction when it owns an
actual boundary even if it has only one implementation.

Require equivalence evidence before a shorter replacement. For example, a native
parser that drops empty fields cannot replace one that preserves them solely
because it uses fewer lines. Check corner cases, error behavior and lifecycle
as well as happy-path outputs. Use characterization or differential checks where
appropriate, not raw line-count comparisons.

Run focused tests after meaningful steps, then relevant regressions, formatting,
lint and typecheck. Inspect the final diff for accidental behavior and scope
changes. Report the maintenance benefit, trade-offs, preserved contracts and
evidence, executed checks and compatibility gaps. Do not claim equivalence for
unexercised boundaries or introduce an unrelated rewrite to lower a metric.
