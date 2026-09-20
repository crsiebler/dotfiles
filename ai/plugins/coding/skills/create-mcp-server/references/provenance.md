# Provenance and adaptations

Adapted 2026-09-19 from Anthropic's
[mcp-builder](https://github.com/anthropics/skills/tree/34040c9c568585f6929bedeaad110ad08f079624/skills/mcp-builder)
at commit `34040c9c568585f6929bedeaad110ad08f079624`. The local skills checkout was
read-only and clean. Its SKILL.md and reference guides informed this bundle.
The Apache-2.0 [LICENSE.txt](../LICENSE.txt) is copied unchanged. No separate NOTICE
file was present in the source bundle.

SKILL.md and design/typescript/python/verification/evaluation references are
rewritten adaptations with modification notices. Core retained ideas: workflow
quality, clear schemas/descriptions, bounded pagination, transport selection,
actionable errors, annotations, version-appropriate SDKs, and realistic evaluations.

Changes: harness-neutral instructions; project-first SDK/language choice; official
server reuse assessment; scoped tool coverage instead of blanket API coverage;
version checks instead of fixed import templates; optional output formats; precise
legacy-SSE distinction; operational permissions and isolated test evidence. No
upstream scripts, model-provider evaluation dependencies, or example credentials
are shipped. The user's runtime and repository policy remain authoritative.

Official references checked during authoring (2026-09-19):
- [MCP tools, 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)
- [MCP transports, 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)

The dated protocol pages are authoring evidence, not a latest-version assertion.
SDK main branches described newer major versions when checked; consumers must
verify their own protocol and dependency versions. Local fixture/evaluation records
live outside the distributable skill in the dotfiles tests and documentation.
