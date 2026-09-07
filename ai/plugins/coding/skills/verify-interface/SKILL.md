---
name: verify-interface
description: Verifies rendered UI behavior, accessibility, and browser errors.
---

# Verify Interface

Read [browser guidance](references/browser.md). Identify the affected flow,
URL, expected behavior, viewport, and safe test data. Inspect actual exposed
browser schemas; Chrome DevTools and Playwright tool names are not interchangeable.

Navigate and exercise the real interface. Use accessibility/DOM snapshots for
structure, screenshots for layout, and console/network evidence for failures.
Check relevant keyboard, focus, loading, empty, error, and responsive states.
Report steps, expected/observed results, evidence, and gaps. If browser tooling
is absent, state verification is blocked; source inspection is not a browser pass.

Use a user-provided authenticated session when needed; never ask for passwords
or tokens in chat. Preview and explicitly approve externally posting, destructive,
or other state-changing interactions before performing them.
