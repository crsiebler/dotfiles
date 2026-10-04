# Requirements

## Required and conditional dependencies

External research needs an exposed authorized search/page-fetch capability.
This instruction-only skill has no mandatory Python package, browser binary,
Exa CLI, or npm dependency. Native search/browsing is adequate when available.
Exa MCP is an optional provider; load [Exa guidance](exa.md) only when its tools
are exposed and selected.

## Setup and checks

Inspect runtime tool schemas before choosing a provider. If research tools are
absent, use supplied context and report unavailable verification; do not invent
calls or silently download a provider SDK.

For optional Exa setup, follow the provider's
[official MCP instructions](https://docs.exa.ai/reference/exa-mcp) and the active
harness's connection UI/configuration. Endpoint/key requirements depend on that
connection. Configuration writes, network access, and authentication need their
own scope; never expose keys. An SDK installation is not a configured MCP
connection and does not expose tools to the agent.

After setup, verify the advertised search/fetch schema and a scoped read if
authorized. Connection presence alone does not establish source quality,
subscription limits, or successful retrieval.
