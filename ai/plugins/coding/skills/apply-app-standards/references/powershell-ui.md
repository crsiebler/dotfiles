# PowerShell interfaces

Apply only to an actual project using this technology. Read the bundle's entry
and requirements first. Project versions, constraints and existing tools override
the topic inventory below; inherited version labels are examples, not minimum
requirements or claims of current support. Verify relevant APIs against official
documentation for the installed version before relying on them.

## Standards

A Windows GUI does not imply PowerShell 5.1. Keep UI thin over module APIs; own event lifetime, thread affinity, runspaces and cancellation. Cancellation is not rollback.

## Interface responsibilities

- Keep layout and presentation separate from module APIs. Bind structured results
  to controls with intentional update notifications and validation feedback.
- Manage event subscription lifetimes and handler state; prevent duplicate actions
  and stale callbacks after a view closes.
- Keep slow work off the UI thread using target-supported runspace/background
  patterns. Respect apartment requirements and thread affinity; marshal updates
  to the UI thread rather than touching controls from workers.
- Design responsive progress, error, empty, and completion states. Propagate
  cancellation, dispose workers/resources, and unsubscribe events on shutdown.
  Explain partial completion; cancellation is not automatic rollback.
- Preserve accessible labels, keyboard navigation, focus order, readable contrast,
  and feedback that does not depend only on color. For TUIs, handle terminal size,
  input errors, and terminal-state restoration without requiring a graphical host.
- Keep secrets out of displays and logs. UI confirmation must not bypass module
  validation, ShouldProcess semantics, or required authorization.

Validate relevant event, binding, error, cancellation, and lifecycle paths using
project tests and authorized interactive checks on the target host. Report actual
checks and unavailable GUI/TUI verification separately. Return changed interface
behavior, module-boundary implications, and remaining risks; do not invent visual
validation, accessibility compliance, or performance measurements.
