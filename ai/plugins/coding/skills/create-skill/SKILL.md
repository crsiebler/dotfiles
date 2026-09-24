---
name: create-skill
description: Author, adapt, and evaluate portable skills with representative task evidence and iterative improvement. Use for creating skills or improving their instructions and discovery descriptions.
---

# Create Skill

Use the user's workflow and artifacts to define purpose, triggers, output, and
success. Ask only for material missing information. Preserve the requested scope;
creating a skill does not authorize its external effects, installation, or spending.

Read [authoring and CLI contracts](references/authoring.md) before writing a new
bundle or running helpers. Use [requirements](references/requirements.md) to check
prerequisites. Resolve `scripts/create_skill.py` from this loaded skill, regardless
of the working directory; all writable paths belong in the active project.

1. Draft a concise SKILL.md with a matching action-oriented directory/name and a
   precise description. Put conditional detail in linked references; include scripts
   only for reusable operations. Follow repository packaging conventions.
2. Choose representative requests, difficult cases, and nearby non-trigger cases.
   Define observable expectations and keep some requests held out for later checks.
   Record them using the [evaluation schemas](references/schemas.md).
3. Run authorized cases with and without the skill (or compare revisions). Use the
   actual available harness; sequential execution is valid. Native agents, background
   jobs, and token telemetry are optional, never assumed. Delegate only if authorized.
4. Inspect actual artifacts and grade with evidence. Read the
   [grader](references/grader.md), [blind comparator](references/comparator.md), or
   [analyzer](references/analyzer.md) prompt only when that evaluation mode is useful.
   These are reference prompts, not installed native agents or commands.
5. Aggregate recorded evidence and generate a Markdown report with the portable
   helpers. Review subjective quality separately; counts alone cannot prove it.
   Revise concrete failures, then rerun affected and held-out cases. Record limitations
   and stop when the agreed outcomes are met or a missing capability needs resolution.

Follow [validation](references/validation.md) before delivering a bundle. Package a
project copy only after validation; never overwrite an installed skill or existing
output. [Optional Claude adapters](references/claude-adapters.md) are a separate,
explicitly authorized workflow, never an automatic prerequisite or fallback.

Modified 2026-09-17 from Anthropic skill-creator, Apache-2.0; see
[provenance](references/provenance.md) and [license](LICENSE.txt).
