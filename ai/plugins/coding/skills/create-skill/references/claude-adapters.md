# Optional Claude-specific evaluation

The upstream Apache bundle includes run_eval.py, improve_description.py, and
run_loop.py. They depend on a separately configured Claude CLI and/or Anthropic
Python SDK/API access. They are not retained in this portable distribution and
are never invoked by its helpers. Portable authoring, packaging, and aggregation
require neither a provider login nor model access.

If a user explicitly requests an upstream adapter, inspect its current interface,
dependencies, and writable paths before proposing its exact operation. Obtain any
required dependency/spending authorization and place its working copy and outputs
inside the active project. Preserve installed sources, avoid automatic servers,
and do not assume the upstream adapters enforce this package's path boundaries.
Do not translate absent native agent/metric capabilities into invented tools or
zero token measurements. Use the portable evaluation workflow when adapters are
unavailable; do not automatically download or install them.
