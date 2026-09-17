# Authoring and execution contract

Capture purpose, trigger examples and non-triggers, expected artifacts, relevant
inputs, and success criteria from the request first. Resolve material gaps before
choosing tests; a skill request does not authorize external effects or installs.
Use a project workspace, never a sibling of an installed skill. Author SKILL.md
with a matching action-oriented directory/name and a concise capability description.
Put substantial conditional guidance in linked references and deterministic reusable
operations in scripts. Follow the target repository's packaging conventions.

The portable CLI is `python /loaded/create-skill/scripts/create_skill.py`:

- `check`: report Python and PyYAML availability, no writes.
- `--project ROOT validate SOURCE`: validate a project-local skill directory.
- `--project ROOT package SOURCE OUTPUT.skill`: validate and package a skill as ZIP.
- `--project ROOT benchmark INPUT OUTPUT.json`: aggregate recorded run evidence.
- `--project ROOT report INPUT.json OUTPUT.md`: render an inspected benchmark.

ROOT must be an existing, nonsymlink project directory. Relative paths are relative
to ROOT; absolute paths must remain inside ROOT. Input trees must have no symlinks.
Installed resources are read-only even if ROOT contains the installation. Outputs
must be fresh paths outside the input skill, with existing nonsymlink parents;
no overwrite flag. Files are bounded at 2 MiB each, trees at 1,000 entries and
16 MiB total; final artifacts at 16 MiB. No servers, CLI agents, or network calls.
Exit codes: 0 success, 2 input, 3 missing dependency, 4 generation/I/O, 5 validation.
Errors identify a category without printing input contents. CLI summaries are bounded.

Benchmark layout: INPUT/eval-N/{with_skill,without_skill}/run-N/grading.json
(or INPUT/runs/eval-N/...). Record an expectations array containing nonempty `text`,
boolean `passed`, and nonempty `evidence`. Summary counts are derived from those
expectations; if supplied, summary counts/rate must agree. A sibling timing.json
may contain total_duration_seconds and total_tokens; absent values stay null.
Character counts never stand in for tokens. Every run retains its source-relative
location and evidence. Invalid or absent runs fail rather than silently disappear.

Run representative requests with and without the skill using available, authorized
capabilities; sequential execution is valid. Delegation is optional and requires
permission and a bounded budget. Save actual artifacts/transcripts, then grade
against testable expectations and inspect subjective quality separately. Use the
schema reference and grader/comparator/analyzer guidance as prompts, not assumed
native roles. Record model/runtime if known and missing telemetry as unknown.

Review reports with the user, identify concrete failures, revise a project copy,
and rerun affected cases plus untouched held-out cases. Avoid optimizing wording
only for examples already seen. Keep version history, input hashes, and evaluation
conditions so comparisons remain interpretable. Stop when agreed outcomes are met
or a missing capability requires user action; never loop or spend automatically.
