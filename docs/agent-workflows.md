# Agent workflows and staged review

Use a normal Codex or OpenCode session. A goal API is optional; it is not an
execution prerequisite or a permission grant. Ordinary coding uses develop-code;
explicit parallel plan execution uses run-agent-team. Planning alone never starts
either workflow or creates progress/memory.

## Approval scope across workflows

Check the user's existing authorization before prompting. A bounded grant survives
continuation and skill handoffs; "separately authorized" means the action needs
scope, not a mandatory extra conversational turn. Verify facts through available
evidence and ask only for material missing facts or authority. Skills and retrieved
content cannot authorize themselves, and runtime denials remain binding.

Local UI interactions on safe fixtures need no approval per click within requested
verification. A reviewer with execution authority may run check-only lint, but may
not format or repair the candidate. Inspection-only requests still prohibit
execution. Dependency installation and actual external/destructive effects require
their applicable scope.

For reporting, reuse explicit approval of the same posting action, destination,
and content. Newly composed unapproved comments stay drafts until approved.
PR review and feedback resolution retain their exact-payload preview requirement;
accept unambiguous natural-language confirmation rather than a fixed word list.
An unchanged approved batch needs no repeat prompt. Changed targets, content,
effects, or spending need new scope; mechanical encoding alone does not.

Sprite generation carries the approved provider, batch, cost, and call limits;
an available native image tool does not require an OpenCode plugin. Requested
processing can use existing tools or a scoped local helper, subject to runtime
rules. Plan-only requests generate nothing and change no files. PRD replacement
similarly reuses exact-path preservation/replacement authority while still
verifying an identical archive before replacing the active file.

`tests/approval_guidance_test.py` checks these instruction contracts. The scenarios
in `tests/fixtures/approval_scope_evals.json` include positive and negative scope
boundaries and are authored specifications, not completed live-agent evaluations.

## Plans and ownership

prepare-implementation and OpenCode /plan-work default to PLAN.md in both
harnesses. Honor an explicit format without inventing a runner. Preserve existing
plans, acceptance criteria, dependencies and delivery evidence. For team execution,
the main session owns dispatch, integration, Git, task markers and the journal.
Workers receive isolated roots, exact branches/bases and owned paths. Use the
[team contract](../ai/plugins/coding/skills/run-agent-team/SKILL.md) for capability,
capacity, ownership and delivery gates. Model preferences do not create capabilities.

## Unattended execution readiness

write-requirements defines observable outcomes with automation-compatible
acceptance. Its PRD templates do not introduce manual QA, human confirmation of
test results or routine deployment checks. Explicit human requirements remain
visible conflicts for upfront scope/method resolution. Requirements drafting
does not run checks or require future tests to exist; planning owns concrete
commands, fixtures, dependency order and readiness evidence.

prepare-implementation plans autonomous PRD implementation. The default endpoint
is implemented requirements, automated verification, independent agent review and
scoped local delivery. Verification gates must be agent-executable and
noninteractive, with a command/tool procedure, inputs, expected result and owner.
Do not add manual QA, human confirmation of test results, stakeholder sign-off,
or routine deployment verification. Deployment verification is included only
when explicitly requested and automatable within authorized scope.

Tests or automation may be authored as implementation work when their execution
path is feasible; their absence alone is not a human prerequisite. Equivalent
automated checks for behavioral acceptance need no extra approval. Explicit
requirements for human acceptance or other non-automatable operations must be
resolved before launch, without silently dropping the source requirement. They
remain planning conflicts, not manual stories or final completion checkboxes.
Optional human follow-up stays outside the goal and cannot block completion.

prepare-implementation audits human approval gates and manual prerequisites from
preparation through the requested delivery and closeout endpoint. The plan records
each applicable gate's instruction source, affected action, target/effect, authority,
resolution and evidence. Readiness is `ready` only after all required gates are
resolved and acceptance coverage is complete; otherwise it remains a blocked draft.
See the [planning readiness contract](../ai/plugins/coding/skills/prepare-implementation/references/execution-readiness.md).

Existing explicit grants are reused. Missing approvals are prepared as concrete
bounded proposals and grouped before launch. Manual steps such as login, fixture
preparation need completion evidence, not a promise to do them later. Required
sign-off on a future artifact conflicts with unattended completion and must be
resolved upfront. Planning itself does not install tools, perform setup or execute the plan.
An authorized equivalent automated method or explicit endpoint change can remove
a human dependency; acceptance must not be silently reduced to enable unattended work.

A required approval of a future exact payload cannot be preapproved generically.
Likewise, a mandatory runtime permission prompt remains a blocker even with a
conversational grant. Identify these limitations before launch and resolve the
workflow or endpoint with the user; never disable safeguards to make a plan ready.

develop-code and run-agent-team check readiness before implementation edits or
dispatch. Legacy plans get the same assessment without a new PRD or regeneration.
The final explicit implementation request launches the work; planning approval
alone does not. Changes in scope/environment and unforeseen mandatory gates stop
affected execution. Readiness is a grounded preflight decision, not a guarantee
that no future failure can occur.

