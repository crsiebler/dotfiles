# PowerShell

Apply only to an actual project using this technology. Read the bundle's entry
and requirements first. Project versions, constraints and existing tools override
the topic inventory below; inherited version labels are examples, not minimum
requirements or claims of current support. Verify relevant APIs against official
documentation for the installed version before relying on them.

## Standards

Honor declared versions/platforms, public command and pipeline contracts. Installed binaries do not select targets. Preserve ShouldProcess/WhatIf, exports and error behavior; report missing target validation.

## Target selection

Honor declared versions and platforms. Check module and platform compatibility
separately for Windows PowerShell 5.1 and PowerShell 7.
Prefer modern PowerShell 7 for unconstrained new work after inspecting project
evidence. Do not infer requirements from installed binaries or Windows alone.
Add backward compatibility, capability checks, or shims only for concrete required
consumers; do not impose them on modern-only work.

Use syntax and APIs supported by the declared minimum version. For 5.1, avoid
7-only constructs such as ternary and pipeline-chain operators. Encoding defaults
differ by command and runtime; choose explicit encodings when interoperating,
including BOM needs for non-ASCII scripts read by Windows PowerShell. Verify module
edition and assembly compatibility rather than assuming legacy modules load in 7.
For remoting, check endpoint runtime, transport/platform support, and serialized
object limitations; do not assume remote objects retain local methods.

## Implementation and validation

- Use advanced functions with CmdletBinding, typed and validated parameters, and
  intentional pipeline binding. Return structured objects on the success stream;
  keep formatting at presentation boundaries and diagnostics on separate streams.
- Define actionable errors and deliberate terminating/nonterminating behavior;
  use try/catch with appropriate error handling rather than swallowing failures.
- For applicable state changes, implement SupportsShouldProcess and guard the
  actual operation with ShouldProcess so WhatIf/Confirm work. Validate scope and
  context, avoid secret exposure, and obtain approval for consequential operations
  not already authorized. Routine safe scripting needs no security handoff.
- Preserve shipped public APIs: exported names, parameter sets, output types, and
  error contracts. Keep helpers private and exports explicit; align manifests,
  dependency/runtime requirements, documentation, and module versioning with the
  supported contract. Extract helpers only when useful, not to impose a layout.
- Keep profiles thin and host-aware; avoid heavy startup work and unexpected side
  effects. Reuse modules rather than duplicating automation in profiles.
- Use project-configured Pester, analysis, manifest/import checks, and relevant
  tests on declared targets when available and authorized. Validate pipeline/error
  behavior, exports, and WhatIf paths without performing unapproved live changes.
  Report actual checks and unavailable runtime coverage, not assumed compatibility.
