# Codex CLI entry (conditional)

Read this reference only when trusted runtime context identifies Codex CLI and
the user wants its goal/skill entry commands. Other harnesses use their actual
skill-discovery and task-entry mechanisms; these commands are not portable.
The workflow and capability checks belong to team-execution.md, not this adapter.


Select run-agent-team using the client's skill picker (`/skills` in Codex CLI),
or explicitly name `$run-agent-team` in a normal request when discovered under
that name. Use the picker if plugin qualification or duplicate names are unclear.
`/goal <objective>` attaches an objective to the active chat; it does not by itself
select this skill, create an approved plan, allocate worktrees or authorize writes.
Select the skill, then set a goal naming the exact approved plan and existing
execution scope. Do not assume combined slash-command/skill parsing.

For example, after selecting run-agent-team and the Sol main model:

```text
/goal Execute the approved PLAN.md using run-agent-team. This main session owns orchestration. Use up to two concurrent Luna implementation workers and the required Astra story-reviewer within the skill's budgets. Follow the already-approved execution, worktree and local-commit scope. Preserve pending work and report any missing authority or native capability.
```

This example is not an execution grant. Actual authorization must identify the
integration branch/root, allowed task-worktree lifecycle, local story commits and
closeout scope. No push, post, install or deployment follows implicitly.
Official syntax: [developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
and [explicit skill invocation](https://learn.chatgpt.com/docs/build-skills).
