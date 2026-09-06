# Markdown implementation checklist

Write project-local `PLAN.md` unless the user specifies another path. Produce a
self-contained user-story checklist, not JSON. Inspect the project for real paths,
instructions, test tools and commands; record missing checks as unavailable or
unresolved, never invent scripts or documentation. Planning does not execute tests.

## Plan contract

- Record objective, requirement sources, scope/non-goals, existing working branch
  if known (otherwise unknown), and current authorization/delivery expectations.
  Do not create/switch branches. No commits unless explicitly requested; sensitive
  actions still require approval. Plan approval is not blanket execution authority.
- Use unique stable IDs (`US-001`), numeric priorities in execution order, and
  explicit dependencies (`none` or earlier story IDs). Validate every dependency
  exists, is earlier, and the graph has no cycles; order by dependencies first.
- Bound each story to one focused task including verification and review. Do not
  require a fresh session per story. Include concrete user benefit, relevant paths,
  measurable acceptance criteria, tests and typecheck as applicable, and browser
  verification for UI changes using the project's available workflow.
- Start every generated story and acceptance/workflow checkbox unchecked. Evidence
  slots say pending/not run, never fabricated completion. Approved continuation
  preserves existing checked statuses and their evidence; edit only scoped sections.
- Each story schedules research, implementation, verification, independent review,
  remediation/reverification, then a checkpoint after review. Independent review
  may use `@code-reviewer` through available native delegation, or a human reviewer.
  If unavailable, record review pending; do not label self-review independent.
  Reviewers inspect; implementers run tests and fix findings. No simulated delegation.
- Keep sufficient resumption state in this same plan: decisions, changed paths,
  actual command/result evidence, review findings and disposition, blockers,
  authorization limits, and next eligible story. No required Ralph progress/memory
  files, staged-only reviewer, or imported Ralph execution hard gate.

## Recommended agents

Preserve supplied specialist recommendations in each story. When none are supplied,
suggest agents only where their expertise would help; use exact known role names,
not invented specialists or a mandatory agent quota. Trivial implementation work
can stay with the primary agent. Recommendations are optional unless the user
explicitly requires a particular agent.

Separate implementation and review assignments. An implementation specialist may
research, edit, and test within the authorized scope. An independent reviewer
inspects the changes and reports findings; the implementer handles remediation.
Include delegation notes defining responsibilities and file ownership so the
primary agent and specialists do not edit the same files concurrently.

At execution time, confirm the role is available through native delegation before
invoking it. A name in the plan or a definition on disk is not proof of availability.
If a recommendation is unavailable or unnecessary, record the reason and select
an appropriate alternative; do not silently substitute for an explicitly required
agent. Preserve the independent-review requirement even if the suggested reviewer
is unavailable. Planning records recommendations only and does not spawn agents
to execute the stories.

## Template

Replace placeholders using project evidence; repeat the story section as needed.

```markdown
# Implementation plan: <feature>

## Objective and context
- Objective: <observable outcome>
- Sources: <supplied requirements and inspected project paths>
- Scope: <included work>
- Non-goals: <excluded work>
- Working branch: <existing branch or unknown; no creation/switching>
- Authorization: <current grant and actions still needing approval>
- Delivery: <requested deliverable; no commits unless explicitly requested>
- Verification commands: <existing commands and purposes; unavailable checks>
- Assumptions / open questions: <material gaps or none>

## Ordered stories

### US-001 — <bounded story title>
- [ ] Story complete
- Priority: 1
- Depends on: none
- User story: As a <user>, I want <capability> so that <benefit>.
- Relevant paths: <source/test paths identified during inspection>
- Recommended implementation agents: <known role names, or primary agent>
- Recommended review agent: <known independent role, human reviewer, or not selected>
- Delegation notes: <bounded assignments and file ownership, or not needed>

#### Acceptance criteria
- [ ] <specific observable behavior>
- [ ] <regression/edge case verified with relevant existing tests>
- [ ] <applicable typecheck command succeeds, or documented unavailability>

#### Execution checklist
- [ ] Research relevant code, instructions, dependencies and test coverage.
- [ ] Implement scoped changes and appropriate tests.
- [ ] Verify acceptance criteria with identified commands/tools.
- [ ] Obtain independent review; record reviewer, scope and findings.
- [ ] Remediate findings and rerun affected checks (or record no fixes needed).
- [ ] Checkpoint after review: update evidence, decisions and next story.

#### Evidence and checkpoint
- Changed paths: pending
- Verification: not run; record command, result and relevant evidence paths
- Review / remediation: pending
- Agents used / recommendations skipped: pending; record actual delegation and reasons
- Decisions / blockers / approval needed: pending
- Next eligible story: <ID or final delivery; confirm after checkpoint>

## Resume and delivery
- Current state: planned; implementation and checks not run
- Next action: review plan and resolve material questions
- Resumption notes: <constraints and knowledge needed to continue>
- [ ] Final report: delivered scope, evidence, review outcomes, gaps and remaining work
```

For example, a search change might first add query normalization with unit tests,
then add a results filter depending on that story. Use actual project commands;
a documentation-only story may record typecheck as not applicable with a reason.
These are examples, not a mandatory architecture or fixed number of stories.

For a Python API-client story, recommendations could be:

```markdown
- Recommended implementation agents: `python-pro`
- Recommended review agent: `code-reviewer`
- Delegation notes: Let python-pro own the client module and its tests. Review the
  resulting diff independently; the primary agent coordinates and verifies the handoff.
```

## Handoff

Report the saved path, ordering/dependency checks, assumptions and unresolved
verification tools. Offer optional launch text only for use after plan review:
“Read PLAN.md and project instructions. Continue the next eligible story within
current authorization, maintain evidence/checkpoints in PLAN.md, and report gaps.”

The user may enter that text through native `/goal`; do not create the goal or
execute CLI commands during generation. The native thread continues with its
knowledge and rereads PLAN.md as needed. Rely on native automatic compaction;
do not force compaction, add hooks, run a fake `/compact` shell command, or impose
Ralph-style fresh contexts. Record durable resumption state rather than resetting
the plan. Finish execution with an evidence-backed delivery report.
