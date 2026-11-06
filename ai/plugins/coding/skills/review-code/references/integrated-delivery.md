# Integrated delivery review

The delivery owner invokes this gate once for the complete integrated candidate,
after required verification and before full delivery. Use the approved target
base or the workflow's verified local baseline. Identify the base commit and candidate tree.
Record the comparison start if using a merge base. Include the whole
comparison, acceptance criteria, and relevant passing check results with their
provenance. Treat prior story reviews as evidence and focus on interactions,
regressions, and coverage across the integrated change.

Freeze the candidate during review. Invoke an independent reviewer in a fresh
session, separate from its implementers. Supply this contract, the repository
root, exact comparison and candidate identities, criteria, check results,
inspection-only scope, and bounded reading limits sized for the comparison.
Record actual reviewer identity and session before accepting the result.
The reviewer uses
[review-code](../SKILL.md) and its
[branch comparison scope](scopes/pull-request.md). It reads the complete diff
in manageable groups and follows directly affected contracts as needed.
Verification stays with the delivery owner. Neither reviewer nor review
result grants authority to change files or publish.

Request an explicit `pass`, `changes_required`, or `blocked` result with the
reviewed identity, covered scope, evidence and limitations. Include evidenced
findings with severity and stable references. In-scope critical, high and
medium defects, and any unmet acceptance criterion, require remediation.
Missing reviewer capability, missing coverage or uncertain candidate identity
blocks delivery. An empty or incomplete response cannot establish a pass.

Allow one initial review and at most one targeted follow-up in the same session
for substantive fixes. The delivery owner routes fixes through authorized
implementation, reruns affected checks, and supplies the new identity and
remediation delta. Targeted review covers the initial findings and regressions
introduced by the fixes. A changed comparison base or unrelated edits invalidate
coverage and require a fresh full gate for the materially different candidate.
Preserve consumed passes and blocker evidence across continuations. A failed
gate cannot be retried solely by changing sessions or models.

Record the final reviewed identities, criteria and coverage, reviewer session,
finding dispositions, and verdict in the existing handoff or checkpoint.
Reuse a passing integrated review only when the base, comparison start,
candidate tree and required scope match and its provenance is verifiable.
Recheck identity before delivery. Story review alone cannot satisfy this gate.
