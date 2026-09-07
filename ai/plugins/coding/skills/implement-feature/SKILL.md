---
name: implement-feature
description: Implements scoped features with testable boundaries and verified behavior.
---

# Implement Feature

1. Read repository instructions, affected code, existing tests, and acceptance
   criteria. State the smallest implementation scope and material unknowns.
2. Use `develop-with-tests` for behavior changes: reproduce the missing behavior
   before implementation. Reuse existing architecture; introduce injection or an
   adapter where it makes an external dependency testable, not as ceremony.
3. Implement the focused change. Preserve compatibility, error handling, and
   project boundaries; avoid unrelated redesign or speculative features.
4. Use `run-tests` and `format-code` as appropriate. Run the project's typecheck.
   For rendered UI changes, use `verify-interface` or disclose why blocked.
5. Review the diff and report changes, executed checks, and remaining gaps.

Do not create branches, commit, push, post, install, or deploy merely because
implementation is complete. Those operations require separate authorization.
