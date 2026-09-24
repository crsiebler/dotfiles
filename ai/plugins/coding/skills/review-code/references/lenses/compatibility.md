# Compatibility

Use when consumers depend on a public API, schema, default, error, encoding,
ordering, runtime/platform version or persisted representation. Identify affected
producers/consumers and the baseline contract before assessing equivalence.

Trace success and failure behavior, missing/empty/null distinctions, precision,
locale/time-zone handling, Unicode and serialization. Check side effects and
resource lifecycle as well as returned values. An apparently shorter replacement
may change validation, error types, duplicate handling or cleanup. Do not infer
equivalence from a happy-path test or similar signatures.

For versioned protocols, persistence or releases, inspect supplied evolution,
defaults and migration evidence, old/new readers and writers, supported platforms,
and mixed-version rollout/rollback expectations. Missing counterpart or migration
evidence limits the conclusion; it does not justify executing a migration or
querying production. Distinguish an authorized intentional breaking change from
an accidental regression and verify that documented expectations match callers.

Use supplied characterization, contract or integration evidence with its actual
scope/revision. Test source alone does not establish a passing run. Attribute each
issue against the selected scope's baseline, cite the consumer/trigger and changed
contract, and propose practical verification without executing it. Do not demand
unrequested indefinite backward compatibility or approve unverified equivalence.
