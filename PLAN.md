# Implementation plan: Producing and document skills

## Objective and context

- Source: [PRD](tasks/prd-producing-and-document-skills.md), FR-01–FR-31 and US-001–US-014.
- Objective: five native craft plugins with independently packaged media production,
  original document creation/reading, and portable skill-authoring workflows.
- Scope: producing registration, audio/sprite relocation, Apache-licensed
  create-skill/create-gif adaptations, eight original document skills, tests, and docs.
- Non-goals: PRD section 6; no proprietary Anthropic document sources, general Office
  editing, OCR, macro execution, automatic conversion, new providers, or installation.
- Current status: execution authorized; US-001 and US-003 delivered after their story commits. PRD remains the
  requirements source; this checklist owns implementation completion status.
- Working branch: `feat/producing-and-document-skills`, prepared with the committed
  plan and PRD before execution.
- Mode: standard; risk classification selects the shared review budget per story.
- Authorization: user approved implementation after the explicit request covering
  all 14 stories and per-story commits. Dependency installation remains separate.
- Delivery: one authorized commit per passing story; no implicit push or installation.
- Adapter: CodexGoalMarkdown for later authorized Codex execution. This Markdown
  choice does not start a Goal or Ralph run; Ralph requires its JSON adapter.

## Common implementation and verification contract

Each story inherits these requirements in addition to its own criteria:

- New skills contain matching SKILL.md frontmatter, scripts/, references/requirements.md,
  authoring.md or reading.md, validation.md, and requirements.txt. Extra resources
  must be justified and linked. Choose tested package constraints, not guessed pins.
- Python 3.11+ baseline; resources resolve from the installed skill. Outputs and
  temporary work remain project-local; inputs and installed resources are preserved.
- Refuse accidental output collisions and escaping paths. Provide bounded output,
  actionable dependency/input/generation/validation errors, and no implicit installs.
- Creation helpers expose prerequisite checks, narrow generation, and artifact
  inspection. Reading helpers expose prerequisite checks and source-located bounded
  extraction. Document CLI/input/output contracts before implementing them; avoid
  a universal document schema and sibling-skill Python imports.
- Write meaningful failing tests for behavior changes. Use independent output
  inspection, unchanged-input hashes, missing-dependency cases, invalid inputs,
  path/symlink boundaries, and collision/failure tests where relevant.
- Required source check: `make validate-ai`. Required final regression command:
  `python3.11 -m unittest discover -s tests -p '*test*.py'`.
- Focused tests: use `python3.11 -m unittest discover -s tests -p '<test_filename>'`
  for each named test below once created. New test paths are proposed, not existing
  commands claimed to have passed. Reuse existing test patterns and fixtures.
- Typecheck: no standalone repository target exists. Record unavailable explicitly;
  source validation and tests are not a substitute claim of a passing typecheck.
- Formatting/lint: no root pyproject.toml, Ruff, Prettier, or package.json configuration
  was found during planning. Inspect applicable configuration again during execution;
  run configured formatters on changed files before final verification. Report absent
  configuration/tools; do not install or introduce configuration without authorization.
- Run meaningful generation/extraction tests with dependencies available. Skips are
  explicit gaps, not successful verification. Report optional renderers separately;
  absent rendering must not become a claim of visual approval.
- No product UI is planned. If the adapted evaluation viewer is changed, use
  verify-interface for its browser behavior; unavailable required checks block delivery.
- Recommended read-only advisor for Python helper stories: @python-pro, only when
  useful and authorized under the shared budget (at most two advisors total per story).
  Bounded question: format-specific correctness, dependency compatibility, or proposed
  CLI/test contract. Executor owns edits/tests; advisor availability is checked at use.
- Staged reviewer: native story-reviewer when required by the shared mode/risk budget.
  No substitute reviewer or repeated fresh review sessions to bypass a blocker.

### Per-story execution checklist (apply to every story)

