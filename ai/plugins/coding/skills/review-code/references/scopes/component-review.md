# Existing component review

Identify the component, revision/snapshot, purpose and requested focus. No diff
is required. Establish its public contracts, entry points, state/resource owners,
relevant callers and dependencies from actual source and supplied evidence.
Bound the inspection to those contracts rather than expanding to every neighbor.

Trace success/failure behavior and important invariants. Existing tests can show
which contracts are asserted, but are not execution evidence. Do not run tests,
reproduce defects actively or edit a proposed fix. Apply only concerns whose
surface is present; distinguish static deductions from observed runtime behavior.

Pre-existing defects are in scope for an existing component. State attribution
honestly; without a historical comparison do not claim a regression was introduced
by a particular commit. Optional restructuring requires evidence of maintenance
cost, affected consumers and compatibility, not a preferred design pattern.

For cross-component review, name both sides and versions of each interface.
Unavailable implementations/configuration limit the conclusion even when one side
looks correct. Report inspected entry points and consumers, uninspected areas,
missing evidence and prioritized findings. Keep design proposals separate from
assessment of implemented contracts; neither implies authority to refactor.
