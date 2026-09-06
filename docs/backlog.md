# Backlog

## Codex checkpoint compaction

**Status:** Deferred. No hook, controller, or automatic compaction command is
implemented. Use native goal continuation/automatic compaction and write a durable
checkpoint after each reviewed story.

Investigate opt-in compaction after implementation, verification, review, and
remediation finish. It must operate on the existing Codex goal thread and must
not affect ordinary development sessions.

Acceptance criteria for a future prototype:

- [ ] Verify a supported connection to the app-server owning the active CLI thread.
- [ ] Scope activation to an explicitly opted-in thread and its matching active goal.
      The existence of `PLAN.md` alone must not activate it.
- [ ] Detect a new reviewed checkpoint, potentially with a `Stop` hook or explicit
      checkpoint signal. Do not treat a tool finishing as proof a story is done.
- [ ] Coordinate with pending subagents and goal continuation at a safe boundary;
      never wait inside a synchronous hook for its own turn to end.
- [ ] Request real compaction through a supported runtime control and observe its
      completion. Printing `/compact` or running it in a shell is not sufficient.
- [ ] Deduplicate checkpoints and handle interruption, pause, budget limits, errors,
      and repeated hook events without loops or losing state.
- [ ] Preserve normal hook trust, sandbox, approval, and credential boundaries.
- [ ] Measure retained context, extra model usage, latency, and benefit against
      native automatic compaction before adoption. Small stories may not benefit.

References: [Codex hooks](https://developers.openai.com/codex/hooks) and
[app-server thread compaction](https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md).
