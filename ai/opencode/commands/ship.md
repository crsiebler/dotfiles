---
name: ship
description: Prepare a scoped GitHub shipping sequence with preview and explicit approval
---

Load and follow `manage-changes`, including its GitHub reference, for the requested
commit/push/PR sequence. GitHub is the currently supported external adapter.
Treat `$1` as an optional base branch value, not shell code. If absent, discover
the repository default base for comparison and omit `--base` when creating.
Describe the final purpose and behavior across all included commits, with actual
validation/limitations and the repository PR template. Link issue/ticket context
only when verified. Inspect all included commits and the complete base diff.

Stop on `main`/`master`, no relevant changes, or unexplained uncommitted work.
An authorized archival closeout commit may be included in the prepared sequence;
preserve unrelated work. Use a unique project-local body file. Preview every
requested write, including any commit scope, exact push remote/ref and PR
head/base/title/body/command. One explicit approval may cover the whole bounded
sequence. Carry existing exact approval forward; changed targets/content need
a fresh scoped preview/approval. Do not push or merge implicitly. Return the
verified PR URL only after successful creation or verified existing PR discovery.

$ARGUMENTS
