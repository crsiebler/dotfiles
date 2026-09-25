# Data and state

Use for persistence, shared mutation, numeric precision, ordering or state
evolution. Name the invariants and legal transitions, their owners and consumers,
and the contract that makes a violation consequential. Inspect inputs, missing
values, precision/rounding, units, locale/time-zone interpretation and serialization
where those choices affect behavior.

Trace transaction boundaries and partial writes, read-modify-write races, isolation
assumptions, lock ownership, ordering and concurrent updates. Check whether retries,
deduplication and idempotency keys preserve the invariant across crashes or duplicate
delivery. A transaction around one write does not prove an entire multi-step
workflow is atomic; state the actually protected boundary.

Inspect cache ownership, key construction, invalidation and stale-read assumptions
when correctness depends on them. Follow state through cancellation, errors,
resource cleanup and restart. Distinguish an illegal transition from merely an
unusual but supported order. Use concrete interleavings to explain races without
executing them or claiming a race was measured.

For schema/data evolution, examine supplied old/new readers/writers, defaults,
precision, compatibility and rollback evidence. Missing counterparts or production
configuration prevent whole-system assurances. Report exact unknowns instead of
querying live data or running migrations. No DELETE/DROP, migration, repair or
operational command is authorized by this read-only lens.

Findings need the trigger/interleaving, violated invariant, affected records or
consumer class, impact and evidence. Propose contract-sensitive verification
without inventing loss counts or claiming unperformed integration tests.
