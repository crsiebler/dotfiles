# Pre-push verification and review

Apply this gate to the actual candidate being pushed, including branches with
all changes already committed. Resolve the repository root, intended ref,
candidate tree and target base before verification. For PR creation without a
push, verify the remote PR candidate and apply the same gate before publishing.

## Repository checks

Read the repository's root `AGENTS.md` and applicable nested instructions for
the affected paths. Follow their documented pre-push procedure and exact
commands, working directories, environments, fixtures, and ordering. Run the
configured lint, typecheck, and tests. Run integration, E2E, build, or other
checks when required by the repo or when the applicable documented trigger
matches the change. If instructions are incomplete, inspect existing task
runner targets and CI check definitions for the affected packages or flows.
Use those definitions for missing details. Surface material conflicts or
ambiguity instead of guessing a command or silently omitting a required check.
Record an unsupported check category and how its absence was established.

Run checks against candidate-equivalent inputs using the existing environment.
Exclude unrelated working changes and stale outputs. Use check-only commands
where the documented procedure offers them. Inspect side effects and honor
permissions for installs, migrations, services and network access. Record the
commands, scope, candidate, actual results and any conditional skips. Reuse
verifiable passing evidence only for the same candidate, relevant inputs and
required scope. A staged candidate may carry forward its results if the commit
and check inputs match. Rerun affected checks after authorized fixes.

Block the push on failed, unavailable or unresolved required checks. Keep any
optional limitations visible. Reconfirm the exact candidate and target before
writing. If a hook, edit or ref change invalidates evidence, resolve it and
verify again before pushing.

## Independent review

After the checks pass, discover `review-code` and load its
`references/integrated-delivery.md` from the advertised bundle. Apply that
contract to the full base-to-candidate comparison before preparing the write
preview. Reuse qualifying integrated evidence from final local delivery if
available. Otherwise invoke an independent reviewer using actual runtime
capability and authorized scope. Use the native reviewer when supported.
Otherwise supply the complete discovered reviewer instructions and integrated
delivery contract to a fresh independent agent. Record the actual binding and
session. Block publication on unresolved required
findings or missing review evidence. Return findings to the authorized
implementation workflow for fixes and preserve the review session and budget
for the permitted targeted follow-up. Update the preview if the approved
target or material content changes.
