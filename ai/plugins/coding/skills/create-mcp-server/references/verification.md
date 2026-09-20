# Verification and prerequisites

This instruction-only skill has no runtime helper or required Python/Node packages.
The server being built needs its project-selected SDK, runtime, schema/HTTP clients,
and test tooling. Inspect availability before commands. Do not install tooling,
launch persistent services, or alter global client configuration as a hidden check.

| Check | Evidence required |
| --- | --- |
| Tool contract | tools/list names, schemas, annotations, pagination and declared capabilities agree with handlers |
| Validation | Invalid/missing inputs fail before provider calls; success outputs match schemas |
| Provider adapter | Fixtures exercise endpoint mapping, pagination, empty data, auth errors, rate limits, timeout and malformed responses |
| Effects | Mutations respect permissions; retry tests show no duplicate effects; no live writes needed for ordinary tests |
| Transport | Real SDK client initializes, lists tools, calls success/failure cases, then closes cleanly |
| Stdio | Captured stdout contains only protocol messages even during startup/errors; diagnostics and secrets are checked |
| HTTP when applicable | Methods, Origin rejection, authentication/tenant boundaries, session and cancellation behavior |
| Packaging | Declared executable exists in actual build/package output and works outside source cwd |
| Task usefulness | Representative fixture-based tasks succeed with attributable results; distinguish manual from agent runs |

Test new behavior with a failing regression first, then implement and rerun. Use
existing fixtures and deterministic local fake providers. Live integration checks
need an authorized account/environment and clear effects. A read-only query can
still transmit private data or incur costs. Do not run a whole live suite blindly.

Record exact commands/results and SDK/runtime versions where observed. Explain
skips and unavailable checks. Confirm no leftover owned processes/artifacts; respect
project process/deletion policy. Never infer success from early-returned tests,
syntax checks, screenshots, successful discovery, or an Inspector launch alone.

## Provenance

Modified from Anthropic mcp-builder; see [provenance](provenance.md).
