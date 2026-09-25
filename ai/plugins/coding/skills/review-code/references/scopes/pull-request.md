# Pull request, branch and release comparisons

Resolve the exact repository/PR or base/head pair from explicit input and verified
read-only metadata. Do not infer a PR from an unrelated branch name. Record actual
base/head revisions, comparison semantics (merge-base PR changes versus endpoint
release comparison), included commits, changed files and intended behavior.
Missing local refs or remote evidence must be disclosed; do not silently compare
the worktree, last commit or a stale tracking branch instead.

Inspect all included changes, handling renames/deletions, relevant consumers and
contracts, and supplied CI evidence. A CI success applies only to its actual
revision and job scope. Read in bounded groups and retrieve missing sections
through allowed inspection; do not checkout, fetch into the repository, execute
tests or post. Respect tighter native role tool limits, including network limits.
If the head changes, identify which snapshot was reviewed and remaining gaps.

Attribute introduced and exposed defects against the verified baseline. Distinguish
pre-existing defects and optional maintenance recommendations; do not fill a review
with unrelated legacy issues. Cross-component changes require the corresponding
producer/consumer contracts, including mixed-version behavior where relevant.

For a release comparison, name both releases/revisions and relevant migration,
packaging, rollout and rollback evidence. For cross-repository work, name each
repository/component/version and inspect only authorized supplied or available
counterparts. Missing counterparts block claims about whole-system compatibility;
report exact missing evidence instead of inventing behavior or expanding access.

Use the caller's findings schema. OpenCode `/review-pr` owns its detailed PR
orchestration and GitHub inline schema; generic review does not duplicate them.
Feedback disposition and thread resolution belong to the separately advertised
feedback workflow. This assessment does not submit a review or authorize merge.
