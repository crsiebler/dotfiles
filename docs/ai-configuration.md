# AI configuration

This guide describes the checked-in implementation, not a claim that live
authentication, model access, or every integration has been verified. Installation
and connection setup are separate, explicitly authorized operations.

## Contents

- [Sources and installed layout](#sources-and-installed-layout)
- [Installation and merge behavior](#installation-and-merge-behavior)
- [Connecting applications](#connecting-applications)
- [Native agents and Ralph limitations](#native-agents-and-ralph-limitations)
- [Validation and manual evaluation](#validation-and-manual-evaluation)
- [Troubleshooting and rollback](#troubleshooting-and-rollback)
- [Manual removal of old AI files](remove-old-ai-files.md)

## Sources and installed layout

| Source | Purpose and destination |
| --- | --- |
| `.agents/plugins/marketplace.json` | Checkout-local `craft` marketplace; no remote skill source |
| `ai/plugins/<plugin>/skills/<action>/` | Portable skill bodies, scripts, and references |
| `ai/AGENTS.md` | Single harness-agnostic personal policy; copied byte-for-byte to `AGENTS.md` in both user configuration roots |
| `ai/codex/config.toml` | Managed Codex defaults and MCP connections |
| `ai/codex/astra.config.toml` | Standalone opt-in model evaluation profile |
| `ai/opencode/{opencode.json,tui.json,astra.json}` | OpenCode config, terminal UI, and opt-in model overlay |
| `ai/codex/agents/*.toml` | 128 canonical custom-agent sources; all copied unchanged to Codex, Markdown generated for OpenCode |
| `ai/plugins/coding/skills/prepare-implementation/references/story-execution.md`, `story-review.md` | Shared execution contract and canonical staged-review protocol/JSON schema for Ralph and Codex Goal |
| `ai/opencode/agents/*.md` | Three native OpenCode-only agents: `sprite-artist`, `ralph`, and `ralph-reviewer`; copied unchanged |
| `ai/opencode/commands/` | `/create-sprite`, `/define-requirements`, `/plan-work`, `/ship`, `/find-agents`, `/recover-ralph`, and unchanged `/review-pr` |
| `scripts/install-ai.py`, `scripts/render-agents.py` | Local installer and two-harness agent renderer |
| `ai/plugins/delegating/skills/use-subagents/scripts/subagents` | Skill-bundled discovery helper |

Codex defaults to `$HOME/.codex`; an explicit `CODEX_HOME` must be absolute.
OpenCode defaults to `$HOME/.config/opencode`; an explicit `XDG_CONFIG_HOME`
must be absolute and names the parent config directory, not `opencode` itself.
Codex receives all native source copies under its `agents/` directory and plugins through
native local marketplace registration. OpenCode receives copied skills through
the existing `skills` CLI, plus generated agents, three native agents, and commands.

The root [AGENTS.md](../AGENTS.md) is separate repository-only policy, not installed
personal instructions. The installer reads `ai/AGENTS.md` with `read_bytes()` and
copies it without concatenation or normalization. Application inventories and
setup belong in this guide, not the personal policy.
Edit canonical TOML role bodies, not generated
OpenCode Markdown; edit the three OpenCode-only agents in their native Markdown.
Agent metadata lives in native sources, with generic TOML-to-Markdown rendering;
there are no exclusions or overrides JSON files.

### Four plugins and skill names

| Plugin | Skills |
| --- | --- |
| `coding` | `analyze-review-feedback`, `resolve-review-feedback`, `review-code`, `format-code`, `develop-with-tests`, `implement-feature`, `refactor-code`, `run-tests`, `verify-interface`, `manage-changes`, `write-requirements`, `prepare-implementation`, `create-sprites` |
| `reporting` | `assess-work-item`, `report-progress`, `report-project-status` |
| `researching` | `search-web` |
| `delegating` | `use-subagents` |

Use the skill identifier actually advertised by the harness; do not guess Codex
namespace syntax or cached installation paths. Resolve bundled resources from
the loaded skill location. Marketplace authentication policy is `ON_USE`, not an
instruction to log in during installation.

`search-web` selects available search, page-fetching, or multi-step research tools
by their exposed schemas. Its core guidance is provider-agnostic; Exa MCP details
are loaded conditionally from `references/exa.md`. Plugin skill discovery is
directory-based, so the rename needs no installer or manifest special case.
For retained installed `use-exa` copies and Codex plugin refresh, follow the
[rename cleanup steps](remove-old-ai-files.md#renamed-web-research-skill).

The base Codex configuration leaves the user's model selection intact. Astra is
opt-in: `astra.config.toml` selects `gpt-6-astra` with high reasoning effort;
OpenCode's `astra.json` selects `openai/gpt-6-astra` and the configured build variant.
Verify account availability and the installed harness's profile/overlay help
before activating these files. Installation does not prove model availability
or make Astra Ralph-compatible.

## Installation and merge behavior

From the checkout:

```sh
make validate-ai
# Only with explicit installation authorization, choose one:
make install-codex
make install-opencode
make install-ai
```

Python 3.11+ is required for validation, rendering, and installation; Make defaults
to `python3.11`. Codex installation requires exactly CLI 0.153.4.
OpenCode skill installation requires `skills` on `PATH`. Missing prerequisites
are blockers: no `npx` bootstrap, login, dependency installation, or binary install
is performed by these targets.

The installer registers the local checkout with Codex's native plugin interface
and adds `coding@craft`, `reporting@craft`, `researching@craft`, and
`delegating@craft`. OpenCode uses local `skills add` copies rather than symlinks.
The checkout must remain available for subsequent local marketplace refreshes.

Managed JSON/TOML keys override existing values; unrelated keys survive.
Arrays are replaced rather than unioned. MCP transport changes remove incompatible
local process fields when moving to remote transport and obsolete URL/header
fields when moving to local transport. Changed local commands clear old process
fields, and managed process environment maps are replaced atomically rather than
accumulating old credentials. Environment references remain references; the
installer does not substitute secret values into configuration.

Remote endpoint changes also discard inherited OAuth, bearer-token environment
bindings, and HTTP/header maps before applying the new managed bindings. Old
credentials must not follow a connection name to a different URL.

Before managed writes, installation accepts only the source's exact read-tool
exceptions within protected MCP namespaces. It refuses other overlapping OpenCode
allow rules (including inline agent permission/tool overrides), Codex overrides
that bypass write prompts, and expanded research-tool allowlists. Reconcile those
rules manually; errors do not print their values. Managed OpenCode namespace rules
precede their exact exceptions; retained custom denies are ordered afterward.
An existing bare/trailing Exa or Context7 namespace deny requires reconciliation
before adding exceptions, because it may be an intentional blanket restriction.
Codex tool disables (`enabled = false`) survive merging; unsupported approval
values such as `deny` are rejected instead of being silently replaced by approval.
These checks also cover installed companion configs and Codex profiles, not
arbitrary project configuration; inspect project-level overrides separately.

Destination symlinks and conflicting skill assets are refused to protect files a
CLI directory replacement could lose. Reconcile `opencode.jsonc` manually if
present; the installer will not choose between it and `opencode.json`. Native
marketplace source collisions also require explicit reconciliation rather than
silently repointing a registration.

TOML is serialized into normalized formatting, so comments and original layout
are not preserved in the installed merged file. Changed files receive adjacent
timestamped backups. User-level `AGENTS.md` and same-name shipped agents/commands
are replaced, not prose-merged. Changed OpenCode skill files are backed up under
`.install-ai-backups/<timestamp>/skills/`. Unrelated files and stale assets are
not removed automatically.

Writes use per-file atomic replacement, but installation is not a whole-operation
transaction. A later native CLI failure can leave earlier files installed. Native
Codex configuration changes are backed up even if the native command fails.

AI-only targets do not touch shell files, `.env`, global Git settings, or binaries.
Broad `make install` does all of those for shell/OpenCode/Ralph setup
and requires `sudo` for Ralph. It does not install Codex or global subagents.

## Connecting applications

Connection definitions are not authenticated sessions. Use the installed
harness's help or current provider documentation for its actual login interface;
do not invent cross-harness CLI syntax. Installation never performs a login.
Approve authentication separately, keep credential stores private, and inspect
actual exposed tool schemas after connection. Tool presence is not authorization
to write external state.

| Connection | Default | Authentication/context |
| --- | --- | --- |
| `github` | Enabled globally | `GITHUB_MCP_TOKEN`; hosted GitHub MCP |
| `exa` | Enabled globally | `EXA_API_KEY`; hosted Exa MCP |
| `context7` | Enabled globally | `CONTEXT7_API_KEY`; hosted Context7 MCP |
| `jira` | Disabled | Atlassian Rovo v2 OAuth; `ATLASSIAN_CLOUD_ID` is site context |
| `postgresql` | Disabled | Project least-privilege database URI and built local Node `mcp-suite` server |

AWS and Elastic MCP definitions are intentionally absent from both source configs.
Installation preserves unrelated installed entries, so older definitions may
remain until individually reviewed and removed with approval. See
[manual cleanup](remove-old-ai-files.md#4-review-old-codex-agents-and-configuration).

OpenCode additionally retains disabled optional Chrome DevTools, Playwright, Jam,
and ElevenLabs connections. Their presence does not authorize starting them or
downloading their runtime packages.

### Tool approval policy

| Service | Without tool approval | Requires tool approval |
| --- | --- | --- |
| GitHub | Exact configured repository, commit, issue, PR, search, and review reads | Edits, comments/reactions, pushes, branches, merges, settings and other mutations; unknown tools |
| Exa | Search, advanced search, fetch, and `agent_run` research | Other tools are denied/filtered, not merely prompted |
| Context7 | `resolve-library-id` and `query-docs` | Other tools are denied/filtered |
| Jira/Rovo | Exact documented reads, searches, discovery, and `executeRead` | Writes, destructive operations, and unknown tools |
| PostgreSQL | `check_dangerous_operations_allowed` | `execute_query` and unknown tools |
| Chrome, Playwright, Jam | All tools when the connection is enabled | No MCP tool-level prompts |
| ElevenLabs | None | Every tool, including reads |

GitHub/Jira/PostgreSQL use default `ask` in OpenCode and `prompt` in Codex, with
exact read exceptions (`allow` / `approval_mode = "approve"`). Exa/Context7 use
default deny plus exact allows in OpenCode; Codex filters them with `enabled_tools`
and approves those exact tools. Neither relies on broad `get_*`/`search_*` patterns
or server annotations to automatically approve newly introduced tools.

This policy does not enable disabled servers. Browser/audio connections remain
OpenCode-only; no new Codex connections are installed. The eight inspection agents
and `ralph-reviewer` retain their narrower permissions. Project/runtime overrides
can still change effective behavior and need separate inspection. MCP rules do not
control `git push` or `gh` through shell tools. Existing user-authorization rules
for external actions and `/review-pr --post` remain in force even when a browser
tool itself needs no permission dialog. Research calls may consume service quotas.

Rovo tool discovery varies by tenant and authentication. The exact names cover
the [v2 catalog](https://developer.atlassian.com/cloud/rovo-mcp/guides/supported-tools/)
and directly exposed reads in the
[support catalog](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/).
`executeRead` is the documented read dispatcher; `executeWrite` and
`executeDestructive` still prompt. Reads may include Confluence and connected
Teamwork Graph content. Attachment retrieval can return a download command;
executing that command is a separate operation, not part of the MCP allow rule.

PostgreSQL tool names and behavior were inspected at MCP-suite commit
[`2a2881a`](https://github.com/crsiebler/mcp-suite/blob/2a2881a5986d22349dd9fcec84820cd58656ed61/servers/postgresql/src/tools/index.ts).
There is no separate read-query tool. `execute_query` accepts arbitrary SQL and
can perform writes depending on server configuration; it always asks, even for
`SELECT`. These dotfiles neither classify SQL nor change database privileges.
Upstream tool changes require reviewing and updating the exact exceptions in both
source configs. Static/fake tests do not prove live server behavior.

### GitHub, Exa, and Context7

GitHub uses `https://api.githubcopilot.com/mcp/` with only
`repos,issues,pull_requests` toolsets. Use a fine-grained PAT with one resource
owner, selected repositories, minimal permissions, and an appropriate expiry.
One fine-grained token does not span multiple resource owners; plan distinct
approved credentials/configuration for other owners. Organization approval or SSO
requirements may apply. Do not broaden permissions just to remove an error.

OpenCode supplies `Bearer {env:GITHUB_MCP_TOKEN}` with OAuth disabled; Codex uses
`bearer_token_env_var`. Exact read tools skip approval; other calls retain
`github_*: ask` / `default_tools_approval_mode = "prompt"`. Restricted toolsets are
not a read-only guarantee. Never print token values to troubleshoot the installer
preflight.

The `/review-pr` command uses separately authenticated `gh`. Its canonical
objectives, schema, context gathering, and orchestration live in
[`ai/opencode/commands/review-pr.md`](../ai/opencode/commands/review-pr.md).
`--post` must preview the exact GitHub review command or API payload and obtain
explicit confirmation before any review write. MCP write access does not waive it.

Exa uses its hosted endpoint with search, fetch, advanced search, and agent-run
tools; Context7 uses `https://mcp.context7.com/mcp`. The supplied environment keys
are referenced by headers in both harness configurations. Successful source validation proves
neither remote service access nor account quotas.

### Trusted project opt-in

Keep project integrations disabled in personal defaults. In a trusted project,
review the effective configuration and enable only the needed connection using
the harness's project configuration (`.codex/config.toml` or OpenCode's project
configuration). Preserve approval prompts and least-privilege credentials.
Project configuration itself is not consent to Docker lifecycle, migrations,
cloud mutations, or other sensitive operations.

**Atlassian Rovo:** The connection name is `jira`, and its provider is
`https://mcp.atlassian.com/v2/mcp`. Use harness-supported OAuth with an approved
Atlassian account/site. `ATLASSIAN_CLOUD_ID` identifies the site, not a credential.
Headless token authentication is a separate, explicitly approved setup using the
provider's current supported method; no token header recipe is installed here.
Inspect the exposed Rovo v2 tool schemas before use.

**PostgreSQL:** Both configurations refer to the custom local Node server from
[mcp-suite](https://github.com/crsiebler/mcp-suite), built at
`$HOME/Repositories/mcp-suite/servers/postgresql/dist/servers/postgresql/src/index.js`.
Keep the connection disabled until trusted project opt-in. Node must be available
on the harness's `PATH`, and the built entry point must exist. Follow the upstream
project's setup documentation; this installer does not clone, build, or install
`mcp-suite`, install Node, or verify the server's dependencies.

Codex uses `sh -c` with `exec node` and a quoted `$HOME` path; its `env_vars`
passes `HOME` and `POSTGRESQL_CONNECTION_STRING`. OpenCode invokes `node` directly
with `{env:HOME}` in the entry-point argument and an environment reference for
`POSTGRESQL_CONNECTION_STRING`. Neither configuration puts the URI in argv,
maps it to `DATABASE_URI`, or uses Docker.

Export `POSTGRESQL_CONNECTION_STRING` privately in the launching environment.
The launchers do not preflight missing or empty connection strings; validating
the connection string and enforcing server behavior are the server's
responsibility, not guarantees supplied by these dotfiles. Use a project-specific,
least-privilege database identity, not a superuser or production connection by
default. Preserve approval prompts and never dump environment values or connection
strings into logs. Configuration alone does not establish read-only enforcement.

## Native agents and Ralph limitations

The renderer validates 128 canonical TOML sources and copies all 128 byte-for-byte
to Codex. OpenCode receives 128 generated Markdown agents plus the separately
copied, byte-identical `sprite-artist.md`, `ralph.md`, and `ralph-reviewer.md`
(131 total). Those three native Markdown roles are OpenCode-only.

`ad-security-reviewer`, `agent-installer`, `architect-reviewer`, `code-reviewer`,
`compliance-auditor`, `security-auditor`, `powershell-security-hardening`, and
`story-reviewer`
use native `sandbox_mode = "read-only"`
and read-only role guidance: inspect and recommend without tests, edits, mutating
commands, or external posts. Codex allows runtime-authorized read-only shell
inspection. OpenCode maps this setting to deny-all plus `read`/`glob`/`grep`, a
more restrictive tool policy, not equivalent Codex sandbox or MCP enforcement.
Codex parent runtime permission overrides apply after role settings, and MCP
approvals are independent. These settings do not guarantee immutable per-role
policy or project-only access.

For each selected harness, the installer invokes the Python renderer with
`--harness` and `--check`, then `--output` into local staging before installation;
validation alone does not write agent output.
See [agent authoring](agent-authoring.md) for full renderer semantics and tests.

Native delegation must invoke a registered role, not merely inspect or role-play
its definition. `use-subagents` is optional discovery tooling, not a prerequisite
for every delegation. Unsupported roles stay unsupported.

The supported Ralph loop is:

```sh
ralph --mode standard --max-iterations 10
```

Invoking `ralph` authorizes scoped implementation, needed dependencies/checks, and
one commit per passing story, as defined in the native Ralph agent. The runner
supplies only invocation metadata; stable rules live in the agent and shared
execution/control references. It grants no pushes, external posts, or
sensitive-operation approvals.
The separate `--authorize-story-commits` flag is removed.

The single-file Python supervisor requires Python 3.11+, POSIX, Git, configured
OpenCode, installed Ralph agents, and a clean initial worktree with valid
`plan.json` committed on exactly `branchName`. It no longer requires jq at runtime.
Detached HEAD, `main`, `master`, and branch mismatch are rejected without branch
repair. `--auto` is unsupported and rejected, not an opt-in approval mode.

Ralph supports only OpenCode; there is no harness selector or Codex execution
profile. A fully complete plan needs no OpenCode; existing stop/interrupted state
still blocks until reconciled. Git is needed to inspect possible persisted state.

Ralph additionally loads the installed skill's `references/ralph-control.md`.
Before launching, it persists runner-owned `running` state and a unique iteration
ID. The agent writes the supplied project-local outcome file, not the ledger.
Only a matching completed/committed story or evidence-backed retryable handoff
permits another session. Human blockers, failed/missing handoffs, and crashes do
not auto-retry. Recovery preserves the verified candidate and has a default budget
of two additional sessions per story across invocations. Every attempt retains the
bounded initial/targeted review cycle; retries do not mean unlimited reviews.

`--iteration-timeout N` sets an optional wall-clock limit in seconds (default 0,
unlimited). Timeout or signals terminate the managed process group and stop; no
provider-specific usage-limit detection is claimed. `.ralph-stop` is unconditional,
including while running. Clear it only after human review; `--resume` accepts a
reconciled baseline but preserves counters and committed-completion requirements.
See [stop/recovery and cleanup](../README.md#stops-crashes-and-bounded-recovery).
The ledger is in per-worktree Git metadata; outcome files are in the worktree even
for linked worktrees. The runner rejects tracked stop/outcome files. Initial dirty
work and submodules are refused, and ignored files are outside snapshot coverage.
Runner ownership is not OS isolation from an unrestricted same-user process.

Use `ralph --status` for a read-only diagnostic snapshot; it creates no state or
lock files and never starts OpenCode. Its success exit code means a report was
produced, not that a blocked run is ready. The `recover-ralph` skill (OpenCode
`/recover-ralph`) guides the primary interactive assistant through assessment,
approved repair, verification, and preparation. Its default endpoint does not
restart the loop. Exact stop-file removal and launch require preview and explicit
confirmation; this exception never permits the autonomous Ralph agent to clear
its own stop. No ledger edits, counter resets, or fabricated outcomes are allowed.
See [the recovery runbook](ralph-recovery.md) for approval and resumption details.

`prepare-implementation` selects its default from active-harness identity supplied
by trusted runtime context or the invoking native entry point:
OpenCode produces Ralph-compatible `plan.json`; Codex produces a Markdown checklist
in `PLAN.md`. The native `ai/opencode/commands/plan-work.md` wrapper supplies the JSON
default. Explicit user output requests override the default. If routing is
unavailable or ambiguous, ask about the format; do not infer the active harness
from `PATH`, installed binaries, directories, environment variables, inspected
source text, or user-policy headings.

Codex can use native `/goal` for an approved checklist. Planning does not launch
execution or create execution logs/memory. Goal inherits Ralph's full shared
execution, memory, review, prepared-branch, and per-story commit contract, using
Markdown checkboxes rather than JSON `passes`. Both executors load
`references/story-execution.md` and `references/story-review.md` in full relative
to the advertised installed `prepare-implementation` skill, never checkout or
hardcoded plugin-cache paths. The executor sends the full canonical protocol to
the reviewer wrapper; wrappers do not own separate schemas.

Goal requires explicit scoped execution and story-commit authorization, an
existing commit, and the plan's exact prepared working branch. Reject detached
HEAD, `main`, `master`, and mismatch before any writes; never create/switch branches.
A quoted launch template is not authorization. Both use fast/standard/deep risk
budgets, at most two read-only implementation advisors, and budget-selected self
or native review with one initial pass and at most one targeted same-session pass.
Native Codex review requires `story-reviewer`; OpenCode Ralph still requires its
native `ralph-reviewer`, with `steps: 3` and the exact staged-Git allowlist. The
generic generated OpenCode `story-reviewer` has no shell access and is not a
substitute. Codex's tool-turn budget is behavioral, not equivalent hard enforcement.

Keep task sources limited to the stable plan, completion state, and concise current
status, worktree-root `docs/progress.md` append-only, and root `memory.json` at version 1 with at most
20 patterns and 20 suppressions. Missing memory is normal; invalid memory blocks
without overwrite. Update memory only after passing review, promoting reusable
accepted fixes with verification and suppressing only evidenced false positives.
Only durable guidance belongs in the nearest `AGENTS.md`.
Create the journal only for a permitted execution checkpoint, never during planning
or requirements drafting. Do not read or migrate legacy execution logs. After full
verified delivery, use the separately approved
[completed-run archive](../ai/plugins/coding/skills/prepare-implementation/references/completed-run-archive.md)
for the plan, journal, and memory together; Ralph must first validate completion
and exit. PRD replacement separately requires approved archival and verified
preservation before replacement, never automatic execution-state cleanup.

Missing required protocol/reviewer/session, failed required checks/review, invalid
memory, or failed commit stops delivery with the story pending. Passing checks
and review plus a successful authorized story commit establish completion; restore
only the provisional task marker if finalization/commit fails. Preserve unrelated
work and append blockers and resumption evidence. Record actual runtime/model/source,
mode, limits, and reviewer session provenance, marking unknowns. Goal retains
native continuation/compaction, not Ralph's external hard iteration limit,
fresh-session loop, or completion sentinel.
See [Codex goals](codex-goals.md); automatic checkpoint compaction is
[backlogged](backlog.md), with no hook or controller installed.

## Validation and manual evaluation

Repository-local commands:

```sh
make validate-ai
python3.11 -m unittest discover -s tests -p '*test*.py'
python3.11 tests/agent_contract_test.py
bash tests/ralph_model_test.sh
bash tests/ralph_review_test.sh
bash tests/zsh_aliases_test.sh
zsh -n aliases/.aliases zsh/.zshenv zsh/.zshrc
```

There is no standalone repository typecheck target. `validate-ai` checks local
plugin structure, JSON/TOML syntax, and both Python renderer targets without
starting a harness or MCP. Python tests cover installer merging and backups,
environment sync, discovery, and an isolated native plugin contract. That native
test skips when Codex is missing or not 0.153.4; report skips rather than claiming
live compatibility. Ralph tests exercise runner/model and review contracts;
`tests/ralph_review_test.sh` uses Ruby only to validate native reviewer YAML.
Ruby is not an installer dependency.

MCP contracts retain explicit expected connection sets, schema projections,
approval rules, and secret-reference checks. PostgreSQL transport tests run a fake
`node` in project-local scratch space with an allowlisted environment and a `HOME`
containing spaces and shell metacharacters. They check argv, path resolution,
connection-string passthrough, exit status, and secret-free output, including a
missing-Node failure. OpenCode's known environment substitutions are modeled in
the test, not exercised through its real configuration loader. No real
`mcp-suite` server or database starts; these tests do not verify server-side
connection validation, database permissions, or live harness integration.

The following are **manual evaluation cases, not recorded successful runs**:

- After authorized installation, restart each harness and verify skill/role
  discovery, intended source checkout, and native
  delegation. Start a new Codex thread after plugin changes.
- Test an approved scoped GitHub read and verify the prompt; draft a PR review
  without posting. Verify `--post` stops at the exact payload confirmation gate.
- Connect Exa and Context7 with an approved minimal request; record service and
  credential errors without secret values.
- Enable each project integration separately and verify account/site or database
  identity using approved non-mutating requests. Confirm other
  project connections remain disabled. Do not test mutation by performing it.
- In an authorized disposable project, evaluate one bounded OpenCode Ralph story
  and inspect check evidence, staged-review budget, history, and memory.
- Separately evaluate Codex Goal's shared contract: prepared-branch guards,
  native `story-reviewer` and same-session targeted review, memory validation,
  interrupted resumption, and failed checks/review/commit leaving a pending story.
  Source checks do not establish these live execution outcomes.
- Evaluate planning format selection with
  `tests/fixtures/implementation_planning_evals.json`. These are manual evaluation
  cases, not recorded model results. Verify both native defaults, explicit format
  overrides, preservation of existing plans, and generation without execution.
- Evaluate task scenarios in `tests/fixtures/agent_evals.yml` only with approval;
  record runtime/model, inputs, grader, repetitions, observed outcomes, latency,
  tokens, and cost basis. Static tests do not establish behavioral safety or speed.

## Troubleshooting and rollback

### Installer output and errors

Installation checks required executables and the Codex version before rendering;
`validate-ai` needs neither Codex nor `skills`. Progress is flushed plain ASCII:
preparation counts describe staged agents, not installed files. Destination paths,
config/policy completion, actual agent/command totals, and each successful plugin
or skill bundle are reported separately. The standalone renderer still emits its
machine-readable JSON; the installer does not expose that JSON or staging paths.

Errors identify the phase and, where available, the file and parse location or
safe filesystem error category. CLI errors identify the operation and exit status;
malformed CLI JSON is reported as a response error, not a broken config file.
Raw parser messages, configuration values, and subprocess output are withheld.
Inspect the named location privately; do not paste credentials into diagnostics.
Failures before managed writes say so, distinguishing destination preflight that
may create directories or CLI state from installation. Once managed writes start, the
installer reports completed file/plugin/bundle counts and warns that changes may
remain, including changes by a failed CLI. It does not automatically roll back.

| Symptom | Action |
| --- | --- |
| Missing `skills`, Python, or compatible Codex | Stop and arrange approved prerequisite installation; do not silently download |
| Missing GitHub token | Securely export `GITHUB_MCP_TOKEN` in the launching shell; never print it |
| Symlink, conflicting skill asset, or JSONC error | Reconcile manually; do not delete custom data to pass preflight |
| `craft` source clash | Review native plugin registration and explicitly reconcile the intended checkout |
| Old AWS/Elastic MCP still appears | Review retained installed/project definitions and approve individual cleanup; source removal does not delete installed entries |
| PostgreSQL Node or entry point unavailable | Verify Node on the harness's `PATH` and the built `mcp-suite` path; follow upstream setup with approval |
| PostgreSQL connection validation fails | Check the private launching environment and upstream server requirements; the launcher does not validate the URI |
| Wrong implementation-plan format | Check explicit user requests and active-harness identity from trusted runtime context or the native entry point; ask if routing is unknown |
| Changes not visible | Restart the harness, start a new Codex thread, and inspect duplicate discovery roots |

Retain backups until the intended configuration works. For rollback, inspect and
restore only approved per-file backups and skill assets; reconcile native plugin
registration separately if needed. Installation may have partially completed.
Preserve approval rules; do not broaden permissions as an automatic rollback step.

For individually approved cleanup, follow [manual removal](remove-old-ai-files.md).
`make clean` removes `.zshrc` backups only; AI cleanup remains manual. Never
delete an entire configuration root to remove backups.
