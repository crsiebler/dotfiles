# PowerShell security assessment

Apply only to an actual project using this technology. Read the bundle's entry
and requirements first. Project versions, constraints and existing tools override
the topic inventory below; inherited version labels are examples, not minimum
requirements or claims of current support. Verify relevant APIs against official
documentation for the installed version before relying on them.

## Standards

Assessment only: no tests or remediation. Assess JEA exposure, remoting, logging collection/sensitive output, signing trust and module provenance. Execution policy is not a security boundary.

## PowerShell control assessment

Use only controls relevant to the target and supplied evidence:

- Assess Just Enough Administration (JEA) role capabilities, exposed commands and
  parameters, endpoint configuration, and privilege boundaries.
- Review remoting transports, endpoint access, authentication configuration, and
  delegation risks without connecting to or reconfiguring live systems.
- Assess transcript, module, and script block logging coverage, retention/access,
  and sensitive-data exposure. Distinguish configured settings from evidence that
  logs are actually collected; never claim unobserved controls work.
- Review code signing, publisher trust, module provenance, and publishing policy.
  Execution policy is not a security boundary or a substitute for access controls.
- Inspect scripts, scheduled-task definitions, and module interfaces for excess
  privilege, unsafe dynamic invocation, credential handling, and secret leakage
  through output or errors. Apply baseline mappings only when required by scope.

Return prioritized findings with artifact locations, observed evidence, impact,
assumptions, and scoped recommendations. Describe proposed validation and rollback
considerations for the caller without executing them. Separate confirmed gaps
from missing evidence, and report inspection limits without fabricated results.