- [ ] Verify execution/commit authorization, exact branch, instructions, and state.
- [ ] Resolve this story's material gaps; research relevant library APIs with Context7.
- [ ] Add failing behavioral tests, implement scoped changes, and update related docs.
- [ ] Run configured formatting/lint, record unavailable typecheck, and run focused tests
  plus source validation; perform applicable artifact/browser verification.
- [ ] Stage only intended changes and follow the shared staged-review protocol.
- [ ] Resolve findings and rerun affected checks; at most one targeted same-session pass.
- [ ] Update validated memory and append progress; mark delivered only after the
  authorized story commit succeeds. Do not check this reusable template as a batch
  completion record; record each story's evidence in docs/progress.md.

## Ordered stories

### US-001 — Register producing and relocate media skills
- [x] Story complete
- Priority: 1
- Depends on: none
- Requirements: PRD US-001; FR-01–FR-04.
- Benefit: users discover media workflows under their own craft.
- Paths: .agents/plugins/marketplace.json, ai/plugins/producing/.codex-plugin/plugin.json,
  coding/producing skill directories, scripts/install-ai.py, .vscode/settings.json,
  tests/ai_install_test.py, tests/plugin_test.py, audio tests, README.md, AGENTS.md,
  docs/ai-configuration.md.
- [ ] Manifest description is exactly “Creative asset and document production workflows.”
- [ ] Move complete audio/sprite bundles, preserving bytes and file modes; retain names
  and command references. No duplicate skills or old active source links remain.
- [ ] Update exact-four guard and fixtures to five; retain generic installation loops.
- [ ] Inventory docs and audio/editor import paths reflect the move immediately.
- [ ] Focused installer/plugin/audio generation/audio service regressions pass;
  common typecheck, formatting, source-validation, and review gates pass.

### US-002 — Adapt create-skill
- [ ] Story complete
- Priority: 2
- Depends on: US-001
- Requirements: PRD US-002; FR-05–FR-17, FR-31.
- Benefit: assistants author and evaluate repository-conformant skills portably.
- Paths: ai/plugins/coding/skills/create-skill/, tests/create_skill_test.py.
- [ ] Import only the Apache skill-creator bundle from the inspected local clone;
  retain license, applicable notices, upstream commit, and modified-file notices.
- [ ] Portable authoring/evaluation uses project workspaces and installed resources;
  preserve schema/report helpers without assuming native agents or token metrics.
- [ ] Claude CLI adapters are optional, explicitly scoped, and never auto-invoked.
  Document their dependencies separately; no automatic servers or global changes.
- [ ] Validate packaging, local evaluation/report helpers, missing dependencies, and
  writable-path boundaries. Browser-check any modified viewer using verify-interface.
- [ ] Common verification and review gates pass.

### US-003 — Adapt GIF assembly and inspection
- [x] Story complete
- Priority: 3
- Depends on: US-001
- Requirements: PRD US-003; FR-05–FR-14, FR-18, FR-21–FR-23, FR-31.
- Benefit: users generate correctly timed GIFs without needing an AI provider.
- Paths: ai/plugins/producing/skills/create-gif/, tests/create_gif_test.py.
- [ ] Preserve Apache license/provenance/notices; move execution helpers under scripts/.
  Prefer Pillow; justify any retained ImageIO/NumPy dependency through actual usage.
- [ ] Supplied frames and procedural graphics have documented CLI/contracts; explicit
  timing, loop, palette, transparency/background, and aspect-preserving resize policies.
- [ ] Tests prove duplicate/frame reduction preserves elapsed time, variable-duration
  inspection sums decoded durations, and pixel-art sampling preserves intended edges.
- [ ] Validate disposal/background behavior, actual size/format/loop metadata, invalid
  inputs, output limits, and collisions. Account for encoded timing precision.
- [ ] Conditional Slack reference separates presets from verified limits; common gates pass.

