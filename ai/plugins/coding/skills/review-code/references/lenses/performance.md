# Performance

Use when the code or request exposes a credible workload, resource-growth path or
measured regression. Establish input size, access pattern, frequency, concurrency,
data volume and relevant environment from supplied evidence. Mark unknowns;
do not invent throughput, latency, memory, token or cost measurements.

Trace algorithmic complexity and repeated work, query counts and round trips,
batching, blocking operations, allocations, retained objects and unbounded queues.
Relate the path to the actual workload and user/operational impact. Distinguish
asymptotic reasoning and estimates from measured behavior. A loop or abstraction
alone is not evidence of a material bottleneck.

For caching, inspect key correctness, invalidation, hit/miss assumptions, retention
and stampede behavior; faster stale or cross-user results are not an acceptable
optimization. Consider backpressure and resource bounds rather than assuming more
parallelism always helps. Preserve correctness and lifecycle in proposed changes.

Use supplied profiles/benchmarks only with their input, revision, configuration and
measurement basis. Name missing representative measurements and propose focused
verification. Do not run benchmarks, queries or load tests, install a profiler,
or rewrite code during review. Prioritize demonstrated costs over speculative
micro-optimizations and do not prescribe universal performance targets.
