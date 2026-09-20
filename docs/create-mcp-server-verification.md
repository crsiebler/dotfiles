# create-mcp-server verification

The coding plugin owns
[create-mcp-server](../ai/plugins/coding/skills/create-mcp-server/SKILL.md).
It adapts Anthropic mcp-builder under Apache-2.0; provenance and an unchanged
upstream license are bundled. The skills repository was only read. No global
configuration, installed skill, or mcp-suite implementation was changed.

## Scope and evaluation evidence

The bundle is instruction-only: SKILL.md and conditional design, TypeScript,
Python, verification, evaluation, and provenance references. It has no helper
runtime requirements, generated server template, or bundled model client.
Existing coding plugin skill-directory discovery includes it automatically.

[Evaluation inputs and conditions](../tests/fixtures/create_mcp_server_evaluation/evals.json)
and four recorded response artifacts cover local TypeScript planning, remote
Python tenant/refund planning, an existing-server non-trigger, and a held-out
model-backed review planning case. The responses were generated sequentially by
the authoring assistant in the same Codex session and self-reviewed. The fourth
case was reserved until after drafting, but this was not a blind evaluation.

The create-skill benchmark/report helpers produced
[the report](create-mcp-server-evaluation.md) from
[recorded evidence](../tests/fixtures/create_mcp_server_benchmark.json).
All 15 listed expectations were met by these planning responses. This small,
non-blind sample does not measure autonomous implementation success, trigger
precision, or improvement over a baseline. No without-skill comparison was run;
timing and token telemetry are unavailable. No live MCP server or provider was
started and no SDK server implementation was compiled by these cases.

## Validation and limitations

- `make validate-ai` passed: local plugin/skill structure and JSON/TOML validation.
- `python3.11 -m unittest discover -s tests -p ai_install_test.py` passed all
  34 installer regression tests using their isolated fixtures/fake commands.
- `git diff --check` passed.
- Relative bundle references and frontmatter name/description were checked from
  an unrelated project working directory; license bytes match upstream.
- Python 3.11 create-skill `benchmark` and `report` ran successfully.
- create-skill `check` and `validate` could not complete: PyYAML is absent in the
  checked local and bundled Python environments. No dependency was installed.
  No `.skill` archive was produced; this delivery is a project source bundle.
- No standalone repository typecheck or Markdown formatter is configured.
- Installation/refresh and verification in fresh Codex/OpenCode sessions remain
  separate authorized steps. Existing installed copies were not overwritten.

For stronger evidence, run independent with/without or revision comparisons in
fresh authorized sessions, implementing small fixture-backed TypeScript/Python
servers and testing their actual MCP transports and package entry points. Do not
interpret the current planning report as having performed those checks.
