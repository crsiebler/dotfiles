# Planning the dependency DAG

Build one graph from the plan's stable story IDs. Record explicit prerequisites
and the stories responsible for integrated acceptance; recommended agents are
per-story hints, not dependency nodes. Every edge must reflect a real required
output or integration prerequisite, not artificial ordering for convenience.

Validate IDs are unique, every reference exists, no story depends on itself, and
there is no cycle. Kahn's algorithm: compute each node's prerequisite count, emit
zero-count nodes by priority then document order, remove their outgoing edges and
repeat. If un-emitted nodes remain, report the exact cycle/unresolved prerequisites
and keep the plan a draft. Use the same validated edges in Markdown Depends on or
Ralph's existing notes/priorities; add no JSON keys or second tracker.

This computes a valid planning order. It does not dispatch agents, declare a
prerequisite delivered, allocate worktrees or choose runtime models. Preserve
constraints and ownership notes as handoff data for whoever executes the plan.
