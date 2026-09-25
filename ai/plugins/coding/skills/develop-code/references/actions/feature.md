# Feature method

1. Translate requested outcomes into observable success and failure contracts.
   Inspect relevant callers, state, interfaces and existing tests. Clarify missing
   facts only when they change the solution. A routine local change needs no full
   plan, ADR or speculative architecture.
2. Select evidence using [testing strategy](../testing-strategy.md). For new
   behavior, write meaningful failing tests before implementation and confirm
   the failures reflect the absent requirement, not broken setup. Cover distinct
   required paths; neither one test nor an arbitrary coverage target is sufficient
   by definition. Preserve pre-existing implementation and report its actual order.
3. Implement within existing architecture. Prefer suitable reuse and explicit
   dependencies when they clarify a real boundary or enable realistic tests.
   Injection or an adapter is a tool, not mandatory ceremony. Keep errors,
   compatibility, lifecycle and validation appropriate to the affected contracts.
4. Run the focused checks to green, then relevant regressions and configured
   formatting before final verification. Investigate failures rather than weaken
   assertions. Verify rendered UI flows with authorized browser evidence when
   relevant, or clearly report the verification blocker.
5. Inspect the diff for accidental behavior changes. Report implemented outcomes,
   relevant failure coverage, commands/results, missing checks and unresolved
   compatibility or integration risks. Do not claim delivery through a caller's
   gate unless that gate actually passed.
