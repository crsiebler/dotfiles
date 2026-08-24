# OpenCode Plugin Research

Research date: 2026-08-23

This assessment evaluates OpenCode plugins against the current setup:

- macOS and Zsh
- Dotfiles-managed global OpenCode configuration
- Ralph autonomous workflows
- Native task and background subagents
- More than 130 configured agents
- Global skills and project-local instructions
- Context7 and optional MCP integrations
- Mixed TypeScript and Python repositories
- Strict Git, privacy, secret-handling, and noninteractive-shell policies

OpenCode automatically installs configured npm plugins with Bun at startup.
Global and project hooks all execute sequentially. Treat every plugin as
arbitrary process-level code with potential access to the filesystem,
environment, credentials, conversation history, and configured tools. Pin exact
versions and manage accepted plugins through this repository.

Official plugin documentation:
<https://opencode.ai/docs/plugins>

## Best Fits

| Priority | Candidate | Recommendation | Rationale |
| ---: | --- | --- | --- |
| 1 | `opencode-shell-strategy` | Adopt as a reviewed instruction | Reinforces noninteractive shell requirements without executing plugin code |
| 2 | `@nick-vi/opencode-type-inject@1.5.2` | Enable per TypeScript project | Adds imported type definitions and lookup tools for substantial TypeScript projects |
| 3 | `@mohak34/opencode-notifier@0.2.8` | Upgrade the existing plugin | Improves focus handling, messages, and terminal support without adding a duplicate notifier |
| 4 | `@tarquinen/opencode-dcp@3.1.15` | Run a controlled pilot | May reduce token use in long Ralph sessions, but overlaps native compaction |
| 5 | `@plannotator/opencode@0.27.7` | Optional human-review pilot | Visual plan and diff annotation could complement Plan Mode |
| 6 | `opencode-vibeguard@0.1.0` | Sensitive-project pilot only | Locally redacts configured secrets before remote model calls, but remains immature |

## Recommended Baseline

