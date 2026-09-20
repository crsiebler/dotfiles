# Task evaluations

Start with a few representative workflows sized to the tool surface; ten questions
and dozens of calls are not mandatory. Include a normal read, pagination or large
results, an error/recovery case, and a meaningful composed workflow. Use snapshots
or local fixtures with independently verified expected values. Keep cases
independent; write effects are tested with mocks or an explicitly approved sandbox.
Do not force string-exact answers on open-ended outputs such as code review.

For each case, record prompt, fixture/API version, expected result or rubric,
allowed effects, tool-call evidence, observed output, and disposition. Add difficult
and held-out cases plus nearby non-triggers for skill discovery (for example,
connecting an official MCP or selecting an LLM model provider).

When evaluating the skill itself, follow create-skill's available workflow and
schemas. Compare with/without the skill or actual revisions where feasible. Save
actual outputs before grading; a list of expected behavior is not a run. Same-agent
manual walkthroughs can reveal omissions but are not blinded model benchmarks or
proof of generated-server correctness. State contamination and scope limits.

Use the active authorized harness, sequentially if needed. Do not assume Claude
API credentials, subprocess agents, Exa, WebFetch, Inspector, or background services
exist. Delegation requires authorization. Do not copy the upstream evaluation
runner merely to impose a model provider. Missing tokens/timing stay unknown.
Never claim improved performance without comparable measurements.

## Provenance

Modified from Anthropic mcp-builder; see [provenance](provenance.md).
