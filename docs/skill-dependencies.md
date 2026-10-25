# Skill dependency audit

## Scope and findings

This source audit covers all 47 repository-owned Craft skills under
`ai/plugins/*/skills/*/`. It examines skill entry points, supporting references,
shipped helper imports/subprocesses, and declared Python requirements. It does
not modify or inventory installed vendor skills, authenticate providers, install
utilities, provision models, or establish live integration compatibility.

All 47 bundles contain a linked references/requirements.md that travels with
the installed bundle. The standards and core-method additions are instruction-only;
project execution uses the target project's declared toolchain. Existing Python
pins and historical tested-environment records are preserved.

The principal distinctions are:

- Ten helper bundles have pinned Python package manifests. They can use separate
  project environments; no global Python package installation is necessary.
- Audio's outer helper uses standard library, while generation needs a separately
  provisioned Apple Silicon MLX runtime and verified weights. Discovery/archive
  helpers also use standard library.
- Browser verification selects one available backend with Chrome as the baseline.
  Installing Playwright CLI, Playwright MCP, project Playwright, and Computer Use
  together is not a requirement.
- Provider connections, native harness/reviewer capabilities, browser binaries,
  optional Office renderers, licensed fonts, and project toolchains are conditional.
  Installing a library does not expose an agent tool or authenticate a connector.

## Inventory

“None” means no additional utility for the stated baseline, not that an agent can
perform the workflow without its exposed file/tool capabilities. Versions below
are bundled pins, not recommendations to upgrade another project.

