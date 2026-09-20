# TypeScript implementation

1. Inspect package.json, the lockfile, tsconfig, module type, Node/runtime target,
   and the installed SDK declarations. Match imports and tool registration to that
   SDK major. Follow version-specific official examples; never mix SDK generations.
2. Prefer the high-level registration interface when it satisfies the contract.
   Lower-level request handlers can be legitimate; do not label every existing
   handler deprecated or rewrite working servers solely to match an example.
3. Keep schema validation at the tool boundary. Infer TypeScript types from runtime
   schemas when practical. The supported schema libraries and registration argument
   shapes vary by SDK generation; verify them rather than assuming Zod syntax.
4. Separate a provider client from tool mapping and the transport entry point. Use
   dependency injection only where it makes provider mocking/lifecycle ownership
   clear. Apply timeout/cancellation through the actual HTTP client API.
5. Align package main/bin, compilation output, module imports and executable paths.
   In monorepos, shared imports can produce nested output directories. Verify actual
   emitted files and an isolated package inventory; do not assume dist/index.js.
6. Run configured formatter, typecheck, build, focused tests, and protocol smoke
   checks. Typecheck the tests if the main tsconfig excludes them. Use a preinstalled
   Inspector or SDK client if available; invoking npx can download code and needs
   the applicable installation authorization.

The official SDK main branch can target a different major than your repository.
Consult [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
and its version-specific documentation. This bundle intentionally does not ship
an unpinned package manifest or a supposedly universal copy/paste server.

## Provenance

Modified from Anthropic mcp-builder; see [provenance](provenance.md).
