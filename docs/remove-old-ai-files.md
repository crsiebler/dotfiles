# Manually remove old AI files

The installer does not identify or remove previous installations. Use this guide
to review old AI files yourself. `make clean` removes only `$HOME/.zshrc.backup.*`;
it does not remove existing `.env` backups, AI files, or AI backups.

Run only commands for individually reviewed paths. Do not paste this document as
a script or delete an entire configuration directory. If an AI agent performs
cleanup, approve the exact paths before any move, edit, uninstall, or deletion.

## 1. Locate your configuration

Save work and quit active OpenCode, Codex, and Ralph sessions. Do not install or
update configuration while removing files.

| Configuration | Default location | Override |
| --- | --- | --- |
| OpenCode | `$HOME/.config/opencode` | `$XDG_CONFIG_HOME/opencode` |
| Codex | `$HOME/.codex` | `$CODEX_HOME` |

Use Bash for the examples. Set these variables only after checking any overrides
used by your actual launcher:

```bash
opencode_root="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"
codex_root="${CODEX_HOME:-$HOME/.codex}"
printf 'OpenCode: %s\nCodex: %s\n' "$opencode_root" "$codex_root"
ls -ld -- "$opencode_root" "$codex_root"
```

Stop if a path is empty, relative, `/`, or unexpected. Missing directories need
no cleanup. Inspect symlinks and their parents before acting; remove a reviewed
link itself without following it into its target.

## 2. Preserve customizations and credentials

Privately inspect selected files and compare them with the current repository.
Create a private archive outside all skill/agent discovery roots and outside Git:

```bash
# Choose a fresh directory name; stop if it already exists.
archive="$HOME/ai-config-backup-20260905"
(umask 077; mkdir -- "$archive")
```

Back up each selected configuration file before editing it. Use distinct names
for each origin and do not overwrite earlier backups. Configuration backups may
contain credentials; do not print them in chat or shared logs.

Preserve `$HOME/.env`, authentication stores such as Codex `auth.json`, shell
configuration, unrelated plugins, custom agents/skills, and project work including
Ralph's `plan.json`, `progress.txt`, and `memory.json`.

For user-level `AGENTS.md`, compare each installed copy with `ai/AGENTS.md` and
preserve customizations privately before an approved replacement. Earlier sources
used `ai/shared/instructions/personal.md` concatenated with `ai/codex/AGENTS.md` or
`ai/opencode/AGENTS.md`; the current installer copies the single `ai/AGENTS.md`
unchanged to both destinations. Do not delete active user instruction files or
the separate repository-root `AGENTS.md` as cleanup.

## 3. Remove selected old skills

These names were previously supplied by this repository:

```text
code-formatter-javascript-typescript  code-formatter-python
code-review-analyzer                 code-review-resolver
dev-browser                         exa
feature-implementer                  git-manager
godot-sprite-forge                   jira-daily-update
jira-task-init                       prd
ralph                               refactor-specialist
status-update                       subagents
test-driven-development             test-runner-pytest
test-runner-vitest
```

Inspect the `skills/` directory under each active configuration root. Also check
`$HOME/.agents/skills`, `$HOME/.claude/skills`, project-local skill directories,
and any additional locations configured in your harness. Same-named user skills
are not automatically obsolete.

Move one reviewed directory into your archive, including its scripts/references:

```bash
ls -ld -- "$opencode_root/skills/prd"
# Destination must not already exist.
mv -- "$opencode_root/skills/prd" "$archive/opencode-skill-prd"
```

Renaming it inside `skills/` can leave it discoverable. If you prefer permanent
removal, first back it up and inspect its contents, then delete only that path:

```bash
rm -r -- "$opencode_root/skills/prd"
```

For a symlink, use `rm --` without `-r` or a trailing slash. Do not turn the list
of names into a bulk deletion loop. Current sources live in `ai/plugins/`.
Skill cleanup is separate from command cleanup. Preserve `/review-pr` unchanged.

### Renamed web research skill

1. After a separately authorized installation or native plugin refresh, verify
   that `search-web` from `researching@craft` is available in the selected harness.
   Its source replaces `ai/plugins/researching/skills/use-exa/`; no compatibility
   alias or automatic installed-file deletion is provided.
2. Inspect `$opencode_root/skills/use-exa` and any `use-exa` copies in the other
   discovery roots listed above. OpenCode copies can remain beside `search-web`.
   Preserve customizations, including references, outside discovery roots and
   obtain exact-path approval before using the manual removal process above.
   A matching name alone is not permission to remove a user-authored skill.
