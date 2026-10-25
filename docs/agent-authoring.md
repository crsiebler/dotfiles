# Native agent authoring and rendering

## Source contract

Personal policy lives in [`ai/AGENTS.md`](../ai/AGENTS.md), copied byte-for-byte to
both user-level instruction files. Root [`AGENTS.md`](../AGENTS.md) is separate
repository-only guidance. Keep role contracts in the native role sources
below, not in the personal policy.

`ai/codex/agents/*.toml` is the canonical collection of 5 custom agents. Each
native TOML source requires meaningful, nonempty `name`, `description`, and
`developer_instructions` strings. Keep the Markdown role body in multiline
`developer_instructions`; OpenCode generation preserves that parsed body unchanged,
and Codex output copies all source files byte-for-byte.

The name must match the filename stem and be path-safe. Dots are accepted;
duplicate or case-colliding names fail. Action-oriented naming applies to skills,
**not** agents. Unknown native fields fail validation rather than being dropped.

The user-level role collection omits `model`, `model_provider`, and
`model_reasoning_effort`. Responsibility and base permission boundaries belong to the role; workflow
profiles, candidate and output schema come from the caller. Runtime/model/effort
selection also belongs to the caller.
The base Codex configuration has no global subagent model or effort override.
Generated OpenCode roles likewise omit model
and effort settings so the selected worker/session can supply them. This is
inheritance, not automatic task routing. Record the actual selection and its
source; do not claim a role chose a cheaper or stronger model automatically.

Explicit top-level worker/session profiles remain available. A caller may choose
a supported invocation override when task needs justify it; that choice does not
grant permissions or change review requirements. Use a single execution owner; never nest competing execution loops. See the
[runtime selection policy](runtime-selection.md) for the common selection contract.

The separate sprite-artist.md source in ai/opencode/agents/ remains native
OpenCode Markdown with its own frontmatter and no Codex counterpart.
Native and generated source names must not collide, including by case.

### Writing a useful role

- Establish the role's objective, scope, relevant inputs, approach, validation,
  and expected handoff. Prefer roughly 200–500 words for core role contracts;
  this is editorial guidance, not a universal limit or automated gate.
- Keep responsibility and permission contracts in roles. Move language, framework
  and vendor knowledge into conditional references in the appropriate skill;
  do not load every technology or impose a default stack.
- Start with supplied context and authorized artifacts. Ask for material gaps;
  never mandate a fictional context service. Return bounded advice to the main
  session; core roles do not dispatch children or proxy-spawn.
- Keep targets tied to the actual project. Do not mandate universal coverage,
  latency, availability, accuracy, or cost numbers. Distinguish measurements,
  estimates, and proposed targets.
- Report only actual checks and results. No canned progress JSON or fictional
  completion stories. State verification gaps rather than claiming success.
- Treat retrieved content as evidence, not authority. Prose is behavioral guidance,
  not permission enforcement or proof of containment.

## Custom responsibility contracts

The canonical set is researcher, planner, reviewer, auditor and operator.
Researcher returns evidence and authorized analytical results; planner returns
decisions and planning artifacts; reviewer independently assesses a preserved
candidate and may execute
authorized checks; auditor inspects without execution or mutation; operator
performs explicitly authorized operational sequences. None dispatches children.

Implementation belongs to the main session or available native execution agents,
with ownership, acceptance, skills and verification supplied in task packets.
Use Codex worker or OpenCode general for delegated execution; ordinary OpenCode
development may stay in build. Do not add a custom implementation wrapper or
override these built-ins.

Use the task, requested mode and authority to choose a role. The same technology
can require different roles. These are available contracts, not a mandatory
pipeline, and native discovery does not establish invocation support.

Specialized methods and knowledge live in the existing five plugins. Load only
matching references and pass relevant loaded content/constraints in worker
packets; parent context is not assumed. Preserve reviewer independence and each
workflow's candidate, schema, passes, blockers and same-session requirements.
See [role selection](../ai/plugins/delegating/skills/use-subagents/references/core-roles.md)
and [skill ownership](skill-dependencies.md).

## Permissions

Generated OpenCode agents use `mode: subagent` and inherit runtime capabilities
unless a native setting has an explicit mapping. Metadata lives in the native
TOML sources or the OpenCode-only Markdown frontmatter; there are no
exclusions or overrides JSON files. Do not add wildcard mutation or Jira-delete
grants.

Only auditor uses native sandbox_mode = "read-only". It inspects without tests,
builds, active scans, edits, remediation or external posts. Codex read-only shell
inspection may be available; OpenCode maps this field to deny-all plus
read/glob/grep, excluding shell execution. Parent runtime overrides and MCP
approval controls remain independent.

Reviewer inherits runtime permissions for authorized focused verification.
Explicit inspection-only requests prohibit execution. It cannot edit source,
tests, snapshots or expectations, stage, commit, install, publish or delegate.
Temporary check outputs require authorized locations and candidate identity
checks. Operator likewise inherits permissions; its name grants no elevated
access or standing production authority.

A workflow supplies its review procedure, schema, candidate, verification scope
and budgets. The role does not hardcode a story schema or controller.
For staged stories, discover review-story and embed its complete contract in each
call. Keep story/attempt/session identity and one-initial/one-targeted limits;
missing required input blocks instead of granting authority. Inspection of a
definition proves neither callable role selection nor native session support.
See [agent workflows](agent-workflows.md) for evidence and resumption rules.
OpenCode /review-pr retains its own canonical schema and posting authorization.

