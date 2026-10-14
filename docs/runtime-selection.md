# Runtime and model selection

The central portable selection policy is the **Runtime and model selection**
section in [ai/AGENTS.md](../ai/AGENTS.md). Installation copies that policy unchanged
to both user-level harnesses. Roles supply expertise, permitted tools and outputs;
runtime profiles and explicit launch arguments supply model and effort choices.
This is a source foundation, not a scheduler or automatic task classifier.

## Selection surfaces

| Surface | Source behavior |
| --- | --- |
| Codex session | Base config explicitly selects `gpt-6.1-sol`; opt-in Astra profile selects `gpt-6-astra` with high effort |
| Codex delegated roles | All 128 sources omit model/provider/effort; global subagent model/effort defaults are absent |
| OpenCode session | Base config selects `openai/gpt-6-astra`; Astra/Sol overlays select only the top-level session model |
| OpenCode delegated roles | Generated roles and native Ralph reviewer omit model/effort; general/build/subagents config pins are absent |
| OpenCode utility calls | `small_model` remains the explicit Luna utility setting; it is not a specialist role selector |
| Ralph launch | Omitted model/effort uses OpenCode defaults; explicit `--model` and `--effort` select the worker attempt and are recorded in context |

The renderer still supports explicit model/effort fields for callers' custom
collections. Source omission preserves native inheritance rather than translating
to a fictional `auto` selector. Codex's documented inheritance differs when an
explicit model is selected without effort: that model's default effort can apply.
See [official subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents).
Verify effective settings in the installed runtime before claiming inheritance
or an override worked; parsed source and captured launch arguments are narrower
evidence. Model availability, provider variants and quality remain runtime checks.

Choose native Codex **or** Ralph/OpenCode for one attempt. Existing risk-based
staged review remains authoritative; changing models cannot reset a blocked
candidate, renew review budgets, or substitute a generic reviewer. A valid explicit
plan launch can cover eligible in-scope implementation, checks, delegation and
local commits across the sequence. Labels, profiles and plan files confer no grant.

## Rollout boundary

Galena is the source checkout and local verification host. Native Codex goals use
concurrent dependency-ready task workers; Ralph remains serial. Paperclip/NCase
multi-session management is a separate future project. Controller/application
integrations belong in Avengers; external tracker selection and Apple work are
excluded. No scheduler, credential change or deployment is supplied here.

A native coding plugin refresh installs the revised skills without applying
personal policy, role files or runtime/model configuration. Coordinated activation
of those other sources requires its own scope and preservation of installed local
settings. Restart the selected harness and use a fresh disposable task to verify
skill discovery, supported explicit selection, role restrictions, task worktrees,
compact planning and one authorized local sequence through the review contract.
Keep stopped goals stopped. Live calls, spending, pushes, PRs, merges and deployment
need their own approved execution scope; source checks do not authorize them.

Offline evidence: renderer/role contracts, runtime-selection config tests, actual
Ralph executable startup and captured fake-worker arguments. These tests do not
establish unattended operation, model quality or installed discovery.
