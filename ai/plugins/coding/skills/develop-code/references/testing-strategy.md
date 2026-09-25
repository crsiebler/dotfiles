# Select verification by changed contract

Repository instructions, actual scripts and configured tool versions determine
commands. Inspect their side effects before execution. Prefer relevant installed
tools; missing dependencies do not authorize installation, external integration,
migrations or service operations. For diagnosis-only/planning-only work, present
the needed evidence without running commands outside that scope.

| Change | Evidence |
| --- | --- |
| New behavior or bug fix | Meaningful failing behavior/regression tests before implementation; intended failure, then green and relevant regressions |
| Behavior-preserving refactor | Passing baseline and missing characterization before transformation; compatibility of affected consumers |
| Static docs, metadata, configuration or dependency declarations | Relevant schema, parsed contracts, lint, typecheck or build validation; no low-value spelling assertions |
| Configuration generators or runtime selection | Generated meaning, defaults, overrides, invalid inputs and actual selection behavior |
| External integration | Realistic boundary double plus authorized integration evidence for contracts the double cannot establish |

Use [testing anti-patterns](testing-anti-patterns.md) when writing tests or choosing
doubles/utilities. Keep application behavior real, isolate actual external or
nondeterministic boundaries, and use contract-valid fixtures. Test cleanup owns
only fixture-created resources and must handle partial setup failure. A production
cleanup API is appropriate when production genuinely owns that lifecycle.

For red/green work, run the new assertion and confirm the intended failure before
implementing. Import errors, unavailable binaries and invalid fixtures are setup
failures, not evidence of missing behavior. Cover materially different failure
paths, boundary values and interactions according to requirements and risk.
Do not impose a fixed test count or coverage percentage.

When implementation already exists, preserve it and disclose actual order. Show
regression sensitivity through safe, scoped evidence without discarding existing
work to reenact test-first. If execution is blocked, explain the blocker and
what remains unverified; do not invent a red/green run.

For brownfield work, characterize observable contracts before transformation.
Differential tests can compare old/new behavior where safe, but do not establish
that the old behavior was desirable. Separate intended fixes from preservation.
Unit doubles do not prove real filesystem, process, database, browser or service
compatibility. Run relevant integration checks for critical paths only with the
necessary authorization and environment, otherwise report the verification gap.

Diagnose flakes using evidence about clocks, randomness, scheduling, shared state,
ordering and environment. Distinguish product races from fixture contamination
or setup failures. Preserve assertions and failure evidence; do not add arbitrary
sleeps/retries, disable tests or hide failures to obtain green output.

Run configured formatters on intended changed files before final verification.
Then run required lint, typecheck and relevant tests/build/schema checks. Inspect
automatic changes. Broaden/repeat checks when new edits, failures or unresolved
risks justify it. Never infer a script merely from a familiar command name.
If formatter or typecheck is unavailable, report it explicitly; do not invent
passing results or change configuration to make checks disappear.

For rendered UI, verify affected flows, states, focus/keyboard and relevant
viewports with actual authorized browser evidence. Use an applicable advertised
interface-verification skill when available. Source inspection and screenshots
alone do not prove interactive behavior. Report missing browser capability or
required UI checks as limitations, not successful verification.

Handoff includes change classification, causal/equivalence evidence, actual
test order, exact commands and results, relevant regressions and unverified
boundaries. Explain why static validation was selected where applicable.
Keep source validation, model behavior, integration behavior and installed
activation evidence distinct; successful narrow checks do not prove the rest.