3. For Codex, verify the registered `researching@craft` source checkout and use
   the installed CLI's supported native plugin refresh/replacement process with
   separate approval. Follow step 5 if an obsolete registration needs removal;
   do not delete caches manually or remove the active `craft` marketplace.
   Review separately installed standalone `use-exa` copies independently.
4. Quit and restart the selected harness and start a new Codex thread. Verify
   `search-web` discovery and absence of unwanted duplicates before discarding
   backups. Updating checkout sources alone does not clean installed copies.

### Renamed OpenCode commands and sprite agent

After preserving customizations and verifying an authorized installation of the
replacements, review these exact obsolete installed paths under the verified
`opencode_root` from step 1 (default `$HOME/.config/opencode`):

| Obsolete installed path | Replacement |
| --- | --- |
| `$opencode_root/commands/godot-sprite.md` | `$opencode_root/commands/create-sprite.md` |
| `$opencode_root/commands/prd.md` | `$opencode_root/commands/define-requirements.md` |
| `$opencode_root/commands/ralph.md` | `$opencode_root/commands/plan-work.md` |
| `$opencode_root/commands/pull-request.md` | `$opencode_root/commands/ship.md` |
| `$opencode_root/commands/subagents.md` | `$opencode_root/commands/find-agents.md` |
| `$opencode_root/agents/godot-sprite-artist.md` | `$opencode_root/agents/sprite-artist.md` |

Back up each reviewed file outside discovery roots and obtain explicit approval
before manually removing that exact path. The installer neither migrates nor
deletes these files and installs no aliases. Do not bulk-delete commands or agents.
Preserve `$opencode_root/commands/review-pr.md`, `$opencode_root/agents/ralph.md`,
and `$opencode_root/agents/ralph-reviewer.md`. The Ralph executable, `prd.json`,
`progress.txt`, and bundled discovery helper `subagents` are not renamed.

### Consolidated PowerShell agents

1. Verify an authorized installation of `powershell-expert` in each selected
   harness before retiring its predecessors. Keep `powershell-ui-architect` and
   the read-only `powershell-security-hardening` assessment role.
2. Compare each old installed file with any personal customizations and preserve
   needed copies outside discovery roots. Use the verified roots from step 1.
3. Obtain explicit approval for each exact path below before manual removal.
   Repository source retirement does not authorize deleting installed copies.

| Obsolete installed path | Replacement |
| --- | --- |
| `$codex_root/agents/powershell-5.1-expert.toml` | `$codex_root/agents/powershell-expert.toml` |
| `$codex_root/agents/powershell-7-expert.toml` | `$codex_root/agents/powershell-expert.toml` |
| `$codex_root/agents/powershell-module-architect.toml` | `$codex_root/agents/powershell-expert.toml` |
| `$opencode_root/agents/powershell-5.1-expert.md` | `$opencode_root/agents/powershell-expert.md` |
| `$opencode_root/agents/powershell-7-expert.md` | `$opencode_root/agents/powershell-expert.md` |
| `$opencode_root/agents/powershell-module-architect.md` | `$opencode_root/agents/powershell-expert.md` |

4. Review project-local registrations separately, restart the selected harness,
   and verify discovery without duplicates. No automatic deletion, global cleanup,
   compatibility aliases, or historical `prd.json`/`progress.txt` rewrites occur.

## 4. Review old Codex agents and configuration

These three roles are native OpenCode-only sources with no Codex counterparts.
Review older Codex copies of:

```text
ralph                 ralph-reviewer       sprite-artist
```

Older generated copies may still exist under `$codex_root/agents` or project
`.codex/agents`. Check the declared `name`, not only the filename. Back up and
remove only confirmed obsolete generated definitions, including older
`godot-sprite-artist` copies. Preserve all three current native sources in
`ai/opencode/agents/` and their installed OpenCode copies.

Preserve `ad-security-reviewer`, `agent-installer`, `architect-reviewer`,
`code-reviewer`, `compliance-auditor`, `security-auditor`,
`powershell-security-hardening`, and `story-reviewer`: they are supported
native Codex roles with `sandbox_mode = "read-only"` and read-only guidance, not
cleanup candidates by name. Compare customized copies with `ai/codex/agents/`
before any approved replacement. Codex receives all 128 TOML sources unchanged;
there is no exclusions file. See [agent authoring](agent-authoring.md) for source
ownership and the distinct Codex sandbox, MCP, and OpenCode tool boundaries.

The new `story-reviewer.toml` adds a role; it retires no installed paths. Preserve
its generically generated OpenCode `story-reviewer.md` counterpart too: the 128
generated agents plus three native sources total 131 OpenCode agents. That
read/glob/grep-only counterpart does not replace native `ralph-reviewer.md`.
No additional deletion or migration is needed for this addition.

