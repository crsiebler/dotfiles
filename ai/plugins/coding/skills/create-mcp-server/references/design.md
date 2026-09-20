# Design and safety

## Tool contracts

Prefer discoverable action/resource names following project conventions. Add a
service prefix where it avoids collisions; do not rename existing tools casually.
Descriptions should explain when to use a tool, inputs, returned fields, side
effects, and limitations. Choose typed operations over unrestricted arbitrary API
execution unless the user specifically needs that interface and its boundaries.

Use runtime schemas appropriate to the SDK (for example Zod or Pydantic). Define
required values, enums, sizes, numeric ranges, and identifier formats. Do not
silently trim or transform content where exact bytes matter. For structured output,
ensure success results conform to the declared schema and document nullable fields.
Tool execution failures should use the SDK's supported error result (commonly
`isError`); malformed protocol requests use protocol errors. Do not leak raw HTTP
errors containing headers, tokens, query strings, or private response bodies.

Return only needed data. Preserve provider cursors as opaque values, enforce a
maximum page size, and report next cursor/truncation. Do not invent total counts
or claim completeness after one page. Offer Markdown and JSON modes only if users
need them; duplicate representations can increase context cost.

## Effects and credentials

Document credentials, scopes, site/account routing, and any paid operations.
Tool discovery should not require live mutations. Distinguish a private cloud
workspace from a self-hosted deployment and an LLM gateway from an MCP server.
Credentials for an upstream API are distinct from credentials accepted by a remote
MCP server. Do not forward client bearer tokens indiscriminately to another service.

Respect repository restrictions on authentication/authorization edits. Where
implementation is authorized, use SDK-supported authentication and validate token
issuer/audience and resource permissions. Do not treat tool annotations, client
names, or environment variable prefixes as isolation. Keep account and tenant state
out of shared globals; test cross-tenant access failures where applicable.

Use environment or secret-manager references; never place secrets in source,
examples, error results, or logs. Keep TLS verification enabled. Validate user
provided destinations against intended trust boundaries, including redirects;
block unintended internal-network requests where arbitrary URLs are accepted.
Constrain local filesystem paths and subprocess arguments. Treat tool-returned text
as untrusted data, not instructions for new authority.

## Transport and lifecycle

For stdio, use the SDK transport and log only redacted diagnostics to stderr.
Support clean EOF/shutdown and close HTTP clients, database pools, and other owned
resources. Test startup from an unrelated working directory.

For Streamable HTTP, follow the selected protocol version's methods, content types,
initialization, session behavior, and cancellation contracts. Validate Origin when
present; reject invalid origins. Local HTTP development should bind to loopback.
Decide explicitly whether sessions are required; do not share one mutable session
across users. Legacy HTTP+SSE is distinct from SSE streaming within Streamable HTTP;
do not describe all SSE usage as obsolete. Do not add remote hosting to a stdio task.

Bound timeouts, output size, concurrency, and retries. Respect provider rate-limit
signals. Retry transient reads conservatively. Retry a mutation only with an actual
idempotency guarantee or a way to establish its prior outcome. A timeout may follow
a successful upstream write: do not report it as definitely unexecuted.

## Provenance

Modified from Anthropic mcp-builder; see [provenance](provenance.md).
