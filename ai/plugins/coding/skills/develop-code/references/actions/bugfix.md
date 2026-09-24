# Diagnosis and repair

Respect the requested investigation boundary first. For diagnosis-only work,
inspect and report without edits. Run a reproduction only when the request and
runtime permit it; source-only or read-only assessment must use tracing and
supplied evidence. Never use a failing production path as an implicit test target.

1. Establish expected versus actual behavior, triggering inputs, environment,
   frequency and impact from concrete evidence. Separate user observations,
   traces, source deductions and unverified hypotheses. Narrow the affected path
   before proposing repairs.
2. Follow data/state and control flow to a causal explanation. Compare relevant
   working/failing conditions where authorized. State what evidence would falsify
   the hypothesis. Symptom disappearance, arbitrary retries or swallowed errors
   do not establish a fix. If the cause cannot be verified, say so.
3. For an authorized repair, add a regression reproducing the actual defect
   before implementation. Confirm it fails for the intended reason. Use a safe
   local boundary double or authorized integration, preserving the logic that
   causes the failure. Follow [testing strategy](../testing-strategy.md) for
   pre-existing edits, unavailable execution and realistic boundary evidence.
4. Repair the confirmed cause with the smallest correct change. Inspect related
   callers and failure paths for the same assumption. Keep public errors,
   validation, security and resource ownership intact unless a behavior change
   was explicitly requested. Do not widen scope into unrelated redesign.
5. Verify the regression and related contracts, format changed files before final
   checks, and inspect the diff. Distinguish an application race from fixture,
   clock, shared-state, ordering or environment failures; do not mask either with
   retries or weakened assertions.

Report the causal chain and its evidence, what changed (or diagnosis only),
regression sensitivity, actual commands/results, remaining hypotheses and any
unverified integration. If meaningful reproduction is blocked, do not invent
red/green evidence or call an unconfirmed hypothesis a verified repair.
