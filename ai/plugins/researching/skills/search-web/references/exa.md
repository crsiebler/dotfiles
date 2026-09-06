# Exa Research

Read this reference only when Exa MCP tools are available and selected for the
task. The generic research workflow lives in [Search Web](../SKILL.md). Inspect
the active schemas; these examples do not establish tool availability.

## Tool Selection

Apply this order:

1. Known URL or explicitly requested page content -> `web_fetch_exa`.
2. Open-ended or current lookup -> `web_search_exa`.
3. Multi-step comparison, enrichment, list building, or schema-constrained
   output -> `agent_run`.
4. Precise filtering or result controls -> `web_search_advanced_exa`, including
   domain, category, date, text, geographic, freshness, highlights, summary,
   or subpage controls.
5. Fetch search results only when snippets are insufficient or primary-source
   detail matters.

Batch related URLs with `web_fetch_exa` when useful. Use only tools exposed by
the active MCP connection; never claim to have used an unavailable tool.

Expected tool families (actual names may have harness/server prefixes; inspect
the exposed schemas before use):

```text
web_search_exa, web_fetch_exa, agent_run, web_search_advanced_exa
```

Use `web_search_exa` for simple lookups and `web_search_advanced_exa` for
targeted retrieval. Pass only filters that serve the user's objective; overly
restrictive filters can reduce recall.

## Agent Runs

For a new Agent run, provide a `query` and any needed options. To resume an
existing run, provide only its `runId`. If a run reports that it is still
running, retain its returned ID and resume it with only that ID.

Do not send both `query` and `runId`. A resumed run continues the existing
request; it does not accept a new refinement query. Start a new run if the
research objective changes.

Use `outputSchema` when the caller needs machine-readable results. Keep the
schema bounded, require a source URL or citation for each externally sourced
record where applicable, and prefer official or primary sources for technical
claims.

`agent_run` may also accept structured `dataSources` when the request calls for
Exa Connect-backed research. Use those providers only when the user requests
that type of enrichment and the active tool schema exposes them.