| Plugin / skill requirements | Baseline | Conditional setup |
| --- | --- | --- |
| coding / [apply-app-standards](../ai/plugins/coding/skills/apply-app-standards/references/requirements.md) | None for reading supplied artifacts | Declared project toolchain and official versioned documentation; setup separately authorized |
| coding / [apply-blockchain-standards](../ai/plugins/coding/skills/apply-blockchain-standards/references/requirements.md) | None for reading supplied artifacts | Declared project toolchain and official versioned documentation; setup separately authorized |
| coding / [apply-database-standards](../ai/plugins/coding/skills/apply-database-standards/references/requirements.md) | None for reading supplied artifacts | Declared project toolchain and official versioned documentation; setup separately authorized |
| coding / [apply-infrastructure-standards](../ai/plugins/coding/skills/apply-infrastructure-standards/references/requirements.md) | None for reading supplied artifacts | Declared project toolchain and official versioned documentation; setup separately authorized |
| coding / [apply-integration-standards](../ai/plugins/coding/skills/apply-integration-standards/references/requirements.md) | None for reading supplied artifacts | Declared project toolchain and official versioned documentation; setup separately authorized |
| coding / [apply-language-standards](../ai/plugins/coding/skills/apply-language-standards/references/requirements.md) | None for reading supplied artifacts | Declared project toolchain and official versioned documentation; setup separately authorized |
| coding / [apply-web-standards](../ai/plugins/coding/skills/apply-web-standards/references/requirements.md) | None for reading supplied artifacts | Declared project toolchain and official versioned documentation; setup separately authorized |
| coding / [apply-ai-standards](../ai/plugins/coding/skills/apply-ai-standards/references/requirements.md) | None for supplied evidence or planning | Existing project tools and separately scoped execution/access; no universal setup |
| coding / [operate-systems](../ai/plugins/coding/skills/operate-systems/references/requirements.md) | None for supplied evidence or planning | Existing project tools and separately scoped execution/access; no universal setup |
| coding / [assess-controls](../ai/plugins/coding/skills/assess-controls/references/requirements.md) | None for supplied evidence or planning | Existing project tools and separately scoped execution/access; no universal setup |
| researching / [analyze-data](../ai/plugins/researching/skills/analyze-data/references/requirements.md) | None for supplied evidence or planning | Existing project tools and separately scoped execution/access; no universal setup |
| researching / [research-users](../ai/plugins/researching/skills/research-users/references/requirements.md) | None for supplied evidence or planning | Existing project tools and separately scoped execution/access; no universal setup |
| reporting / [plan-product](../ai/plugins/reporting/skills/plan-product/references/requirements.md) | None for supplied evidence or planning | Existing project tools and separately scoped execution/access; no universal setup |
| producing / [write-content](../ai/plugins/producing/skills/write-content/references/requirements.md) | None for supplied evidence or planning | Existing project tools and separately scoped execution/access; no universal setup |
| producing / [design-interface](../ai/plugins/producing/skills/design-interface/references/requirements.md) | None for supplied evidence or planning | Existing project tools and separately scoped execution/access; no universal setup |
| delegating / [prepare-handoff](../ai/plugins/delegating/skills/prepare-handoff/references/requirements.md) | None for supplied evidence or planning | Existing project tools and separately scoped execution/access; no universal setup |
| coding / [create-mcp-server](../ai/plugins/coding/skills/create-mcp-server/references/requirements.md) | None for planning | Project runtime/package manager and selected MCP SDK; Inspector optional |
| coding / [create-skill](../ai/plugins/coding/skills/create-skill/references/requirements.md) | Python 3.11+; PyYAML 6.0.3 | Authorized model harness for actual evaluations |
| coding / [develop-code](../ai/plugins/coding/skills/develop-code/references/requirements.md) | None universal | Target project toolchain; Git for Git evidence |
| coding / [format-code](../ai/plugins/coding/skills/format-code/references/requirements.md) | None universal | Configured Ruff/pre-commit/Prettier/ESLint and project environment |
| coding / [manage-changes](../ai/plugins/coding/skills/manage-changes/references/requirements.md) | Git for shipping | GitHub CLI/access for GitHub delivery; project checks; git-cliff for requested changelog generation |
| coding / [map-codebase](../ai/plugins/coding/skills/map-codebase/references/requirements.md) | Native file/search access | ripgrep preferred shell search; Git for history/diffs |
| coding / [prepare-implementation](../ai/plugins/coding/skills/prepare-implementation/references/requirements.md) | None for planning | Adequate native file reads; optional Git/source parser for planning evidence |
| coding / [review-story](../ai/plugins/coding/skills/review-story/references/requirements.md) | Git and project read/search tools; complete workflow packet | Existing project check tools and prepared candidate for execute mode; native role/session support for delegation |
| coding / [resolve-review-feedback](../ai/plugins/coding/skills/resolve-review-feedback/references/requirements.md) | None for supplied feedback | Git; GitHub CLI/access for live feedback; project repair tools |
| coding / [review-code](../ai/plugins/coding/skills/review-code/references/requirements.md) | Native read/search access | Git/provider reads; existing project checks in authorized execute mode; no installs |
| coding / [run-agent-team](../ai/plugins/coding/skills/run-agent-team/references/requirements.md) | None for inspection/planning | Native worker/capacity/reviewer tools with main-session dispatch, authorized model use, Git and approved task worktrees; project checks; explicit model-selection controls only when needed to satisfy a user requirement, otherwise supported inheritance/defaults |
| coding / [run-tests](../ai/plugins/coding/skills/run-tests/references/requirements.md) | Project-configured runner | pytest/Vitest/coverage/services as configured; accessibility: project Playwright, `@axe-core/playwright` and resolved `axe-core`, browser/app fixture |
| coding / [archive-run](../ai/plugins/coding/skills/archive-run/references/requirements.md) | Python 3.11+, Git and POSIX | Exact-path archival authority; no packages or model/runtime dependency |
| coding / [verify-interface](../ai/plugins/coding/skills/verify-interface/references/requirements.md) | One exposed/installed browser backend | Chrome baseline; Node/CLI or MCP; Computer Use plugin; accessibility scans: project Playwright, `@axe-core/playwright` and resolved `axe-core`; other browsers targeted |
| coding / [write-requirements](../ai/plugins/coding/skills/write-requirements/references/requirements.md) | None for supplied context | Selected reader/research skill prerequisites |
| delegating / [use-subagents](../ai/plugins/delegating/skills/use-subagents/references/requirements.md) | POSIX shell; Python 3.11+ for discovery helper | Exposed native delegation capability/budget for invocation |
| producing / [create-audio](../ai/plugins/producing/skills/create-audio/references/requirements.md) | Python 3.11+ outer CLI | Generation: Apple Silicon macOS, Git, uv, pinned MLX source/weights and terms |
| producing / [create-docx](../ai/plugins/producing/skills/create-docx/references/requirements.md) | Python 3.11+; python-docx 1.2.0 | Word/LibreOffice and licensed recipient fonts for visual inspection |
| producing / [create-gif](../ai/plugins/producing/skills/create-gif/references/requirements.md) | Python 3.11+; Pillow 12.3.0 | Image provider only for requested generated frames |
| producing / [create-pdf](../ai/plugins/producing/skills/create-pdf/references/requirements.md) | Python 3.11+; ReportLab 4.4.9, pypdf 6.10.0, Pillow 12.3.0; supplied font input | Poppler raster previews; licensed font with required glyph coverage |
| producing / [create-pptx](../ai/plugins/producing/skills/create-pptx/references/requirements.md) | Python 3.11+; python-pptx 1.0.2, Pillow 12.3.0 | PowerPoint/LibreOffice, fonts, Poppler for visual inspection |
| producing / [create-sprites](../ai/plugins/producing/skills/create-sprites/references/requirements.md) | None for planning/supplied assets | Available native image tool or OpenCode V2/opencode-img/provider API key for generation; Godot only for integration |
| producing / [create-xlsx](../ai/plugins/producing/skills/create-xlsx/references/requirements.md) | Python 3.11+; XlsxWriter 3.2.9, openpyxl 3.1.5 | Excel/LibreOffice for recalculation/rendering |
| reporting / [assess-work-item](../ai/plugins/reporting/skills/assess-work-item/references/requirements.md) | None for supplied context | GitHub tools or installed gh fallback; Jira/Rovo connector; Git |
| reporting / [report-progress](../ai/plugins/reporting/skills/report-progress/references/requirements.md) | None for supplied evidence | Installed gh adapter; Jira/Rovo connector; Git |
| reporting / [report-project-status](../ai/plugins/reporting/skills/report-project-status/references/requirements.md) | None for supplied evidence | Installed gh adapter; Jira/Rovo connector; Git |
| researching / [read-docx](../ai/plugins/researching/skills/read-docx/references/requirements.md) | Python 3.11+; python-docx 1.2.0 | Normal package transitive dependencies |
| researching / [read-pdf](../ai/plugins/researching/skills/read-pdf/references/requirements.md) | Python 3.11+; pypdf 6.10.0 | No OCR or raster renderer shipped |
| researching / [read-pptx](../ai/plugins/researching/skills/read-pptx/references/requirements.md) | Python 3.11+; python-pptx 1.0.2 | Normal package transitive dependencies |
| researching / [read-xlsx](../ai/plugins/researching/skills/read-xlsx/references/requirements.md) | Python 3.11+; openpyxl 3.1.5 | No calculation engine shipped |
| researching / [search-web](../ai/plugins/researching/skills/search-web/references/requirements.md) | Exposed search/page-fetch capability for external research | Exa MCP optional; no universal CLI/package |