1. Vendor a reviewed, commit-pinned copy of
   [`opencode-shell-strategy`](https://github.com/JRedeker/opencode-shell-strategy)
   into the dotfiles repository.
2. Upgrade the existing
   [`@mohak34/opencode-notifier`](https://github.com/mohak34/opencode-notifier)
   rather than adding another notification plugin.
3. Add
   [`@nick-vi/opencode-type-inject`](https://github.com/nick-vi/type-inject)
   only to substantial TypeScript projects.
4. Keep `opencode-gpt-imagegen` for Godot and visual work.
5. Review whether `opencode-dir` is actively used.

## Existing Plugin Review

### `opencode-dir@1.0.13`

Source: <https://github.com/adiled/opencode-dir>

The installed version is current and provides session-wide `/cd`, `/mv`, and
external-directory behavior. Its implementation has a broader risk profile than
the command names suggest:

- Directly edits OpenCode's SQLite database.
- Rewrites stored session messages and directory metadata.
- Writes `.git/opencode`.
- Changes session permissions and system prompts.
- Checks npm for updates at startup.
- Sends error telemetry to a hard-coded Sentry project.
- Advertises `/remove-dir`, but that command is incomplete in the published
  artifact.

Keep it only if session-level directory migration is actively useful. Otherwise,
removing it would reduce internal coupling, automatic update behavior, and
telemetry.

### `@mohak34/opencode-notifier@0.1.15`

Source: <https://github.com/mohak34/opencode-notifier>

The current release found during research was `0.2.8`. It adds richer event
handling, focus suppression, terminal integration, and optional custom commands.
Upgrade only after reviewing its changelog and keep custom outbound commands
disabled unless explicitly required.

### `opencode-gpt-imagegen@0.1.9`

Keep for Godot sprite work and visual asset generation. It provides a capability
that does not overlap the other recommended plugins.

## Strong Candidates

### `opencode-shell-strategy`

Source: <https://github.com/JRedeker/opencode-shell-strategy>

This is an instruction file rather than executable plugin code. It documents
noninteractive flags, pager and editor avoidance, SSH batch mode, `sudo -n`, and
safe first-contact behavior. It strongly matches the existing shell policy.

Vendor a reviewed file or reference a commit-pinned URL. Do not load a mutable
branch URL as a global instruction.

### `@nick-vi/opencode-type-inject@1.5.2`

Source: <https://github.com/nick-vi/type-inject>

The plugin injects relevant TypeScript, TSX, and optional Svelte type signatures
into file-read context and provides type lookup and checking tools.

Benefits:

- Reduces extra reads needed to understand imported APIs.
- Provides explicit type lookup for large TypeScript codebases.
- Runs locally without an external API key.

Tradeoffs:

- Adds tokens to relevant file reads.
- Partially overlaps native LSP and type-check commands.
- Provides no benefit in Python-only repositories.

Enable it in project configuration for TypeScript-heavy repositories rather
than globally.

## Conditional Pilots

### `@tarquinen/opencode-dcp@3.1.15`

Source: <https://github.com/Opencode-DCP/opencode-dynamic-context-pruning>

Dynamic Context Pruning removes stale or duplicate tool output before model
requests while preserving stored session history. It explicitly protects task,
skill, edit, and todo output.

Potential value:

- Lower token usage in long Ralph and review sessions.
- Less obsolete tool output in model context.

Risks:

- Overlaps native OpenCode compaction.
- Can remove details that later become relevant.
- Can reduce provider prompt-cache effectiveness.
- Enables automatic npm updates by default.

Pilot with a pinned version, automatic updates disabled, conservative
thresholds, and measurable token/context-quality goals.

### `@plannotator/opencode@0.27.7`

Source: <https://github.com/backnotprop/plannotator>

Plannotator provides local visual plan and diff annotation. It could complement
Ralph by serving strictly as a human review surface.

Risks:

- Its npm `postinstall` writes commands and a skill into the global OpenCode
  configuration.
- It starts a local browser server that can wait for an extended period.
- Hosted sharing and AI features can send data externally.

If adopted, pin the version, use `user-managed` mode, keep hosted features
disabled, and vendor generated assets into dotfiles instead of accepting
unmanaged global files.

### `opencode-vibeguard@0.1.0`

Source: <https://github.com/inkdust2021/opencode-vibeguard>

VibeGuard locally replaces configured secret and PII patterns before remote
model requests, then restores values before local tool execution.

Limitations:

- OpenCode's local database still contains real tool arguments and output.
- Detection is only as complete as its configured patterns.
- Literal secret values in configuration create another plaintext store.
- False positives may alter prompts or tool arguments.
- Version `0.1.0` has limited maturity.

Use only as defense in depth. Test project-locally on a non-sensitive repository
before considering work use.

### `opencode-websearch-cited@1.2.0`

Source: <https://github.com/ghoulr/opencode-websearch-cited>

This adds general web research with provider-native citations. It complements
Context7, which is specialized for library and framework documentation.

Use only with an approved Google, OpenAI, or OpenRouter search provider. Search
queries may expose repository names, errors, dependencies, vulnerabilities, or
business context and may incur separate provider charges. Disable it for
sensitive work repositories.

### Official Morph plugin

Package: `@morphllm/opencode-morph-plugin@2.0.16`

Source: <https://github.com/morphllm/opencode-morph-plugin>

The official plugin adds contextual editing, WarpGrep codebase and GitHub
search, and remote conversation compaction.

Potential value:

- Faster large-file and scattered edits.
- Natural-language exploratory search.
- Public GitHub code search.

Reasons not to make it a default:

- Sends complete target files and selected conversation context to Morph.
- Free retention can be up to 90 days; paid retention can be up to 30 days.
- Requires `MORPH_API_KEY` and usage-based billing.
- Overlaps deterministic `apply_patch`, `glob`, `grep`, and native compaction.

Use only if remote source processing and retention are acceptable. Prefer the
official plugin over `@f97/opencode-morph-fast-apply`, whose npm and GitHub
versions diverge materially.

### Other conditional tools

- `opencode-wakatime`: useful only if WakaTime telemetry is already desired.
- `opencode-zellij-namer`: useful only when Zellij is the active terminal
  multiplexer; prefer heuristic mode without Gemini.
- `@jfrog/opencode-jfrog-plugin`: useful only in approved JFrog-managed work
  repositories and should not be global.
- `opencode-scheduler`: restrict to read-only jobs because it creates persistent
  `launchd` services and unattended OpenCode sessions.
- `opencode-goal-plugin`: use only outside Ralph-managed workflows and with
  conservative continuation limits.
- `octto`: consider only if browser-based brainstorming provides clear value
  beyond existing PRD and planning workflows.
- `opencode-worktree`: standalone TUI rather than a plugin; keep worktree and
  branch deletion human-controlled.

## Do Not Add

### Competing orchestration harnesses

Reject the following because they duplicate or replace Ralph, native task
delegation, configured agents, MCPs, planning, and repository memory:

- `oh-my-opencode`
- `micode`
- `opencode-workspace`
- `opencode-conductor`
- `@openspoon/subtask2`
- `opencode-background-agents`

These systems add competing state models, autonomous continuation, agent
catalogs, Git behavior, permission changes, or background execution.

### Isolation and process plugins

- `opencode-daytona`: remote source execution and automatic Git synchronization
  conflict with local-first and controlled Git workflows.
- `opencode-devcontainers`: unnecessary unless a repository already treats a
  devcontainer as authoritative; it may copy ignored secrets.
- `opencode-pty`: conflicts with noninteractive-shell policy, overlaps native
  background tasks, and has concerning permission fallback behavior.

### Authentication plugins

- `opencode-openai-codex-auth`: redundant with existing authentication and adds
  third-party OAuth token handling.
- `opencode-gemini-auth`: consumer OAuth is deprecated and current documentation
  warns about Google policy risk.
- `opencode-antigravity-auth`: archived, stores account pools and refresh tokens,
  and carries explicit account-ban warnings.
- `opencode-google-antigravity-auth`: archived fork with the same policy and
  account risks.

Do not install competing provider-auth plugins together. Keep existing provider
authentication and Ollama as the simpler trust boundary.

### Memory, telemetry, and observability

- `opencode-supermemory`: sends conversations and project knowledge to an
  external service and overlaps `AGENTS.md`, `progress.txt`, and `memory.json`.
- `opencode-helicone-session`: useful only when model traffic already passes
  through Helicone; otherwise it adds no capability.
- `opencode-sentry-monitor`: records model input, output, and tool data by
  default and does not fit the strict privacy posture.
- Alternative notifier plugins: duplicate the installed maintained notifier.

### Search and content tools

- `opencode-firecrawl`: documented npm package was unavailable during research.
- `opencode-tavily`: documented npm package was unavailable during research.
- `opencode-md-table-formatter`: low-value cosmetic behavior.
- `opencode-skillful`: archived and superseded by native skill discovery.

## Clients And Managers

These projects are not OpenCode runtime plugins:

| Project | Type | Recommendation |
| --- | --- | --- |
| OpenChamber | Desktop, web, mobile, and VS Code client | Strongest optional GUI or remote client; review authentication before remote use |
| `opencode.nvim` | Neovim client plugin | Useful only if Neovim is the primary editor |
| `ocx` | Extension and profile manager | Overlaps the existing version-controlled dotfiles installation system |
| OpenWork | Cowork and business automation platform | Consider only for broader office or team automation |
| CodeNomad | Multi-instance desktop and web client | Conditional for sidecar and remote workflows |
| Portal/OpenPortal | Web client and launcher | Reject due to network-wide default binding, weaker documented authentication, and activity lag |

## Recommended Adoption Order

1. Vendor the shell strategy as a reviewed local instruction.
2. Upgrade the existing notifier after changelog review.
3. Enable type injection in one TypeScript-heavy repository and measure context
   overhead.
4. Decide whether `opencode-dir` provides enough value to justify its database
   mutation and telemetry.
5. Pilot DCP only if long-session token pressure is measurable.
6. Pilot Plannotator only if visual approval is an unmet need.
7. Pilot VibeGuard only as defense in depth for approved remote-model projects.

All plugin changes require quitting and restarting OpenCode.
