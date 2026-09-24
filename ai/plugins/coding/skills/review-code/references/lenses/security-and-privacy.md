# Security and privacy

Use when untrusted inputs cross trust or authority boundaries, sensitive data is
handled, or exposure/resource-abuse paths change. Identify protected assets,
actors, entry points and expected authority from source and supplied evidence.
Trace input to sensitive operations, including validation, canonicalization,
escaping and enforcement order. A suspicious API name alone is not a finding.

Inspect relevant authorization context, object/tenant boundaries, injection paths,
filesystem traversal/symlinks, command construction, deserialization and network
destinations. Consider reachable resource abuse and defaults that change exposure.
Explain the actual source-to-sink path, required attacker control, existing
mitigations and resulting impact. Do not assume authentication implies authority
over every requested object or that a wrapper flag proves downstream enforcement.

Follow sensitive data through collection, storage, transport, logging, errors,
caches and retention. Assess whether diagnostics disclose secrets or personal
data. Cite locations and redacted shapes, never copy credentials or private data
into findings. Do not read credential stores to confirm a suspected exposure.
Report uncertainty about runtime configuration and enforcement explicitly.

Use supplied evidence or source tracing only. This lens does not authorize active
security tests, exploit execution, auth changes, security-feature disabling,
infrastructure operations or external posts. Recommend the smallest appropriate
remediation and verification for an authorized implementer. Do not invent legal
or compliance conclusions or demand unrelated hardening programs.
