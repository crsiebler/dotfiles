# Requirements

## Required and conditional dependencies

Planning and this instruction-only bundle need no installed SDK or utility.
Implementation needs the target project's runtime, package manager, selected MCP
SDK, provider libraries, and test tools. Inspect its manifest and lockfile before
choosing versions; preserve its SDK major and supported transport.

For Python, the official SDK package is `mcp`; the optional CLI extra is
`mcp[cli]`. For TypeScript, select packages from the project's SDK generation:
v1 uses `@modelcontextprotocol/sdk`; v2 uses `@modelcontextprotocol/server`
and/or `@modelcontextprotocol/client`, with applicable transport/framework
packages. These are alternatives, not a combined installation requirement.
See the [Python SDK](https://github.com/modelcontextprotocol/python-sdk) and
[TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk).

## Installation and checks

Restore declared dependencies using the project's documented, locked workflow.
For a new Python server, after approving dependency changes, use a project
environment and an explicitly selected SDK version:

```sh
python3.11 -m venv .venv-mcp
./.venv-mcp/bin/python -m pip install 'mcp==<approved-version>'
./.venv-mcp/bin/python -c 'import mcp'
```

Replace the version placeholder; use a fresh environment path. For TypeScript,
use the chosen SDK's official installation command with approved versions and the
project's package manager. For an approved npm project, choose the matching major:

```sh
# v1 project:
npm install --save-exact '@modelcontextprotocol/sdk@<approved-version>'
# v2 server project (add the client package only if needed):
npm install --save-exact '@modelcontextprotocol/server@<approved-version>'
```

Choose one example and replace the version; both modify the manifest/lockfile.
Do not mix v1 examples with v2 imports or upgrade dependencies automatically.

The [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) is
optional. If selected, check its current Node.js requirements and approve its
download, local service launch, and server connection separately; a documented
`npx @modelcontextprotocol/inspector` command downloads code when absent.
An existing SDK client or project test can verify transport without Inspector.
No server, credential configuration, or external write is authorized by setup.
