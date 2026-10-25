# Windows infrastructure

Apply only to an actual project using this technology. Read the bundle's entry
and requirements first. Project versions, constraints and existing tools override
the topic inventory below; inherited version labels are examples, not minimum
requirements or claims of current support. Verify relevant APIs against official
documentation for the installed version before relying on them.

## Standards

Identify server/domain/OU/zone/scope and module targets. Inspect AD, DNS/DHCP, GPO and services as relevant. Preview affected objects and rollback; WhatIf is not authorization.

## Conditional topic inventory

These are investigation topics, not a setup plan, required dependencies, acceptance
criteria or instructions to execute changes. No universal latency, coverage,
deployment or architecture target applies. Load only relevant sections.

### Active Directory

- Automate user, group, computer, and OU operations
- Validate delegation, ACLs, and identity lifecycles
- Work with trusts, replication, domain/forest configurations

### DNS & DHCP

- Manage DNS zones, records, scavenging, auditing
- Configure DHCP scopes, reservations, policies
- Export/import configs for backup & rollback

### GPO & Server Administration

- Manage GPO links, security filtering, and WMI filters
- Generate GPO backups and comparison reports
- Work with server roles, certificates, WinRM, SMB, IIS

### Safe Change Engineering

- Pre-change verification flows
- Post-change validation and rollback paths
- Impact assessments + maintenance window planning
