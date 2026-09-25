# Coding workflow verification and evaluation proposal

Status: source implementation through US-010 is committed at
`305226d` on `refactor/coding-skills-for-ponytail`. US-011 live
comparisons were waived by the user when requesting completion of US-011 and
continuation to US-012. No live evaluations ran. US-012 removes the superseded source trees;
installed activation remains separate. Closure is a user scope decision, not
evidence that model behavior passed.

## Source evidence

Baseline: `a6c3b8f2ec7ee0b231eeeef11342f17b617a23a9`.
The [scenario fixture](../tests/fixtures/coding_workflow_evals.json) records
38 baseline artifact SHA-256 hashes, 27 unrun scenarios, and an empty results array.
The [archived execution journal](../archive/2026-09-24-coding-workflows-and-review-architecture/docs/progress.md) contains per-story checks, reviews and
limitations. The [ownership map](coding-workflow-design.md) records policy parity.

| Evidence | Observed result | Limit |
| --- | --- | --- |
| `make validate-ai` | Passed after affected stories | Source structure, not model routing |
| `coding_workflow_contract_test.py` | Four tests passed | Metadata, isolated resource closure and preserved testing reference |
| `agent_contract_test.py` | 20 tests passed | Native metadata/rendering contracts |
| Both `render-agents.py --harness ... --check` variants | 128 sources/rendered, zero writes | No installed role behavior observed |
| `story_execution_test.py`, `story_blocker_test.py` | 11 and six tests passed | Existing execution and persistent blocker contracts |
| `bash tests/ralph_review_test.sh` | Passed | Local reviewer protocol regression, not live Ralph execution |
| `ai_install_test.py` | 35 tests passed | Isolated fixture/fake CLI installation behavior |
| Baseline policy and role comparisons | Unchanged protected policy sections and non-prose TOML fields | Source equality only |
| Helper isolated-copy resource checks | Passed | References resolve without sibling bundles |
| US-010 execution-reference comparison | Removing new optional method paragraph reproduces prior bytes | Existing contract text preserved |
| `git diff --check` | Passed | Whitespace only |

The broad command was:

```sh
TMPDIR="$PWD/tests" \
SKILL_TEST_PYTHON=/Users/corysiebler/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
python3.11 -m unittest discover -s tests -p '*test*.py'
```

It ran 261 tests in 71.463 seconds and exited 1: seven failures and one skip.
Five `create_skill_test` cases and two `document_skills_contract_test` checks
failed because the selected Python lacks PyYAML and the helper exits 3. These
sources are unchanged from the prepared baseline; the prior
[MCP verification record](create-mcp-server-verification.md) documents the same
dependency gap. This is evidence of an existing environment limitation, not a
fresh baseline suite run or a passing full suite. The nonverbose run did not
capture the skip reason. No dependencies were installed.

No standalone repository typecheck or configured Markdown/JSON/TOML formatter is
available. No live model comparison, paid evaluation, global installation,
or post-install discovery verification has been performed. US-012 source
retirement is separately recorded below.

## Optional future evaluation proposal (not authorized or required for this delivery)

| Decision | Proposed scope |
| --- | --- |
| Runtime | Native Codex subagent sessions in this task; record actual tool/version and model provenance returned |
| Model | `gpt-6-sol`, reasoning `medium`, same settings for both variants; stop if unavailable rather than substitute |
| Sample | All 27 frozen scenarios, one fresh baseline and one fresh candidate session each: at most 54 sessions |
| Repetitions | One per variant/case; exploratory evidence, not a reliability estimate |
| Delegation | At most two evaluation sessions concurrently; no child delegation or independent model graders |
| Spending | Existing Codex account usage only; no separate API purchases, external paid services or dependency installation |
| Per-session boundary | One scenario, at most 20 tool calls and 4,000 final-output tokens requested; behavioral limits, not an enforced token or dollar cap |
| Grading | Parent manually scores saved outputs, tool traces and before/after fixture evidence against frozen expectations |
| Retesting | No automatic retries, tuning or additional batch; report incomplete cases and seek a revised budget if needed |

If a hard dollar or token ceiling is required, select an evaluation runner that
can enforce it before launch. The proposed native session count bounds delegation;
it does not establish a hard spending cap. Unknown telemetry stays null.

### Isolation and interpretation

Build baseline and candidate material from exact Git revisions into separate
project-local evaluation directories. Record selected paths, hashes, prompts,
capabilities and configuration before any run. Give each session only its variant
catalog and case-specific project fixture. Do not include expected answers or
prior-session outputs in the model prompt. Alternate baseline/candidate ordering
by scenario. Use fresh sessions with no inherited conversation history.