### US-004 — Add AI-assisted GIF workflow
- [ ] Story complete
- Priority: 4
- Depends on: US-003
- Requirements: PRD US-004; FR-19–FR-20.
- Benefit: users can request original animated artwork when provider support exists.
- Paths: create-gif/SKILL.md and references/, relevant routing fixtures under tests/.
- [ ] Check active tool schemas; use create-sprites for pixel art and a suitable
  available provider for other artwork. Never assume Codex has OpenCode image tools.
- [ ] Distinguish static-image motion from articulated poses; inspect frame alignment,
  style consistency, backgrounds, timing, and loop continuity before final delivery.
- [ ] Evaluate supplied-assets, procedural, AI pixel-art, AI illustration, and absent-
  provider scenarios. Non-AI paths remain usable; no automatic generation/spending.
- [ ] Report instruction evaluations separately from authorized live generation;
  common verification and review gates pass (typecheck unavailable for prose).

### US-005 — Create DOCX documents
- [ ] Story complete
- Priority: 5
- Depends on: US-001
- Requirements: PRD US-005; FR-05–FR-14, FR-24, FR-26.
- Benefit: users produce structured Word documents with explicit layout.
- Paths: ai/plugins/producing/skills/create-docx/, tests/create_docx_test.py.
- [ ] Original python-docx helpers/recipes cover headings/styles, paragraphs, tables,
  inline images, sections, dimensions, margins, and page breaks.
- [ ] Reopen outputs to verify Unicode content, styles, tables, image relationships,
  and layout settings. Test missing dependencies and failed-output/input preservation.
- [ ] Document tested recipes and font/rendering/template limitations without claiming
  pagination verification from package checks alone; common gates pass.

### US-006 — Read DOCX documents
- [ ] Story complete
- Priority: 6
- Depends on: US-005
- Requirements: PRD US-006; FR-05–FR-14, FR-27–FR-30.
- Benefit: assistants extract ordered Word content with useful source locations.
- Paths: ai/plugins/researching/skills/read-docx/, tests/read_docx_test.py.
- [ ] Research current ordered-block/header/footer APIs; define bounded extraction
  with paragraph/table locations, headings, header/footer context, and omissions.
- [ ] Tests cover interleaved paragraphs/tables, headers/footers, unsupported structures,
  truncation, and unchanged source hashes; no tracked-change acceptance.
- [ ] Skill is independent of create-docx at runtime; common gates pass.

### US-007 — Create PPTX presentations
- [ ] Story complete
- Priority: 7
- Depends on: US-001
- Requirements: PRD US-007; FR-05–FR-14, FR-24, FR-26.
- Benefit: users produce editable slides with deliberate layouts.
- Paths: ai/plugins/producing/skills/create-pptx/, tests/create_pptx_test.py.
- [ ] Original python-pptx helpers/recipes cover slide geometry, inspected layouts and
  placeholders, text, images, tables, and supported native charts.
- [ ] Tests reopen outputs for slide count, content, chart data, and geometry;
  template selection does not assume unexplained layout indices.
- [ ] Document overflow/font-fit limits; inspect rendered slides where available for
  clipping, overlap, readability, and consistency. Report unavailable rendering.
- [ ] Common verification and review gates pass.

### US-008 — Read PPTX presentations
- [ ] Story complete
- Priority: 8
- Depends on: US-007
- Requirements: PRD US-008; FR-05–FR-14, FR-27–FR-30.
- Benefit: assistants analyze slide-located content without modifying presentations.
- Paths: ai/plugins/researching/skills/read-pptx/, tests/read_pptx_test.py.
- [ ] Research notes/chart/table APIs; extract supported text, notes, tables, and
  chart values with slide selection, source locations, and bounded output.
- [ ] Identify visual-only/unsupported content and truncation; fixtures verify notes,
  tables, charts, selected slides, and preserved sources.
- [ ] Skill runs without create-pptx imports; common gates pass.

