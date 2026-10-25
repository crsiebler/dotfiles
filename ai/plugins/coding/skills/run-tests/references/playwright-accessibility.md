# Playwright and axe-core regression checks

Use this reference for an existing project Playwright suite. Check
[requirements](requirements.md); use the project's fixtures, pinned versions,
package manager and browser projects. Do not create a second test infrastructure
or substitute jsdom for rendered browser evidence.

## Select and execute

Inspect the selected script, Playwright config, webServer, global setup/teardown,
fixtures, project dependencies and reporters before running. These can start or
reuse services, seed databases, run other projects, write snapshots or upload
results. A selected project can still have setup dependencies. Use only effects
within the caller's authority; service operations and setup retain their approval
requirements. Identify the actual candidate served, including build revision and
source root; a reused stale server is not current-candidate evidence.

Select the affected test files and actual configured project name. Use the local
installed runner or verified project script, never a downloading `npx` fallback.
For example, adapt this command only after inspecting the project:

```sh
./node_modules/.bin/playwright test <existing-accessibility-spec> --project=<observed-project-name> --output=<authorized-project-output-directory>
```

`--output` does not redirect every reporter, trace or custom fixture output.
Inspect their destinations and cleanup behavior separately; avoid output paths
containing source or evidence that must be preserved. Run bounded tests rather
than watch/UI mode. Do not update snapshots or retry indefinitely to obtain green.

The generic `reviewer` may run prepared checks under its supplied contract.
Honor inspection-only mode, candidate identity, pass/session and verification
budgets. Verify candidate and tracked state before and after execution; unexpected
writes invalidate attribution until reconciled by the caller. The reviewer never
edits source, tests, snapshots, expectations, exclusions or baselines and never
installs tooling. Test authoring/fixes belong to an authorized implementation worker.

## Authoring pattern for the implementation owner

Adapt the example below to an existing safe fixture and its real accessibility
contract. It assumes baseURL is configured and the fixture has a Preferences
button that opens a dialog, supports Escape, and restores focus on close.
The focused activation assertion is not a test of the full Tab order.

```ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('preferences dialog accessibility', async ({ page }, testInfo) => {
  await page.goto('/accessibility-fixture');
  const trigger = page.getByRole('button', { name: 'Preferences', exact: true });
  await expect(trigger).toBeVisible();
  await trigger.focus();
  await page.keyboard.press('Enter');
  const dialog = page.getByRole('dialog', { name: 'Preferences', exact: true });
  await expect(dialog).toBeVisible();

  const result = await new AxeBuilder({ page }).analyze();
  // Persist rule IDs only here; detailed DOM evidence needs separate sanitization.
  await testInfo.attach('axe-rule-summary', {
    body: JSON.stringify({
      engine: result.testEngine,
      violations: result.violations.map(item => item.id),
      incomplete: result.incomplete.map(item => item.id),
    }),
    contentType: 'application/json',
  });
  expect.soft(result.violations, 'axe violations with dialog open').toEqual([]);
  await page.keyboard.press('Escape');
  await expect(dialog).toBeHidden();
  await expect(trigger).toBeFocused();
});
```

Add cases for the relevant initial, expanded and error states; wait for meaningful
readiness before each scan. Keep whole-page scanning unless the acceptance scope
is explicitly narrower. If using `withTags`, select tags supported by the pinned
engine for the agreed WCAG target and record them; tags filter rules, not prove
coverage of every criterion. Record `include`, `exclude`, disabled rules and
baseline fingerprints. Never add suppressions solely to make a test pass.
Any accepted baseline needs an explicit rationale, owner and follow-up; reviewer
cannot change it. Avoid snapshots of full axe JSON containing volatile DOM data.

## Interpret and report

Record command, exit status, selected projects/tests, actual browser/channel,
Playwright/adapter/engine versions, candidate, scanned states and rule configuration.
Distinguish setup failure, new violation, known issue and inconclusive result.
The example fails on violations; `incomplete` still needs manual disposition and
is not a passing accessibility judgment even when the test process exits zero.
Retain actionable rule IDs, targets, impact, failure summaries and help URLs in
sanitized evidence where permitted. Raw axe JSON, assertion output, traces and
screenshots may contain private DOM or URL data; prefer safe fixtures and inspect
reporter retention. Never upload evidence implicitly.

Keyboard order/traps, focus visibility, screen-reader announcements and other
manual criteria need separate observations. Use the advertised `verify-interface`
skill when available. Report missing required checks as blocked and optional
coverage as unverified; neither a zero-violation result nor a DOM/ARIA snapshot
certifies WCAG compliance. No mock result or static skill test is a live axe run.

Sources: [Playwright accessibility testing](https://playwright.dev/docs/accessibility-testing),
[test configuration](https://playwright.dev/docs/test-configuration),
[axe-core results API](https://github.com/dequelabs/axe-core/blob/develop/doc/API.md).
