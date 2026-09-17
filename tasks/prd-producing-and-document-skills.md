# PRD: Producing Plugin and Document Skills

**Status:** Draft based on the approved plan

## 1. Overview

The dotfiles repository needs a dedicated plugin for creative asset and document
production. Audio and sprite generation currently reside in `coding`, while
document creation, document reading, and skill-authoring workflows need explicit
ownership.

This change introduces `producing@craft`, relocates existing media skills, adapts
two Apache-licensed Anthropic skills, and creates original Python-based document
creation and reading skills.

The primary users are the repository owner and LLM assistants operating through
OpenCode or Codex. Skills must describe their capabilities accurately, resolve
their bundled resources from installed locations, and report missing dependencies
or unavailable verification capabilities.

## 2. Goals

1. Establish a five-plugin marketplace with unique ownership of each skill.
2. Separate artifact production, document research, and skill authoring.
3. Support GIF production from supplied assets, procedural graphics, and optional
   AI-generated artwork.
4. Provide original creation and reading workflows for DOCX, PPTX, XLSX, and PDF.
5. Document dependencies, execution procedures, references, and validation for
   each new skill.
6. Preserve existing audio and sprite behavior during relocation.
7. Verify bundled helpers and installation discovery through meaningful local
   tests.
8. Preserve upstream licenses and attribution for adapted skills.

## 3. Scope and Ownership

| Plugin | Required changes |
| --- | --- |
| `producing` | Add plugin; own `create-audio`, `create-sprites`, `create-gif`, `create-docx`, `create-pptx`, `create-xlsx`, `create-pdf` |
| `coding` | Add `create-skill`; remove ownership of relocated audio and sprite skills |
| `researching` | Add `read-docx`, `read-pptx`, `read-xlsx`, `read-pdf` |
| `reporting` | Retain ownership of report content, evidence synthesis, and communication |
| `delegating` | Retain existing ownership |

The new plugin description must be:

> Creative asset and document production workflows.

### Source policy

- `create-audio` and `create-sprites`: existing repository sources.
- `create-skill`: adaptation of Anthropic's Apache-2.0 `skill-creator`.
- `create-gif`: adaptation of Anthropic's Apache-2.0 `slack-gif-creator`.
- Document creation and reading skills: original implementations based on
  requirements and library documentation.
- Anthropic's proprietary DOCX, PPTX, XLSX, and PDF skills must not supply
  implementation code, prompts, schemas, assets, or adapted documentation.

## 4. Functional Requirements

### Plugin registration and migration

**FR-01.** Register `producing` as a checkout-local plugin in
`.agents/plugins/marketplace.json`, following existing native manifest and
installation-policy conventions.

**FR-02.** Move complete audio and sprite skill directories into `producing`,
preserving their skill identifiers, bundled resources, and behavior.

**FR-03.** Update the installer's plugin-count invariant, fixtures, inventories,
and active source-path references for five plugins.

**FR-04.** Each skill identifier must occur exactly once in the marketplace.
Existing commands that resolve skills by name must continue to resolve the
relocated skills.

### Skill packaging

**FR-05.** Each new skill must include:

- `SKILL.md` with matching directory and frontmatter names.
- Detailed reference documentation under `references/`.
- Execution helpers under `scripts/`.
- `references/requirements.md`.
- `requirements.txt` for its required Python runtime packages.

**FR-06.** References must be linked using paths relative to the installed skill.
Execution must not depend on the dotfiles checkout, a sibling skill's Python
modules, or a hardcoded plugin cache.

**FR-07.** Additional resource directories are permitted when justified by the
adapted tools, such as evaluation templates. Their purpose and resolution must be
documented.

### Dependency requirements

**FR-08.** Dependency documentation must distinguish:

- Required Python version and packages.
- Optional packages by operation.
- Optional native rendering/conversion tools.
- Fonts and their availability or licensing requirements.
- Harness-specific capabilities.

**FR-09.** Helpers must report missing prerequisites without installing packages,
downloading models, changing global configuration, or provisioning services.

**FR-10.** Package constraints must be selected through compatibility
verification. Documentation must record tested versions without presenting
untested versions as supported.

### Runtime behavior

**FR-11.** Installed skill directories are read-only resources. Outputs,
temporary work, generated scripts, and evaluation artifacts belong in the active
project.

**FR-12.** Helpers must preserve source files, refuse output collisions by
default, and reject paths that escape their documented project boundary.

**FR-13.** Helpers must provide actionable errors and distinguish dependency,
input, generation, and validation failures. Diagnostics must not unnecessarily
expose full document contents.

**FR-14.** Validation must inspect generated artifacts rather than relying solely
on successful library calls. Structural correctness, content correctness, and
visual quality must be reported separately.

