# Optional run ownership metadata

For a full-run archival-enrolled plan, each associated approved PRD carries the
same version-1 work-run block. Bind stable run_id/feature, exact task source,
adapter and explicit saved PRD inventory as supplied data without changing the
task schema or requirement prose. Preserve existing run IDs. Example data:

```work-run
{
  "version": 1,
  "run_id": "search-20261003",
  "feature": "search",
  "adapter": "MarkdownPlan",
  "task_source": "PLAN.md",
  "prds": ["tasks/prd-search.md"],
  "journal": "progress.md",
  "memory": "memory.json",
  "archive_on_completion": true
}
```

Paths are relative to the worktree root. Use MarkdownPlan/PLAN.md for new enrolled runs; preserve existing manifest IDs. journal and memory remain progress.md and
memory.json at the root. Declare only approved run-owned PRDs with unique flat
basenames; never use a wildcard or enroll unrelated artifacts. Metadata expresses
intended ownership/closeout, not actual approvals or successful delivery. Missing
source ownership remains a handoff gap; never fabricate review/check history.
Planning preserves supplied blocks but does not generate run IDs or enroll execution.
The authorized execution owner verifies/binds enrollment before the first checkpoint.
No journal/memory or archival operations are created during planning.
