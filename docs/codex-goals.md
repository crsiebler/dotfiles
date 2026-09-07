# Codex goals and implementation checklists

Use `prepare-implementation` to turn approved requirements into a Markdown story
checklist. The skill defaults to `PLAN.md` when trusted runtime context or the
invoking native entry point identifies Codex, unless you explicitly request another
format. OpenCode defaults to Ralph's `plan.json`; its native `/plan-work` wrapper supplies
the JSON default. If routing is unavailable or ambiguous, the skill asks rather
than inferring the harness from `PATH`, installed tools, folders, environment
variables, or policy headings.
Both formats preserve bounded stories, dependency ordering, and verifiable criteria.

## Prepare

Ask Codex to use the installed `prepare-implementation` skill with your requirements.
Use the skill identifier shown by the runtime rather than guessing plugin namespace
syntax. The skill reads only the selected format reference and creates the plan;
it does not implement, run project tests, create branches, or start a goal.

Each new Markdown story starts unchecked and contains:

- Stable ID, priority, dependencies, user benefit, and relevant paths.
- Observable acceptance criteria and applicable verification commands.
- Research, implementation, verification, independent review, and remediation steps.
- A checkpoint for actual results, decisions, blockers, and the next eligible story.

Review the plan before execution. Existing plans, checked statuses, and evidence
must be preserved unless their replacement/reset is explicitly approved. Missing
commands or evidence are recorded as unknown, not invented.

## Execute with native goals

Codex CLI 0.153.4 was inspected with goals enabled. Check `/goal` in your installed
client; feature availability and account permissions remain runtime concerns. No
Ralph profile or additional runner is required.

Example goal, to enter only after reviewing the plan:

```text
/goal Complete the approved work in PLAN.md. Research and implement one eligible
story at a time, run its required checks, obtain independent review, address
blocking findings, and record evidence and the next step before continuing.
Preserve unrelated work and existing authorization boundaries. Stop with a clear
blocker if required input, review, or permission is unavailable. Finish with the
verified changes and remaining limitations. Do not commit, push, deploy, or post
externally unless I explicitly authorize that action.
```

The plan is a completion contract, not permission to bypass sandbox or MCP rules.
Grant any desired dependency or delivery authorization explicitly with the goal.
Ralph's standing authorization does not automatically apply to a Codex goal.
Independent review uses an available native specialist such as `code-reviewer`,
or a human reviewer; self-review must not be labeled independent. This workflow
does not inherit the separate OpenCode `ralph-reviewer` gate.

Native controls:

| Command | Action |
| --- | --- |
| `/goal` | View the current goal |
| `/goal pause` | Pause it |
| `/goal resume` | Resume it |
| `/goal clear` | Clear it |

Codex maintains the objective in the thread and can continue at idle turn
boundaries. It is not a background daemon that keeps executing after the process
exits. Completion, interruption, blockers, and budget limits can stop progress.
Do not assume a Markdown checkbox or a model's completion claim proves the
acceptance criteria; retain the supporting verification and review evidence.

## Context and checkpoints

After each reviewed story, record current results and the next action in `PLAN.md`.
Read that state when resuming or after native compaction. Keep pending approvals,
unfinished work, and important decisions visible without copying every tool log.
This workflow does not require fresh threads, Ralph memory files, or a custom loop.

Rely on native automatic compaction, or use `/compact` manually when appropriate.
Automatic story-boundary compaction is [deferred](backlog.md#codex-checkpoint-compaction).
No global or plugin lifecycle hook is installed for it.

## Verification status

Routing scenarios are recorded in `tests/fixtures/implementation_planning_evals.json`
for manual evaluation. Static source checks do not establish model behavior. Before
relying on unattended execution, evaluate a bounded goal in an authorized disposable
project, including review invocation, interruption/resumption, and a blocked case.

Sources: [Follow a goal](https://developers.openai.com/codex/use-cases/follow-goals),
[Using Goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex),
[CLI slash commands](https://developers.openai.com/codex/cli/slash-commands).