### Skill authoring

**FR-15.** `create-skill` must support intent capture, authoring, representative
evaluations, evidence review, and iterative improvement using repository
conventions.

**FR-16.** Its portable workflow must not assume Claude-specific tools, subagent
access, token metrics, background servers, or writable installed directories.

**FR-17.** Retained Claude-specific evaluation utilities must be documented as
optional adapters and invoked only when available and authorized.

### GIF production

**FR-18.** `create-gif` must support supplied frames/images and appropriate
procedural graphics without requiring an AI image provider.

**FR-19.** It must offer an optional AI-artwork workflow when the active harness
exposes a suitable generation tool. Pixel-art requests must use the
`create-sprites` workflow.

**FR-20.** It must distinguish animation of a static image from articulated
motion requiring distinct poses. Generated frame sheets must be inspected for
alignment, consistency, and loop continuity.

**FR-21.** Encoding must expose documented choices for dimensions, frame timing,
looping, palette, resizing, and transparency/background handling.

**FR-22.** Optimization must preserve elapsed animation time. Output inspection
must read individual frame durations and report actual dimensions, size, format,
and loop metadata.

**FR-23.** Slack guidance must reside in a conditional reference and distinguish
suggested presets from verified destination limits.

### Document creation

**FR-24.** Creation skills must support the following initial capabilities:

| Skill | Required capabilities |
| --- | --- |
| `create-docx` | Semantic headings/styles, paragraphs, tables, inline images, section dimensions, margins, and page breaks |
| `create-pptx` | Explicit slide geometry, layouts/placeholders, editable text, images, tables, and supported native charts |
| `create-xlsx` | Explicit cell types, formats, worksheets, tables, filters, freeze panes, charts, and formulas |
| `create-pdf` | Paginated paragraphs, headings, tables, images, explicit fonts, page breaks, and page numbering |

Capabilities may be delivered through focused helpers and documented, tested
Python recipes; a universal document schema is not required.

**FR-25.** Spreadsheet generation must preserve literal inputs unless conversion
is explicit. Formula strings, cached results, and recalculation must be
distinguished.

**FR-26.** Creation skills must explain font, rendering, layout, and library
limitations. They must not claim visual verification when rendering or inspection
is unavailable.

### Document reading

**FR-27.** Reading skills must provide bounded, source-located extraction:

| Skill | Required extraction |
| --- | --- |
| `read-docx` | Ordered paragraphs/tables, headings, headers/footers, and explicit notices for unsupported structures |
| `read-pptx` | Slide-located text, speaker notes, tables, and supported chart data |
| `read-xlsx` | Sheet/range selection, cell coordinates/types, formulas, cached values, and hidden-content indicators |
| `read-pdf` | Page selection, page-located text, metadata, and indicators of insufficient text extraction or possible scans |

**FR-28.** Readers must report omissions, truncation, and unsupported content.
Empty extraction must not be presented as proof that a document contains no
information.

**FR-29.** Reading must not modify inputs, silently recalculate formulas, refresh
external links, accept tracked changes, or execute embedded content.

**FR-30.** Reading descriptions must clearly match document inspection/extraction
requests. Creation descriptions must match production requests. Skills must not
require their use when a native tool adequately handles a simple read.

### Licensing and provenance

**FR-31.** Apache adaptations must retain their license, applicable attribution,
upstream provenance, and relevant notices. Modified files must carry prominent
change notices.

## 5. User Stories and Acceptance Criteria

### Common verification gate

Every implementation story must satisfy this gate:

- [ ] Relevant regression tests pass; testable behavior changes begin with
  meaningful failing tests.
- [ ] Configured formatters run on changed files, or their unavailability is
  recorded.
- [ ] Typecheck passes if a project typecheck is available. Currently none exists;
  record that explicitly and use source validation and relevant tests without
  claiming a typecheck passed.
- [ ] Verification limitations and skipped integration checks are explicit.

### US-001: Establish producing and relocate existing media skills

**Description:** As a repository owner, I want media generation grouped under
`producing` so plugin ownership reflects its purpose.

- [ ] Native manifest and marketplace registration define `producing`.
- [ ] Audio and sprite directories are fully relocated with identifiers preserved.
- [ ] Exactly five plugins pass inventory validation.
- [ ] Audio test paths, editor paths, and active documentation links are updated.
- [ ] No duplicate audio/sprite skill identifiers remain.
- [ ] Existing audio regression tests and installer tests pass.
- [ ] Common verification gate passes.

### US-002: Adapt skill authoring to repository conventions

**Description:** As an assistant, I want `create-skill` to author and evaluate
portable skills using the repository's conventions.