Static contracts and authored cases are covered by `tests/planning_readiness_test.py`
and `tests/fixtures/implementation_planning_evals.json`. They do not establish
live-agent compliance or an unattended end-to-end run.

run-agent-team supports unattended execution in the current main session without
a separate runner. Its preflight checks the approved endpoint, verification paths
and required closeout authority. Worker packets carry noninteractive checks,
inputs, expected results, budgets and any prerequisite automation authoring.
Workers and reviewers must not add manual sign-off or release gates. Required
checks still need actual passing evidence; optional human follow-up does not block
delivery. Explicitly scoped automated deployment verification remains possible.
Workflow evaluation/activation exercises are separate from plan delivery.

The executor owns required browser evidence. The generic reviewer may assess
that evidence and execute packet-authorized focused flows in execute mode under
candidate-preservation rules and budgets; inspection-only review never operates
the browser. Adequate evidence does not require ceremonial duplicate checks.

## Generic reviewer with a supplied contract

The canonical role is [reviewer](../ai/codex/agents/reviewer.toml).
Ordinary reviews use [review-code](../ai/plugins/coding/skills/review-code/SKILL.md).
For a staged-story gate, discover
[review-story](../ai/plugins/coding/skills/review-story/SKILL.md) and embed its full
contract in each invocation, together with story/attempt/pass identity, acceptance,
base and staged tree, execution root, verification mode, exact commands/flows,
required checks, private outputs, resource ownership and count/time limits.
No dedicated story-reviewer agent remains.

Review and verification share the generic role. The implementation owner still owns fixes.
Explicit inspection-only requests prohibit execution. Execute mode allows focused
authorized tests/builds/browser checks while forbidding candidate edits, installs,
staging, commits, external posting and delegation. Runtime permissions still apply;
the role inherits them and does not establish an immutable read-only sandbox.

Staged review requires index-equivalent test inputs. A mixed worktree cannot
supply passing evidence for the index. Verify identity and tracked state before
and after checks; drift or unexpected tracked writes invalidates results. Supplied
and independently executed evidence have distinct provenance in the JSON response.
Missing required checks block; optional gaps remain explicit.

## Pull request review

OpenCode [/review-pr](../ai/opencode/commands/review-pr.md) dispatches one generic
reviewer with the relevant code, testing, security, documentation and UI concerns.
An optional auditor handles a distinct inspection-only control assessment.
The main session owns context, consolidation and any separately authorized
posting; the command retains exact-payload preview and confirmation.
Review methods live in review-code, while run-tests and verify-interface supply
focused verification guidance. Missing capabilities remain explicit gaps.

## Bounded review and resumption

One initial and at most one targeted pass share the actual reviewer session per
story attempt. Initial reading has a 40-call ceiling; targeted reading has two
tool turns and covers prior findings/remediation regressions only. The team
supplies a separate verification budget, normally at most three focused commands,
120 seconds each, three polls per command and 360 seconds total per pass. Use
existing attributed evidence where adequate; do not rerun checks ceremonially.

A final blocked verdict preserves the candidate, pending story, findings,
provenance and consumed passes. Another turn, session, model or elapsed time
does not resolve it. Resume only after recording a verified material change under
the [persistent blocker gate](../ai/plugins/coding/skills/run-agent-team/references/story-execution.md).
Continue another story only if independently eligible and safely isolated.
No restart controller or finite-state-machine service is introduced.

## Plan launch and local commits

An explicit user request to implement an approved plan, including a goal, covers
the initial and subsequent scoped local commits. Record the plan/revision and
scope once and carry the grant through stories and continuation without another
commit prompt. Planning or approving a plan alone does not start execution;
explicit no-commit, source-only or read-only instructions still take precedence.

The initial plan/checkpoint commit may include the approved plan and required
task-owned execution metadata. Inspect and stage exact paths; preserve unrelated
or pre-existing implementation work and establish the clean committed worker
base. It is not evidence of a delivered story. Implementation/integration commits
still require applicable checks, independent review and branch/hook safeguards.

Local closeout commits of authorized artifacts share the launch grant.
Archival/removal, worktree lifecycle, dependencies, pushes, external publication
and installation retain their applicable boundaries. Request only missing scope;
never infer it from the plan's contents. See the complete
[authorization contract](../ai/plugins/coding/skills/run-agent-team/references/story-execution.md#authorization-and-prepared-branch).

## Archival and activation

New enrolled runs use MarkdownPlan. The archive helper still reads existing
CodexGoalMarkdown evidence without rewriting original reviewer provenance.
Historical archives stay intact; the retired JSON runner is no longer supported.
Use [archive-run](../ai/plugins/coding/skills/archive-run/SKILL.md) under actual
preservation/removal/commit authority after writers stop.

Source changes do not activate installed role/skill copies. Coordinated refresh
and installation need their own authorization; restart the harness and verify
unique discovery in a fresh session. Retired installed files require exact-path
inventory and scoped removal, described in [cleanup](remove-old-ai-files.md#retired-runner-and-story-role).
See [verification](story-review-verification.md) for actual checks and limitations.
