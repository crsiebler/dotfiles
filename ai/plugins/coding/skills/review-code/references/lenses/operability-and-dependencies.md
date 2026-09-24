# Operability and dependencies

Use for runtime configuration, diagnostics, packaging, deployment assumptions or
dependency changes. Inspect meaningful error/log context without sensitive data,
health/readiness semantics, startup/shutdown and resource release. Verify defaults,
missing/invalid configuration behavior and documented environment assumptions from
source and supplied evidence; do not read secrets to fill a gap.

Trace rollout/rollback compatibility, mixed versions and partial deployment
behavior where relevant. An available rollback command does not prove data or
protocol compatibility. Name missing migration, packaged-artifact or operational
evidence. Do not deploy, restart services, operate containers or change production
configuration during this assessment.

For dependencies, assess actual necessity and suitable existing/native options,
supported versions/platforms, transitive constraints, provenance and lockfile/build
reproducibility. Check that package entry points and distributed resources match
the consumers and stated installation method. Supplied scan/advisory evidence must
match the exact dependency/version and reachable usage; do not invent current
vulnerability status or download tools to inspect it. Flag unresolved licensing
questions for appropriate review without making unsupported legal conclusions.

Distinguish source, build, packaged artifact, installed discovery and live runtime
evidence. Inspect relevant supplied documentation and diagnostics for the actual
failure path, not a generic observability checklist. Recommend bounded verification
for later authorized work. No install, update, external post or automatic specialist
delegation follows from selecting this lens.
