# Provenance and adaptations

Source: Anthropic [skills repository](https://github.com/anthropics/skills),
`skills/skill-creator`, commit `34040c9c568585f6929bedeaad110ad08f079624`.
The clean local clone was inspected before adaptation. Only this Apache-2.0 bundle
was consulted; no proprietary document skill sources were used.

[LICENSE.txt](../LICENSE.txt) is copied unchanged. The selected bundle contains no
separate NOTICE file. Anthropic attribution and modified-file notices are retained
in adapted instructions, schemas, prompts, and helpers.

Adapted files: SKILL.md; references/schemas.md; agents/{grader,comparator,analyzer}.md
moved to references/; scripts/quick_validate.py and package_skill.py;
scripts/aggregate_benchmark.py. The latter's Markdown report function is extracted
and adapted as scripts/generate_report.py (not the unrelated upstream HTML trigger
report script of the same name). New skill_io.py and create_skill.py provide
project-owned I/O and a stable portable CLI.

Intent capture, representative with/without evaluation, grading, blind comparison,
and iterative improvement are retained. Missing metrics remain unknown; output
characters no longer stand in for tokens. Schema/report support remains portable.

Optional upstream Claude subprocess/API optimization utilities, server/viewer, and
HTML templates are not included: the portable workflow uses the invoking harness
and Markdown reports without a server. This adaptation neither claims to package
nor execute those optional adapters; see [their requirements](claude-adapters.md).
No proprietary source or unnecessary asset directories are included.
