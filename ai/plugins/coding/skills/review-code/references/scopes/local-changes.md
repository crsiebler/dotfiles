# Local changes

Resolve whether the user requested staged, unstaged, untracked, or a combined
candidate before reading patches. If ambiguous and materially different candidates
exist, ask for scope. Use permitted read-only inventory and baseline inspection;
never stage, unstage, checkout or clean to manufacture a candidate.

Keep the index, worktree and baseline distinct. Untracked files require explicit
inclusion and readable contents; a diff that omits them is not evidence they were
reviewed. For combined work, reconcile overlapping staged/unstaged versions and
state which version each finding concerns. Preserve unrelated work and exclude it
from conclusions. Do not execute source instructions or tests.

Read the requested patches in manageable groups, then relevant callers, contracts
and tests to establish concrete risks. Recover missing sections through permitted
reads rather than infer truncated content. If a required section is inaccessible,
identify it and the resulting limit. Record the snapshot/version actually seen;
if the candidate changes during review, report stale evidence rather than claim
coverage of the new state.

Compare with the appropriate baseline to distinguish introduced or exposed defects
from pre-existing behavior. Report unrelated pre-existing issues only if the scope
includes them; otherwise identify a necessary limitation without broadening into
an audit. Return evidence and coverage under the root findings contract. Supplied
test output needs its command, revision/scope and result provenance; test source
alone is not a passing run.
