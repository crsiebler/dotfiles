# Bounded codebase audit

Agree the intended system boundary and focus from the request: components,
versions and risks of interest. Start with a small inventory of relevant entry
points, data/authority boundaries, configuration and dependencies. Select a
bounded inspection plan based on impact and uncertainty. Do not claim an entire
repository was reviewed because an inventory or search returned every filename.

Follow concrete paths across the selected components. Track inspected areas,
contracts and evidence provenance, plus areas merely inventoried or sampled.
Prioritize consequential findings and recurring causes without extrapolating a
sample into an invented defect count, measured score or exhaustive assurance.
Respect the caller's evidence/time/tool budget; report remaining coverage at its
limit rather than introducing a new agent chain or autonomous audit loop.

Pre-existing defects are allowed within the agreed scope. Verify triggering paths
and affected contracts, deduplicate shared causes and separate optional maintenance
recommendations. Mark unresolved attribution when source history is unavailable.
For missing services, generated outputs, runtime configuration, dependency versions
or production evidence, name what cannot be established and why it matters.

Audit means read-only source and supplied-evidence assessment. No scanning tools,
tests, exploit execution, installs, migrations, service operations, deployment,
posting or automatic fixes are authorized by this scope. Do not read credentials
to fill a configuration gap. Report findings, inspected coverage, uninspected
surfaces, uncertainty and useful next verification steps without executing them.