## Agent setup procedure

1. Read requirements from the advertised loaded skill, then select only the
   dependencies for the requested operation. Inspect availability through native
   tool schemas or bounded version/help checks.
2. Prefer the target project's existing interpreter, package manager, manifest,
   lockfile, and runtime version. For bundled Python helpers, follow their
   requirements file and use the shipped `requirements.txt`.
3. If a tool is absent, identify the exact blocker and prepare the documented
   setup command with real paths/approved versions. Existing authorization may
   cover project setup; global installs, model directories, configuration,
   authentication, services, and external writes retain their applicable scopes.
4. Install only when authorized. Replace placeholders before execution; choose
   fresh project-local environment paths and preserve existing environments.
   Homebrew examples assume it already exists; they do not install Homebrew.
   Platform-specific alternatives link to the utility's official instructions.
5. Rerun the availability check and then perform the requested verification.
   Report actual results. A dependency `check`, help output, or connection listing
   does not establish successful artifact generation, browser capture, or inference.

Avoid global pip, bare `npx` missing-tool downloads, and arbitrary latest package
versions. Project restore commands such as `npm ci` can replace dependencies and
run lifecycle scripts; inspect their effects. Do not run setup inside read-only
review/diagnosis scopes. No single installation command can provision every
skill's optional backend correctly.

## Delivery and evidence limits

Source checks for this audit: `make validate-ai` passed; five coding workflow
contract tests and one document discovery/resource-closure test passed.
A focused audit confirmed all 29 requirements links resolve within their bundles
and all ten `requirements.txt` hashes are unchanged. Direct helper Python imports
match the documented package families. `git diff --check` passed.
The create-skill helper's `check` and `validate` commands both exited 3 because
PyYAML is missing from the selected Python 3.11 interpreter; no package was
installed to bypass that limitation.

Requirements documents travel with their bundles through the existing authorized
AI/plugin installation workflow. Source changes do not update already installed
skills or a running agent's loaded context; refresh installation separately,
restart the harness, and verify discovery in a fresh task.

This documentation audit does not rerun each utility installation or live provider.
Existing document/artifact evidence remains in
[document skill verification](document-skill-verification.md); MCP authoring
evidence remains in [MCP skill verification](create-mcp-server-verification.md).
The skill-specific requirements distinguish tested environments from syntax
baselines and unverified pairings. Target application dependencies remain defined
by that application's manifests and instructions; the audit does not pretend to
enumerate every possible future project dependency.