### US-009 — Create XLSX workbooks
- [ ] Story complete
- Priority: 9
- Depends on: US-001
- Requirements: PRD US-009; FR-05–FR-14, FR-24–FR-26.
- Benefit: users obtain typed/formatted workbooks with trustworthy formula reporting.
- Paths: ai/plugins/producing/skills/create-xlsx/, tests/create_xlsx_test.py.
- [ ] Original XlsxWriter helpers/recipes cover sheets, explicit types/formats, tables,
  filters, freeze panes, charts, and explicit formulas. No implicit string conversion.
- [ ] Tests preserve leading zeros, formula-like strings, and literal URLs; check
  sheet names, malformed rows, writer errors, truncation, and collisions.
- [ ] Independently inspect formulas/caches/calculation settings; distinguish supplied
  cached values from actual recalculation. Do not imply a calculation engine exists.
- [ ] Common verification and review gates pass.

### US-010 — Read XLSX workbooks
- [ ] Story complete
- Priority: 10
- Depends on: US-009
- Requirements: PRD US-010; FR-05–FR-14, FR-27–FR-30.
- Benefit: assistants inspect precise workbook data without changing it.
- Paths: ai/plugins/researching/skills/read-xlsx/, tests/read_xlsx_test.py.
- [ ] Original openpyxl reader reports sheet/range coordinates, cell types, formulas,
  cached values, hidden sheets/rows/columns, and explicit extraction limits.
- [ ] Tests distinguish missing caches from calculated values; verify bounded ranges,
  literal data, hidden content, and unchanged hashes. No save, recalculation, or refresh.
- [ ] Skill runs without the creation skill; common gates pass.

### US-011 — Create PDFs
- [ ] Story complete
- Priority: 11
- Depends on: US-001
- Requirements: PRD US-011; FR-05–FR-14, FR-24, FR-26.
- Benefit: users produce paginated documents with explicit fonts and layout.
- Paths: ai/plugins/producing/skills/create-pdf/, tests/create_pdf_test.py.
- [ ] Original ReportLab helpers/recipes cover headings, paragraphs, tables, images,
  fonts, page breaks, and page numbers; pypdf supplies independent output inspection.
- [ ] Tests cover escaped markup, multipage output, tables, oversized content,
  missing fonts, page geometry, expected text, and failed publication.
- [ ] Select an approved font fixture for glyph tests; distinguish glyph coverage,
  extraction, pagination structure, and actual visual verification.
- [ ] Common verification and review gates pass.

### US-012 — Read PDFs
- [ ] Story complete
- Priority: 12
- Depends on: US-011
- Requirements: PRD US-012; FR-05–FR-14, FR-27–FR-30.
- Benefit: assistants extract page-located evidence with honest completeness reports.
- Paths: ai/plugins/researching/skills/read-pdf/, tests/read_pdf_test.py.
- [ ] Research current pypdf extraction APIs; define page selection, metadata,
  bounded text, and explicit missing-text/possible-scan indicators.
- [ ] Tests cover multipage selection, image-only pages, malformed documents,
  truncation, and unchanged sources. Empty extraction never implies empty content.
- [ ] No OCR/table-reconstruction promise. pdfplumber remains an optional future
  choice unless a justified, verified in-scope operation needs it; common gates pass.

### US-013 — Verify isolated packaging and integration
- [ ] Story complete
- Priority: 13
- Depends on: US-002, US-004, US-006, US-008, US-010, US-012
- Requirements: PRD US-013; FR-04–FR-14, FR-31.
- Benefit: users can invoke each installed skill independently of the checkout.
- Paths: tests/document_skills_contract_test.py, tests/ai_install_test.py,
  tests/plugin_test.py, affected skill references and package resources.
- [ ] Copy each of the ten new skills into isolated project-local fixtures and invoke
  helpers from unrelated working directories; dependencies are explicit, not inherited.
