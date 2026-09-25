# Reliability

Use when a request crosses process/service boundaries or behavior depends on
timeouts, retries, cancellation, cleanup, recovery or partial failure. Identify
the operation's completion contract and what the caller can safely retry.

Trace deadlines and timeout propagation, bounded retry count/duration, backoff,
retry classification and idempotency. Check duplicate effects when a response is
lost after a successful side effect. A retry loop is not resilience evidence
unless its assumptions hold for actual operations and callers. Avoid prescribing
universal timeout or availability targets unsupported by the project.

Follow cancellation and error propagation across async work. Check resource
ownership and cleanup after partial acquisition, success, exception and shutdown.
Inspect compensation/reconciliation paths for partially committed work, crash
recovery and repeated startup. Distinguish rollback from a best-effort compensating
action with different guarantees. Consider queue ordering and mixed-version recovery
when they affect the contract.

Use source paths and supplied logs/tests with their actual provenance. Identify
the exact failure sequence, observable impact, remaining uncertainty and verification
needed. Do not inject faults, restart services, run tests, operate infrastructure
or fix code during review. Recommend bounded checks for later authorized work;
do not claim the system recovered because a recovery function merely exists.
