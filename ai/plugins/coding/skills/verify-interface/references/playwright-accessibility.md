# Rendered accessibility verification

Use [browser guidance](browser.md) and [assessment](accessibility-assessment.md)
to select the affected journeys, states, viewport, browser and acceptance target.
This reference adds automated evidence; it does not replace interaction checks.

## Capability and scope

Prefer the project's existing Playwright accessibility tests using
`@axe-core/playwright`, which runs the axe-core engine. Check
[requirements](requirements.md) first. Playwright CLI/MCP availability alone does
not establish that this adapter is installed or a scan has run. DOM/ARIA snapshots
and screenshots are useful evidence but are not axe scans. Do not inject code
from a CDN, install packages, or enable servers as an incidental fallback.
When advertised, use `run-tests` for the project runner procedure.

Record the actual browser/channel, Playwright, adapter and axe-core engine
versions, app revision/build source, sanitized URL, viewport and safe fixture.
Use an agreed WCAG version/level when supplied; do not invent a conformance target.
List relevant states before checking: initial page, open menu/dialog, validation
errors and loading/empty results as applicable. Wait for observable readiness in
each state before scanning. Scanning only the landing page misses later states.
Prefer whole-page scans; component-only scans must state their reduced coverage.
Record rule tags, included/excluded selectors, disabled rules and known baselines.

## Independent review with the generic reviewer

The main session supplies `reviewer` with the acceptance criteria, candidate
identity, prepared app/fixture, exact test scope, authorized commands/output
locations and applicable review contract. For a staged story, retain the supplied
review-story packet, session and pass budgets. Do not create a specialist role,
extra review cycle, nested delegate or separate verifier requirement.

Honor inspection-only scope: assess supplied evidence without running browsers or
tests. Otherwise run authorized focused checks with existing tooling. Establish
that the running server/build actually represents the reviewed candidate;
an unrelated preview or mixed working tree cannot verify the staged candidate.
Check candidate identity and tracked state before and after execution. Report
unexpected writes without reverting them. The reviewer does not repair source,
tests, snapshots, scan exclusions or baselines, or install missing dependencies.
Return defects and setup blockers to the caller for implementation.

## Complement the scan

Exercise keyboard-only navigation with Tab/Shift+Tab and relevant activation keys.
Check visible focus, logical order, no unintended traps, dialog initial focus,
Escape/close behavior and focus restoration. Check names/roles/states, error
association, zoom/reflow, reduced motion and contrast where relevant. Distinguish
programmatic focus assertions from an actual keyboard navigation exercise.

Use a real screen reader when the acceptance criteria require one, recording its
name/version, platform and observed announcements. A browser accessibility tree
does not establish VoiceOver/NVDA behavior. Missing assistive technology leaves
that check unverified. A passing automated scan cannot establish WCAG compliance.

## Findings and evidence

Separate axe `violations` from `incomplete` results needing human assessment;
`passes` and `inapplicable` do not clear an unresolved manual check. Preserve the
configured violation gate. Do not suppress rules or exclude nodes just to pass.
For each finding, retain the rule ID, affected state/selector, impact, explanation
and help URL where available; impact is tool metadata, not the sole review severity.
Use safe fixtures and redact private DOM content, URLs and selectors before
persisting attachments. Do not publish raw authenticated scan results or traces.

Report automated results, manual observations, inconclusive items, exclusions and
unverified states separately. A missing required runner, browser, adapter or
candidate attribution blocks the required check; optional gaps remain explicit.
Follow the caller's output schema rather than replacing it with a new report.

Sources: [Playwright accessibility testing](https://playwright.dev/docs/accessibility-testing),
[axe-core results API](https://github.com/dequelabs/axe-core/blob/develop/doc/API.md),
[WAI evaluation guidance](https://www.w3.org/WAI/test-evaluate/).
