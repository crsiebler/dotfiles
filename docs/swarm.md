# Swarm top-level Codex launcher

From this source checkout:

```sh
./bin/swarm --project /absolute/project --plan PLAN.md --scope "<actual execution grant>"
./bin/swarm --project /absolute/project --plan PLAN.md --dry-run
```

The plan defaults to PLAN.md relative to the selected project. The project and
readable plan must already exist; its actual path must stay inside the selected
project and its file must not be a symlink. The launcher starts a fresh interactive Codex
main session using `--model gpt-6.1-sol`, `--cd` and an initial prompt composed from
[Swarm instructions](../ai/codex/swarm.md) and assignment data. It does not alter
an existing session, install files, change approval/sandbox defaults, or add a
native custom-primary-agent configuration key. Keep this script in its checkout;
copying it alone elsewhere cannot locate its instruction source.

Installed Codex CLI help was checked on Galena. It exposes model, working-root,
profile and initial-prompt options, with no named primary custom-role selector.
The [official command reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
and [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
provide the supported configuration surfaces. The launcher uses the locally
verified model/root/prompt options and needs no profile installation.

Swarm loads the installed run-agent-team skill and existing approved Codex plan.
The main thread owns dispatch, version control, merging and task state; existing
specialist workers implement isolated tasks. Missing native role/model controls,
conflicting installed pins, missing discovery or required review support remain
execution blockers. Source-checkout launch and fake-CLI tests do not prove live
model use, skill activation or unattended completion. No live run or global
installation is included. Ralph remains the separate serial OpenCode runner.