- [ ] Skill is owned by `coding`.
- [ ] Portable authoring instructions work without a Claude CLI assumption.
- [ ] Evaluation outputs use project-local paths.
- [ ] Optional Claude adapters and evaluation dependencies are documented.
- [ ] Delegation and metric collection depend on available capabilities and
  authorization.
- [ ] License, provenance, and modified-file notices are present.
- [ ] Common verification gate passes.

### US-003: Adapt GIF assembly and validation

**Description:** As a user, I want supplied frames and procedural graphics encoded
into correctly timed GIFs.

- [ ] Skill is owned by `producing` and named `create-gif`.
- [ ] Encoding options and supported transparency behavior are documented.
- [ ] Frame reduction and deduplication preserve duration.
- [ ] Variable-duration output is inspected correctly.
- [ ] Resizing preserves aspect ratio and supports pixel-art sampling.
- [ ] Tests cover timing, disposal/background behavior, output limits, and
  collisions.
- [ ] License and provenance requirements are satisfied.
- [ ] Common verification gate passes.

### US-004: Add optional AI-assisted GIF production

**Description:** As a user, I want original AI artwork incorporated into GIFs when
a suitable provider is available.

- [ ] Workflow checks exposed provider capabilities before generation.
- [ ] Pixel-art generation follows `create-sprites`.
- [ ] Static-image effects and articulated animation are distinguished.
- [ ] Frame-sheet alignment, consistency, and loop review are required.
- [ ] Provider absence still permits supplied-asset and procedural workflows.
- [ ] Representative routing scenarios are evaluated; live generation is reported
  separately from instruction checks.
- [ ] Common verification gate passes.

### US-005: Create Word documents

**Description:** As a user, I want DOCX documents with structured content and
explicit layout.

- [ ] `create-docx` supports FR-24 through helpers and tested recipes.
- [ ] Reopened outputs preserve expected text, headings, tables, images, and
  section settings.
- [ ] Requirements and rendering limitations are documented.
- [ ] Tests cover Unicode text, layout metadata, input preservation, and failed
  output publication.
- [ ] Common verification gate passes.

### US-006: Read Word documents

**Description:** As an assistant, I want structured DOCX extraction with useful
source locations.

- [ ] `read-docx` preserves paragraph/table order for supported structures.
- [ ] Headers, footers, and headings are identifiable.
- [ ] Output identifies location and extraction limitations.
- [ ] Tests include interleaved paragraphs/tables and unsupported-content reporting.
- [ ] Source hashes remain unchanged.
- [ ] Common verification gate passes.

### US-007: Create PowerPoint presentations

**Description:** As a user, I want editable presentations with deliberate layouts.

- [ ] `create-pptx` supports FR-24.
- [ ] Template layouts/placeholders are inspected rather than selected through
  unexplained hardcoded indices.
- [ ] Output checks verify slide counts, geometry, text, and chart data.
- [ ] Visual review covers clipping, overlap, readability, and consistency when
  rendering is available.
- [ ] Unavailable rendering is reported.
- [ ] Common verification gate passes.

### US-008: Read PowerPoint presentations

**Description:** As an assistant, I want slide-located content for analysis and
summarization.

- [ ] `read-pptx` extracts supported text, notes, tables, and chart values.
- [ ] Slide selection and bounded output are supported.
- [ ] Visual-only and unsupported content is identified.
- [ ] Tests verify locations, notes, chart/table extraction, and unchanged inputs.
- [ ] Common verification gate passes.

### US-009: Create Excel workbooks

**Description:** As a user, I want workbooks with trustworthy data types,
formatting, and formulas.

- [ ] `create-xlsx` supports FR-24.
- [ ] Literal imports preserve leading zeros and formula-like strings.
- [ ] Formula generation is explicit.
- [ ] Reports distinguish stored formulas, supplied caches, and verified
  recalculation.
- [ ] Writer errors and truncation are detected.
- [ ] Tests cover cell types, special strings, formulas/caches, sheet names, and
  output preservation.
- [ ] Common verification gate passes.

### US-010: Read Excel workbooks

**Description:** As an assistant, I want precise workbook inspection without
altering its contents.

- [ ] `read-xlsx` supports sheet/range selection and cell coordinates.
- [ ] Formula and cached-value views are distinguishable.
- [ ] Hidden sheets, rows, and columns are represented or explicitly reported.
- [ ] Missing cached results are not treated as calculated values.
- [ ] Tests verify extraction bounds, types, hidden content, and unchanged inputs.
- [ ] Common verification gate passes.

### US-011: Create PDFs

**Description:** As a user, I want readable paginated PDFs with explicit font and
layout choices.

- [ ] `create-pdf` supports FR-24.
- [ ] Supplied text is escaped before use in markup-aware paragraphs.
- [ ] Tests cover multipage output, special characters, tables, oversized content,
  and missing fonts.
