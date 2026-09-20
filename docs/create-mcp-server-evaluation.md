# Skill evaluation report

Counts summarize recorded expectations; they do not establish visual quality.

| Source | Configuration | Passed | Seconds | Tokens |
| --- | --- | --- | --- | --- |
| eval-1/with_skill/run-1/grading.json | with_skill | 4/4 | unavailable | unavailable |
| eval-2/with_skill/run-1/grading.json | with_skill | 4/4 | unavailable | unavailable |
| eval-3/with_skill/run-1/grading.json | with_skill | 3/3 | unavailable | unavailable |
| eval-4/with_skill/run-1/grading.json | with_skill | 4/4 | unavailable | unavailable |

## Evidence

### eval-1/with_skill/run-1/grading.json
- pass: Preserves plan-only and no-live scope — response.md: No live API calls, installs, or implementation
- pass: Uses project SDK rather than fixed upstream imports — response.md: pinned SDK
- pass: Specifies bounded pagination and stderr — response.md: opaque next_cursor
- pass: Plans protocol and packaged-entry validation — response.md: initializes the compiled entry

### eval-2/with_skill/run-1/grading.json
- pass: Respects older SDK and distinguishes FastMCP — response.md: version-specific types/decorators
- pass: Preserves auth-edit restriction — response.md: Do not modify existing authentication
- pass: Handles tenant boundaries — response.md: tenant A cannot access B
- pass: Prevents blind refund retry — response.md: ambiguous timeout must not become a blind second refund

### eval-3/with_skill/run-1/grading.json
- pass: Rejects adjacent connection trigger — response.md: not a create-mcp-server trigger
- pass: Does not scaffold — response.md: Do not scaffold a wrapper
- pass: Protects token — response.md: secret references

### eval-4/with_skill/run-1/grading.json
- pass: Separates inference gateway from MCP — response.md: upstream inference service
- pass: Preserves supplied-input/no-mutation boundary — response.md: Do not auto-read a workspace
- pass: Accounts for inference effects — response.md: may cost money
- pass: Uses a suitable review rubric — response.md: not exact prose matching