The candidate catalog represents intended post-retirement discovery: omit the
three superseded development skill entries from the evaluation copy, while
leaving repository sources intact until US-012 approval. Record this explicit
catalog transformation; also record that the interim checkout still has old
entries. Include the standalone project guidance and applicable personal/native
role guidance consistently for each variant. Use only the selected variant's
relative resources. Do not install or refresh user-level configuration.

Native subagents may still expose installed skills or ambient runtime guidance.
Inventory this at launch. Supplied-catalog selection is a controlled model
experiment, not proof of automatic installed discovery. If ambient guidance cannot
be separated from the variant under test, record contamination and do not claim
an isolated comparison; use a separately agreed isolated runner instead. Missing
model provenance, fixture capability or authoritative tool traces leaves the
case incomplete, rather than passing it from a hypothetical answer.

Create deterministic, offline project fixtures for engineering cases, with
known defects/contracts, local tests, and preserved user-edit sentinels. Evaluation
writes are limited to the session's case directory. Review, diagnosis-only and
planning-only cases retain their stated read-only or planning scope. No real PR
posts, auth changes, payments, services, production access or global changes.
Use supplied PR/CI evidence rather than live external services. Missing-tool and
reviewer-blocker cases must actually withhold those capabilities in the harness;
merely asking the model to imagine an unavailable tool is weaker evidence and
must be labelled as such.

For image/research negatives, assess coding discovery only; stop before image
service or web execution. This does not evaluate image/research quality. Creative
writing can return text. Record selected and loaded guidance, not just assertions
about which skill the model would use.

### Reserved cases and grading

Six cases are marked reserved: embedded-instructions, diagnosis-only,
fresh-specialist, release-counterpart, retry-cancellation,
and performance-accessibility. Their text is already
visible, so they are held out from tuning but are not blind. Freeze all requests
before runs; do not tune using reserved outcomes. The proposed batch uses these
visible reserved cases, with that limitation; genuinely unseen variants require
an agreed separate preparation and run budget.

Score each expectation and prohibition separately: pass, fail, or unavailable
with an evidence reference. Map baseline development routes to the appropriate
old skills rather than penalizing the baseline for lacking `develop-code`.
Compare actual contract outcomes separately from route names and amount of text.
Record no score for latency, cost or token efficiency without measured telemetry.

Proposed promotion threshold: candidate satisfies every assessable required
expectation and no prohibition; no unresolved required scenario is unavailable;
no candidate contract regression relative to baseline. Any unauthorized mutation,
fabricated evidence or required-review bypass blocks promotion immediately.
One repetition cannot establish general reliability or statistical superiority.
Report baseline and candidate outcomes even when both fail. A failure requires
remediation and a separately bounded recheck, not deletion of adverse results.

Persist each result using the fixture's `result_record_fields`, with exact source
revision, artifact hashes, full input/output, permitted capabilities, actual tool
trace, mutation evidence and grader rationale. Keep static checks, manual
walkthroughs, model behavior and post-install discovery in separate evidence
categories. Do not populate results without actual runs. US-011 closure records the user
waiver, not completion of these proposed evaluations.

## Remaining delivery boundary

The user authorized proceeding to US-012 after waiving live US-011 evaluations.
The source retirement removes exactly these repository source trees, with testing guidance already
preserved in `develop-code`:

- `ai/plugins/coding/skills/implement-feature/`
- `ai/plugins/coding/skills/develop-with-tests/`
- `ai/plugins/coding/skills/refactor-code/`

`review-code` is retained. Final source discovery, consumer reconciliation,
retirement preservation tests and activation/rollback documentation are checked
in US-012. Follow [activation and rollback](remove-old-ai-files.md#consolidated-coding-workflows).
Installation/refresh, shared-root cleanup and fresh-session verification require
separate activation authorization; never manually delete plugin caches.


## US-012 source delivery audit

- Final coding catalog: 13 current entry points. New catalog regression failed
  with precisely the three old entries, then passed after their removal. All five
  coding workflow contract tests pass, including isolated resource closure and
  the preserved anti-pattern reference hash.
- No active source consumers reference the retired identifiers. Remaining names
  identify historical baseline artifacts or explicit migration/removal guidance.
- Five plugin identities are unchanged. Marketplace/manifest, installer,
  retirement engine and renderer sources match the prepared baseline; no new
  ownership records or special-case cleanup logic were added.
- Both renderer checks report 128 sources/rendered and zero writes. Native role
  metadata remains unchanged; three native OpenCode-only roles remain intact.
- README, repository AGENTS, configuration/authoring and removal guides describe
  coordinated policy/roles/skills activation, shared-root effects, custom asset
  preservation and separately approved rollback. New links/anchors resolve.
- Live comparative outcomes remain unrun under the US-011 waiver. Installed
  activation, unique live discovery and installed behavior remain unverified.

The final regression result and staged review are recorded in the execution
journal. The prior full-suite failure above remains an environment limitation,
not evidence of a successful full run.
