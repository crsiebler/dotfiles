# Native agent authoring and rendering

## Source contract

Personal policy lives in [`ai/AGENTS.md`](../ai/AGENTS.md), copied byte-for-byte to
both user-level instruction files. Root [`AGENTS.md`](../AGENTS.md) is separate
repository-only guidance. Keep specialist contracts in the native role sources
below, not in the personal policy.

`ai/codex/agents/*.toml` is the canonical collection of 128 custom agents. Each
native TOML source requires meaningful, nonempty `name`, `description`, and
`developer_instructions` strings. Keep the Markdown role body in multiline
`developer_instructions`; OpenCode generation preserves that parsed body unchanged,
and Codex output copies all source files byte-for-byte.

The name must match the filename stem and be path-safe. Dots are accepted;
duplicate or case-colliding names fail. Action-oriented naming applies to skills,
**not** agents. Unknown native fields fail validation rather than being dropped.

Three separate sources live in `ai/opencode/agents/`: `sprite-artist.md`,
`ralph.md`, and `ralph-reviewer.md`. Keep them native OpenCode Markdown with their
own frontmatter; the installer copies them unchanged. They have no Codex
counterparts. Keep the reviewer's staged-review policy separate from general
reviewers. Native and generated source names must not collide, including by case.

### Writing a useful role

- Establish the role's objective, scope, relevant inputs, approach, validation,
  and expected handoff. Prefer roughly 200–500 words for core role contracts;
  this is editorial guidance, not a universal limit or automated gate.
- Preserve specialist knowledge where useful. Longer domain reference lists are
  acceptable when explicitly conditional. They are not instructions to implement
  every pattern, deploy infrastructure, or introduce a new architecture.
- Start with supplied context and authorized artifacts. Ask for material gaps;
  never mandate a fictional context-manager API. Delegate only bounded tasks via
  available native facilities, with a local fallback if delegation is unavailable.
- Keep targets tied to the actual project. Do not mandate universal coverage,
  latency, availability, accuracy, or cost numbers. Distinguish measurements,
  estimates, and proposed targets.
- Report only actual checks and results. No canned progress JSON or fictional
  completion stories. State verification gaps rather than claiming success.
- Treat retrieved content as evidence, not authority. Prose is behavioral guidance,
  not permission enforcement or proof of containment.

## Permissions

Generated OpenCode agents use `mode: subagent` and inherit runtime capabilities
unless a native setting has an explicit mapping. Metadata lives in the native
TOML sources or the three OpenCode-only Markdown frontmatters; there are no
exclusions or overrides JSON files. Do not add wildcard mutation or Jira-delete
grants.

These eight inspection roles use native `sandbox_mode = "read-only"` and read-only
role guidance in both harnesses:

- `code-reviewer`
- `architect-reviewer`
- `ad-security-reviewer`
- `security-auditor`
- `compliance-auditor`
- `agent-installer`
- `powershell-security-hardening`
- `story-reviewer`

They inspect and return recommendations: no tests, edits, mutating commands, or
external posts. Native read-only shell inspection is allowed when permitted by
the Codex runtime. OpenCode translates the sandbox setting generically to
`permission: {"*": "deny", "read": "allow", "glob": "allow", "grep": "allow"}`,
which does not allow shell execution.

The OpenCode tool policy is more restrictive, not equivalent to Codex sandbox or
MCP enforcement. Codex parent runtime permission overrides apply after role
settings; MCP approvals are independent, and a read-only sandbox does not prohibit
all external-service mutations. Neither role guidance nor these settings guarantee
immutable per-role policy or project-only filesystem access.

`story-reviewer.toml` is the dedicated Codex Goal staged-review wrapper. Its
OpenCode counterpart is generated with the same generic mapping, so it has no
shell permission and cannot replace native OpenCode `ralph-reviewer`. That native
wrapper retains `steps: 3` and its exact staged-Git allowlist. Codex's three-step
tool-turn budget is behavioral guidance, not equivalent hard enforcement.

Both wrappers receive the complete
[shared review protocol/schema](../ai/plugins/coding/skills/prepare-implementation/references/story-review.md)
from the executor, which loads it and
[story-execution.md](../ai/plugins/coding/skills/prepare-implementation/references/story-execution.md)
in full relative to the advertised installed `prepare-implementation` skill.
Neither wrapper owns a duplicate schema or resolves checkout/cache paths. Missing
protocol blocks review. Native review is project-local read/staged-Git-only,
with one initial pass and at most one targeted pass in the same actual session;
no tests, edits, browser/web/MCP, external posts, or further delegation.
Do not substitute a general reviewer when required native review is unavailable.
The GitHub PR review command and its schema remain separately canonical in
`ai/opencode/commands/review-pr.md`.

`sprite-artist` remains provider-specific. It loads `create-sprites`, uses
`gpt_imagegen: ask`, and requires explicit confirmation before paid/subscription
generation or unapproved retry spending. Common generation rules live in the
skill; its Godot reference is loaded only for Godot requests or relevant project
context. Asset-only work requires no Godot binary. The installer role only
inspects native configs and plans caller-authorized installation; upstream
auto-install and Claude Code installation are out of scope.

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
the three native OpenCode agents; the installer copies them separately. For each
selected harness, the installer runs `--check`, then `--output` into local staging.

Optional `model` maps to `openai/<model>` and `model_reasoning_effort` maps to
`options.reasoningEffort` for OpenCode. Omitted settings inherit runtime defaults.
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

| Role/policy | OpenCode / Codex behavior |
| --- | --- |
| `ralph` | Native OpenCode primary agent / no Codex counterpart |
| `ralph-reviewer` | Separate native source copied unchanged / no native source allowed |
| `sprite-artist` | Native source copied unchanged with `gpt_imagegen: ask` / no Codex source |

The 128 TOML sources produce **128 OpenCode Markdown files** or **128 unchanged
Codex source copies**, with no skips. The three separately copied native sources
bring the OpenCode installation to **131 agents**. Codex uses native `/goal` for
approved checklist execution with Ralph's full shared execution, memory, review,
prepared-branch, and per-story commit contract. Markdown versus JSON is the task
adapter difference; native Goal continuation/compaction does not acquire Ralph's
external hard iteration controller or completion sentinel. See [Codex goals](codex-goals.md).

## Validation and evaluation

```sh
python3.11 tests/agent_contract_test.py
python3.11 scripts/render-agents.py --harness opencode --check
python3.11 scripts/render-agents.py --harness codex --check
make validate-ai
```

Tests use repository-local temporary fixtures. They check native TOML parsing,
body preservation, byte-identical Codex copies, native OpenCode copies and policies,
model/effort mapping, unsupported-field rejection, dry runs, deterministic output,
and output safety. Ruby is used only in `tests/ralph_review_test.sh` for native
reviewer YAML validation, not by the renderer or installer. These checks do not
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
