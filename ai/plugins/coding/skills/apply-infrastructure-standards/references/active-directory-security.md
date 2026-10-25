# Active Directory security assessment

Apply only to an actual project using this technology. Read the bundle's entry
and requirements first. Project versions, constraints and existing tools override
the topic inventory below; inherited version labels are examples, not minimum
requirements or claims of current support. Verify relevant APIs against official
documentation for the installed version before relying on them.

## Standards

Assessment only: no tests, exploits, endpoint changes or posts. Trace groups, delegation/ACLs, trusts and SPNs; assess LDAP/Kerberos/NTLM/SYSVOL/GPO from authorized evidence, without changing access controls.

## Conditional topic inventory

These are investigation topics, not a setup plan, required dependencies, acceptance
criteria or instructions to execute changes. No universal latency, coverage,
deployment or architecture target applies. Load only relevant sections.

### AD Security Posture Assessment

- Analyze privileged groups (Domain Admins, Enterprise Admins, Schema Admins)
- Review tiering models & delegation best practices
- Detect orphaned permissions, ACL drift, excessive rights
- Evaluate domain/forest functional levels and security implications

### Authentication & Protocol Hardening

- Assess LDAP signing, channel binding and Kerberos hardening from authorized evidence
- Identify NTLM fallback, weak encryption, legacy trust configurations
- Recommend conditional access transitions (Entra ID) where applicable

### GPO & Sysvol Security Review

- Examine security filtering and delegation
- Validate restricted groups, local admin enforcement
- Review SYSVOL permissions & replication security

### Attack Surface Reduction

- Evaluate exposure to common vectors (DCShadow, DCSync, Kerberoasting)
- Identify stale SPNs, weak service accounts, and unconstrained delegation
- Provide prioritization paths (quick wins → structural changes)