- [ ] Structural checks verify page geometry and expected extracted text.
- [ ] Glyph coverage and visual checks are reported separately.
- [ ] Common verification gate passes.

### US-012: Read PDFs

**Description:** As an assistant, I want page-located PDF extraction with honest
completeness reporting.

- [ ] `read-pdf` supports page selection, metadata, and bounded text extraction.
- [ ] Pages with insufficient extractable text are flagged for further inspection.
- [ ] It does not claim OCR or reliable table reconstruction unless those
  capabilities are explicitly implemented and verified.
- [ ] Tests cover multipage text, selection, image-only pages, malformed inputs,
  and unchanged sources.
- [ ] Common verification gate passes.

### US-013: Verify independent skill packaging

**Description:** As a user, I want installed skills to work independently of the
source checkout.

- [ ] Each new skill is copied into an isolated project-local installation fixture.
- [ ] Helpers run from an unrelated working directory.
- [ ] Linked references, scripts, dependencies, licenses, and required assets are
  present.
- [ ] No sibling-skill Python import or hardcoded checkout path is required.
- [ ] Missing dependencies produce actionable reports.
- [ ] Installed resources remain unchanged during execution.
- [ ] Common verification gate passes.

### US-014: Document ownership and activation

**Description:** As a repository owner, I want accurate setup and migration
instructions.

- [ ] README, repository AGENTS, and AI configuration documentation show final
  ownership.
- [ ] Codex refresh guidance covers updated coding/researching content and new
  producing registration.
- [ ] OpenCode copy behavior and unchanged relocated skill names are explained.
- [ ] Restart and new-thread requirements are documented.
- [ ] Dependency setup remains separate from AI configuration installation.
- [ ] Final validation results and unavailable checks are reported.

## 6. Non-Goals

This release does not require:

- General editing or lossless round-trip preservation of arbitrary Office
  documents.
- OCR, video-to-GIF conversion, or automatic Office conversion.
- Macro execution, external-data refresh, or embedded-content execution.
- PDF signatures, forms, PDF/A certification, or tagged-PDF accessibility
  certification.
- A shared universal document schema or office-automation framework.
- New native agents, chat providers, MCP services, or slash commands.
- Dependency bootstrap, model provisioning, or global installation during
  validation.
- Live AI generation as a prerequisite for non-AI GIF workflows.

## 7. Technical Considerations

### Selected initial libraries

| Capability | Library |
| --- | --- |
| DOCX creation/reading | `python-docx` |
| PPTX creation/reading | `python-pptx` |
| XLSX creation | XlsxWriter |
| XLSX reading | `openpyxl` |
| PDF creation | ReportLab |
| PDF reading/inspection | `pypdf` |
| GIF processing/encoding | Pillow preferred; retain ImageIO/NumPy only where justified by adapted helpers |

Use Python 3.11+ as the initial repository-aligned baseline, subject to tested
dependency compatibility.

### Important limitations

- Spreadsheet libraries do not supply a spreadsheet calculation engine.
- Office structure checks do not prove rendered pagination or slide appearance.
- PDF text extraction does not reconstruct all visual meaning.
- Fonts and glyph coverage must be checked explicitly.
- Image-generation availability differs between harnesses.
- Documentation facts and locally tested behavior must be distinguished.

### Required repository checks

```sh
make validate-ai
python3.11 -m unittest discover -s tests -p '*test*.py'
```

Use additional focused checks where the changed behavior requires them. Do not
interpret skipped generation tests as proof that a format implementation works.

## 8. Success Criteria

The feature is complete when:

1. Five plugins validate with unique skill ownership.
2. Audio and sprite relocation passes relevant regressions.
3. Both Apache adaptations include required notices and provenance.
4. All eight original document skills are discoverable and independently packaged.
5. Representative creation and extraction fixtures pass for each document format.
6. GIF tests demonstrate preserved timing and correct output inspection.
7. Dependencies and optional capabilities are documented per skill.
8. Native rendering, live AI generation, and unavailable checks are reported
   accurately.
9. No global installation or dependency provisioning occurs as a validation side
   effect.

## 9. Remaining Implementation Decisions

These do not change the approved scope but must be resolved and recorded during
implementation:

- Tested package-version constraints for each skill.
- Whether GIF helpers retain ImageIO/NumPy after adaptation.
- Exact extraction output schemas and bounded-output defaults.
- Font fixtures and redistribution terms for Unicode/layout tests.
- Available renderers for DOCX/PPTX/PDF visual verification.
- Whether optional PDF table extraction warrants `pdfplumber`; baseline PDF
  reading must not imply that capability.
