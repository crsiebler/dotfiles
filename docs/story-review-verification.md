# Story review and runner retirement verification

Historical phase record: the current role catalog and activation contract are
in [AI configuration](ai-configuration.md#custom-roles-and-native-execution). Recorded results below
belong to that earlier source revision.

Date: 2026-10-24. Source-only change in the dotfiles checkout.

## Delivered source

- Removed the external runner, its two OpenCode agents, recovery command/skill,
  JSON planning reference, runner tests/fixtures and active runner documentation.
  The Makefile no longer installs the executable and the AI installer no longer
  requires its reviewer file.
- Removed the dedicated story-reviewer role. The coding plugin now provides
  review-story, which owns the full staged-review contract and JSON schema.
  run-agent-team discovers that skill and supplies its contract and concrete
  packet to generic code-reviewer. Ordinary sessions need no goal API.
- code-reviewer and review-code allow authorized focused verification and honor
  explicit inspection-only scope. The role inherits runtime permissions;
  candidate-preservation instructions are behavioral, not immutable enforcement.
  Six other inspection roles retain native read-only settings.
- Review packets identify the staged candidate, execution root, required checks,
  verification mode/commands, resources, private outputs and bounded time/count
  limits. Results distinguish supplied from executed evidence. Mixed worktree
  inputs, candidate drift and unavailable required checks cannot establish a pass.
- Both harnesses default to Markdown PLAN.md. New archival enrollment uses
  MarkdownPlan; legacy CodexGoalMarkdown records preserve original provenance and
  may continue with code-reviewer. The retired JSON adapter is rejected without
  touching its artifacts. Existing archive locks, hash/commit checks, failure
  preservation and copy-only fallback remain.
- Source inventory: 127 canonical roles, one native OpenCode-only sprite-artist,
  128 total OpenCode roles, 31 skills across the existing five Craft plugins.

## Observed checks

Used Python 3.11.16 from /opt/anaconda3/envs/dotfiles/bin/python, with PyYAML
6.0.3. Git fixtures used /Library/Developer/CommandLineTools/usr/bin/git.
Temporary test files stayed under the project tests directory.

| Check | Observed result |
| --- | --- |
| Pre-change story suites | 23 tests passed |
| make validate-ai with the Conda interpreter | Passed after removal of the stale installer prerequisite |
| Focused regression suite | 138 tests passed |
| create-skill dependency check | Python 3.11.16 / PyYAML 6.0.3 available |
| create-skill validate review-story | Passed frontmatter and bounded file-tree validation |
| Git diff whitespace check | Passed |

The focused suite comprises agent_contract_test, agent_team_contract_test,
story_execution_test, story_blocker_test, archive_run_test, ai_install_test,
coding_workflow_contract_test and create_skill_test. It exercises native rendering
and exact copies, generic role discovery/duplicate rejection, isolated installer
fixtures, dependency/worktree rules, review contracts, and real temporary Git
archival behavior. It does not establish model compliance with prose instructions.

Broader discovery was also attempted during the change. With only the Conda
runtime, 248 tests reported 43 failures, six errors and one skip: document/media
packages were unavailable, and one stale installer prerequisite was subsequently
fixed. With the existing bundled Python 3.12.14 selected through SKILL_TEST_PYTHON,
255 tests reported seven failures and one skip. Those seven failures were
create-skill checks (including document-bundle subtests) reporting unavailable
PyYAML in that bundled runtime. Conda has PyYAML but lacks the document/media
packages. No packages were installed, tests weakened or unrelated helpers changed.
The broader suite is not reported as passing.

## Limits and activation

Ten representative review-story evaluation scenarios were added, covering scoped
execution, inspection-only review, mixed candidate inputs, missing tools/contracts,
targeted continuation, persistent blockers, tracked writes, ordinary PR routing
and stale check evidence. They are unrun model evaluation specifications, not
behavioral benchmark results.

No real agent was dispatched, no goal/runner launched, no user configuration
installed or removed, and no commit, push or external post performed. Existing
untracked PLAN.md, docs/claude-code-support-assessment.md and
tasks/prd-claude-code-support.md were preserved. Historical archives and prior
verification records remain; old records are marked superseded where applicable.

A coordinated coding-plugin and native-role/policy refresh is required for active
use. Plugin refresh alone cannot remove the installed generic reviewer's old
no-test contract. Restart and verify unique skill/role discovery and both review
modes in a fresh authorized disposable session. Inventory and separately authorize
exact retired installed paths under
[retirement cleanup](remove-old-ai-files.md#retired-runner-and-story-role).
Never delete plugin caches or historical project state as a shortcut.
