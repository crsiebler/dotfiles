# Python implementation

1. Inspect pyproject/requirements, lockfile, interpreter and installed SDK version.
   Follow the existing package layout and async/test conventions. Verify supported
   imports against the selected release before writing code.
2. Distinguish the official MCP Python SDK from the separately distributed FastMCP
   project. Names and decorators in upstream examples may belong to older releases;
   do not silently switch packages or mix imports from different implementations.
3. Use the selected SDK's high-level registration API where appropriate. Build
   runtime-validated inputs and structured results using supported types/models.
   Verify how model parameters appear in the exposed schema: avoid accidentally
   adding an unwanted nested argument object.
4. Use async clients for network I/O, with explicit timeout and cancellation policy.
   Own connection cleanup through lifecycle/context management. Isolate provider
   adapters for fake-response tests; avoid blocking work in async handlers.
5. Configure logging to stderr for stdio. Test imports and the actual module or
   console entry point from another working directory. Byte compilation alone
   does not establish dependencies, schema correctness, or protocol compatibility.
6. Run configured formatting/lint/typechecking and focused pytest or project tests.
   Missing optional tools are limitations, not permission to pip/uv install. SDK
   client or Inspector checks require available tooling and authorized effects.

Consult the [official Python SDK](https://github.com/modelcontextprotocol/python-sdk)
for the installed major's documentation. Do not assume the main README describes
the user's pinned version or that a decorator proves endpoint authorization.

## Provenance

Modified from Anthropic mcp-builder; see [provenance](provenance.md).