- [ ] Verify resource/link closure, requirements, attribution, unique discovery, no
  sibling imports, and unchanged installed resources. Include missing-package cases.
- [ ] Resolve required dependency-test gaps; skips do not establish working generation.
- [ ] Run complete Python regression suite and make validate-ai; common gates pass.

### US-014 — Finalize documentation and activation instructions
- [ ] Story complete
- Priority: 14
- Depends on: US-013
- Requirements: PRD US-014; all final ownership and delivery criteria.
- Benefit: users understand plugin ownership, prerequisites, and safe activation.
- Paths: README.md, AGENTS.md, docs/ai-configuration.md, docs/remove-old-ai-files.md.
- [ ] Inventory lists seven producing skills, create-skill in coding, and four readers
  in researching. Explain production versus research/reporting and native simple reads.
- [ ] Document coordinated Codex refresh and OpenCode copies, restart/new-thread steps,
  preservation of custom copies, and separately authorized installation/cleanup.
- [ ] Dependency setup is separate from AI installation; no manual plugin-cache deletion.
- [ ] Check active links/paths, record actual final verification and limitations in
  progress, and satisfy common gates. No global installation is a validation step.

## Material gaps before or during execution

- Prepared branch and implementation/per-story commit authorization are satisfied.
- Required dependency installations need authorization; no environment was provisioned.
- Verify upstream clone/commit and Apache notices before adapting either licensed skill.
- Select tested dependency constraints, extraction schemas/limits, GIF dependency set,
  licensed font fixtures, and available native renderers within the owning stories.
- Use Context7 and official documentation for original helpers; never consult or copy
  Anthropic's proprietary document implementations. No additional agent delegation
  is granted by this plan alone.

## Resume and delivery

- For authorized execution, load the installed prepare-implementation skill and read
  references/story-execution.md and references/story-review.md in full relative to
  its reported base directory. Follow CodexGoalMarkdown. Stop if discovery, references,
  or required native story-reviewer invocation is unavailable; do not guess paths.
- Select the lowest-priority-number eligible incomplete story. Recheck the exact
  prepared branch before writes, staging, and commits. Never create/switch branches
  as part of this execution adapter or accept main/master/detached HEAD.
- Read relevant latest worktree-root docs/progress.md entries and memory.json if
  present. Keep this plan limited to requirements, completion, and concise status.
  Append commands/results, review findings/dispositions, approvals, blockers, actual
  runtime/model/mode, advisor use, reviewer session provenance, and commit outcomes
  to docs/progress.md. Create it only at an authorized execution checkpoint.
- Missing memory is normal: use empty version-1 memory in process. Invalid memory
  blocks without overwrite. Create/update bounded memory only after passing review,
  retaining at most 20 patterns and 20 evidenced suppressions.
- Apply shared fast/standard/deep risk budgets. Self-review is allowed only where
  the budget permits and is not independent review. Native review uses story-reviewer,
  the full shared JSON protocol, Review profile expanded-initial, and explicit Pass
  type. Allow one initial and at most one targeted pass in the same actual native
  session per attempt. Preserve reading/evidence recovery limits and coverage tracking.
- Final blocked or malformed review stops delivery; preserve the candidate, findings,
  and consumed passes. Resume only after verifying the required material resolution;
  continuation, a new reviewer, or compaction does not reset review budgets.
- Stage provisional completion only after checks/review pass. Delivery requires a
  successful authorized per-story commit. On failed finalization restore only the
  provisional completion marker and append the actual blocker; preserve other work.
- No implicit push, external post, sensitive operation, or installation. Planning
  creates neither execution journal nor memory. Native Goal continuation does not
  introduce Ralph's external iteration loop or new compaction hooks.
- [ ] Final report lists actual commits, checks/reviews, delivered scope, and gaps.
- After all stories pass and are committed, offer separately authorized archival
  using the installed references/completed-run-archive.md. Never reset active state
  or commit archives under story-commit authorization alone.
