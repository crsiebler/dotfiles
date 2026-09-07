# Bundled subagent catalog helper

The package helper is `scripts/subagents` relative to the `use-subagents`
skill directory. Resolve that location from the loaded `SKILL.md` resource path.
Do not resolve from `$PWD`, assume `$HOME/.config/opencode`, or invoke a global
`subagents` command. The package may be installed anywhere.

After obtaining and verifying the absolute skill directory, use command shapes:

```sh
sh "<absolute-skill-directory>/scripts/subagents" --harness opencode list
sh "<absolute-skill-directory>/scripts/subagents" --harness opencode search "security"
sh "<absolute-skill-directory>/scripts/subagents" --harness opencode fetch "backend-developer"
sh "<absolute-skill-directory>/scripts/subagents" --harness codex list
sh "<absolute-skill-directory>/scripts/subagents" --harness codex search "security"
sh "<absolute-skill-directory>/scripts/subagents" --harness codex fetch "backend-developer"
```

Replace the path placeholder with the verified absolute path. Validate the
harness against the two accepted values and the operation against `list`,
`search`, `fetch`; pass queries and names as individually quoted arguments,
never evaluated shell text. Check the bundled helper's help/interface if an
installed version differs; report a mismatch instead of guessing flags or
changing scripts. The launcher requires Python 3.11+ with `tomllib`; it reports
an unavailable runtime rather than installing one. Missing helper means packaging
is incomplete; an empty catalog can simply mean no native definitions exist.
Report the resolved path and result without installing or using a global CLI.

Return names/scopes/descriptions/paths as provided, search matches without invented
entries, and full fetched definitions on request. Report no matches or missing
names faithfully; offer a broader query or list operation. The helper reads
native project and global definition directories for the selected harness,
respecting `CODEX_HOME` or `XDG_CONFIG_HOME` where applicable. `--scope project`
limits reads to project definitions; `--scope global` selects global definitions.
`--project <absolute-project-root>` selects a project explicitly. Use these
options for project-only boundaries or duplicate names; do not guess which
definition to fetch. Never blend catalogs from different harnesses.

## Discovery versus execution

The bundled helper reads static native definitions, not the live runtime registry. A fetched
OpenCode Markdown definition or Codex agent configuration is reference material;
it does not register an agent, change model/tool permissions, or execute a task.

Native invocation requires an actually exposed harness delegation tool and a
registered agent supported by its schema. Use only that interface when separately
requested/appropriate. Do not assume OpenCode `@agent-name` syntax works in
Codex. Optional PRD `@agent-name` hints remain hints; preserve them without
claiming availability. If delegation cannot run, say “definition retrieved;
native invocation unavailable” rather than implying specialist verification.