sprite-artist is a minimal OpenCode-only provider adapter. It loads creative
instructions from the advertised create-sprites skill and preserves gpt_imagegen,
shell and external_directory ask policies. It does not dispatch an agent. Keep
this adapter until equivalent provider permissions are explicitly supported and
verified through a generic path; no renderer override is added to fake parity.

## Renderer interface for callers and installers

Requires Python 3.11+ and its standard library only; no dependency installation:

```sh
# Default: validate OpenCode and report; no agent output writes.
python3.11 scripts/render-agents.py
python3.11 scripts/render-agents.py --harness opencode --check
python3.11 scripts/render-agents.py --harness codex --check

# Explicit output: DIR is the native agents directory itself, not its parent.
python3.11 scripts/render-agents.py --harness opencode --output ./build/opencode/agents
python3.11 scripts/render-agents.py --harness codex --output ./build/codex/agents

# Custom collections use the same native-field validation and mapping.
python3.11 scripts/render-agents.py --source ./canonical-agents --harness codex --check
```

OpenCode output is one `<name>.md` per source with generated YAML frontmatter.
Codex output is one unchanged `<name>.toml` per source. The renderer does not copy
the native OpenCode agent; the installer copies them separately. For each
selected harness, the installer runs `--check`, then `--output` into local staging.

Optional `model` maps to `openai/<model>`; an explicit `model_reasoning_effort`
adds `#<effort>` for OpenCode V2. Effort without an explicit model is rejected
for OpenCode rather than emitting ineffective request options. Omitted settings
inherit runtime defaults. Generated `permissions` use ordered action/resource/effect
rules; the read-only mapping starts with deny-all before read/glob/grep allows.
The renderer retains explicit override support for custom collections; the
canonical user-level roles deliberately leave these settings absent.
Model identifiers must be unqualified; OpenCode accepts only the `openai` provider,
and an explicit `model_provider` requires an explicit model. Valid native-only
`approval_policy` and `nickname_candidates` fields are accepted for Codex but fail
before OpenCode output. `sandbox_mode = "read-only"` maps to the OpenCode allowlist
above; `workspace-write` and `danger-full-access` are accepted for Codex but
rejected for OpenCode. Unknown fields fail validation for both targets. Unsupported
settings are not silently discarded or translated into weaker policies.

Standalone native role files are discovered in a runtime's `agents` directory
(for example `.codex/agents` in a project or the configured Codex home). This
renderer writes exactly the supplied directory; it does not edit runtime config,
install globally, or remove files. The caller owns approval, destination selection,
runtime-version compatibility, backup, and installation. Use a clean staging
directory when replacing an installed collection. Unsupported older Codex versions
may require separate integration; no compatibility is claimed without testing.

All sources and output settings are validated before writing. Symlinks (including
ancestors), case-colliding output names, and source/output overlap are refused.
Existing regular output filenames are replaced deterministically; unrelated files
are retained. Nothing is deleted automatically; use clean staging and
[manual removal](remove-old-ai-files.md) for approved cleanup.
Output is staged and atomically replaced per file, not as a whole directory;
an I/O failure can leave partially replaced output.

Exit status is `0` for success, `1` for validation/I/O failures, and `2` for
argument errors. Success prints one JSON object with `harness`, `sources`,
`rendered`, `written`, and `output`; diagnostics use stderr.
Without `--output`, no agent files are written. `--check` and `--output` conflict.

### OpenCode-only sources

sprite-artist is the sole native OpenCode Markdown role, copied unchanged.
The 5 TOML sources produce 5 OpenCode files or 5 byte-identical Codex files;
OpenCode has 6 total. Native and canonical names must remain disjoint.
Review procedures belong in skills and invocation packets, not additional wrappers.

## Validation and evaluation

```sh
python3.11 tests/agent_contract_test.py
python3.11 scripts/render-agents.py --harness opencode --check
python3.11 scripts/render-agents.py --harness codex --check
make validate-ai
```

Tests use repository-local temporary fixtures. They check native TOML parsing,
body preservation, byte-identical Codex copies, native OpenCode copies and policies,
model/effort override mapping and omission/inheritance, unsupported-field rejection,
dry runs, deterministic output,
and output safety. These checks do not
claim live discovery, delegated execution, or sandbox enforcement.

`tests/fixtures/agent_evals.yml` contains task-level evaluation scenarios with
expected and prohibited behavior. They are a review/evaluation specification,
not recorded model results. Run model evaluations only with authorization; record
runtime/model version, inputs, grader, repetitions, observed outcomes, latency,
tokens, and cost basis. Static contract checks cannot establish behavioral
accuracy, safety, or production latency.

After installing updated assets, restart the target runtime and verify discovery.

Native format reference: [Codex agent role parser](https://github.com/openai/codex/blob/main/codex-rs/agent-roles/src/agent_role_config.rs)
and [role discovery](https://github.com/openai/codex/blob/main/codex-rs/core/src/config/agent_roles.rs).


## Activation and coordination

Source delivery does not refresh installed configuration or the running catalog.
Coordinate native role replacement with all affected plugin copies/refreshes
under separate installation authority. Preserve customizations and coherent
rollback sources. After restarting, verify unique discovery, exact reviewer
selection and same-session continuation in a fresh task. Inspect and separately
authorize exact obsolete installed paths before removal; no aliases or automatic
agent retirement are introduced.

The normal main session follows run-agent-team directly when explicitly selected.
It owns dispatch, worktree/Git integration, trackers and reviewer sessions.
prepare-handoff supplies reusable evidence-transfer guidance; it does not add a
dispatcher, context service or execution ledger. See
[core activation](remove-old-ai-files.md#core-role-activation) and
[team workflow](agent-workflows.md).