Privately inspect user/project `config.toml` and companion profiles for obsolete
`[agents.<role>]` tables and `config_file` references. Aliases may use different
names. Resolve relative paths against the containing configuration, then remove
only confirmed obsolete registrations in an editor.

If a previous installation supplied `$codex_root/ralph.config.toml`, review and
back it up before removing that exact profile. The current installer does not
install it or scan for old copies. Also remove any explicit selection of the
`ralph` profile from your launcher; preserve `config.toml`, the Astra profile,
credentials, and unrelated profiles.

Also review old Jira/PostgreSQL launchers and associated fields in both harnesses.
Current `jira` uses Atlassian Rovo v2; `postgresql` uses the built local Node
[mcp-suite](https://github.com/crsiebler/mcp-suite) server at
`$HOME/Repositories/mcp-suite/servers/postgresql/dist/servers/postgresql/src/index.js`.
Back up customizations and approve exact config edits before removing obsolete
CrystalDBA/Docker commands, `DATABASE_URI` mappings, headers, or other old fields.
Preserve unrelated settings and approval rules. The current database connection
still uses `POSTGRESQL_CONNECTION_STRING`; do not remove it indiscriminately.

AWS and Elastic MCP definitions are intentionally absent from current sources,
but the installer preserves unrelated installed entries rather than deleting them.
Privately review retained `aws`/`elastic` entries in both harnesses and project
overrides, preserve needed customizations, and approve each exact configuration
edit before removal. Old `AWS_PROFILE`, `AWS_REGION`, `ELASTIC_MCP_URL`, and
`ELASTIC_MCP_AUTHORIZATION` example exports are no longer supplied. Check their
other consumers before any separately approved cleanup of private environment
files; do not remove AWS profiles or credential stores as part of this cleanup.

Old `JIRA_API_TOKEN`, `JIRA_BASE_URL`, and `JIRA_EMAIL` exports are unnecessary for
Rovo OAuth, but other projects may still use them. Remove such exports only after
checking their consumers. Do not remove the entire `.env` or revoke credentials
as part of file cleanup.

## 5. Remove old plugin registrations through their manager

Inspect the installed CLI's help and selected configuration:

```bash
CODEX_HOME="$codex_root" codex plugin list
CODEX_HOME="$codex_root" codex plugin marketplace list
CODEX_HOME="$codex_root" codex plugin remove --help
CODEX_HOME="$codex_root" codex plugin marketplace remove --help
```

After checking the exact plugin ID and backing up customizations, use its native
uninstall command. For example, replace this placeholder with the reviewed ID:

```bash
CODEX_HOME="$codex_root" codex plugin remove 'PLUGIN@MARKETPLACE'
```

Marketplace removal is a separate decision; inspect its dependents first. Do not
delete caches manually or remove the active `craft` marketplace by default. Use
the corresponding manager for skills/plugins installed by other tools.

## 6. Remove the old global subagents helper

Inspect without executing the old program:

```bash
command -v subagents
ls -ld -- /usr/local/bin/subagents
```

If it is the old executable installed by this repository, back it up if needed,
then remove exactly that file:

```bash
sudo rm -- /usr/local/bin/subagents
```

Check a symlink's target separately and preserve the target. If another package
manager owns the executable, use that manager instead. Keep `/usr/local/bin/ralph`.
The current discovery helper is bundled with the `use-subagents` skill.

## 7. Remove selected backups

Keep rollback copies until you have verified the current configuration. Inspect
adjacent `*.backup.<timestamp>` files and directory backups under the configuration
roots, including agent/command subdirectories. Older installs may also have left
`.zshrc.backup.*`, `.env.backup.*`, or binary backups under `/usr/local/bin`.

Changed OpenCode skill files are backed up under
`.install-ai-backups/<timestamp>/skills/`. Earlier manual cleanup may have created
`.install-ai-retired-skills/`, `.install-ai-retired-agents/`, or separate archives.
Inspect these individually; they may contain custom work or secrets.

Delete only reviewed backups using their full names, without wildcard deletion.
For example, if this exact file exists and is the approved backup:

```bash
ls -ld -- "$opencode_root/opencode.json.backup.20260905T120000"
rm -- "$opencode_root/opencode.json.backup.20260905T120000"
```

Inspect directory backups before removing their contents. Do not pipe a directory
listing into a deletion command or remove an entire configuration root.

## 8. Verify

Follow [current installation](ai-configuration.md), restart the selected harness,
and use a new Codex thread. Verify expected skills and agents are available and
duplicates are gone. No model invocation, live MCP call, or installation is needed
merely to inspect the filesystem. Keep private backups until verification is done.
