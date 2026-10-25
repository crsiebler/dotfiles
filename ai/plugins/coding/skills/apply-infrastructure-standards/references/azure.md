# Azure

Apply only to an actual project using this technology. Read the bundle's entry
and requirements first. Project versions, constraints and existing tools override
the topic inventory below; inherited version labels are examples, not minimum
requirements or claims of current support. Verify relevant APIs against official
documentation for the installed version before relying on them.

## Standards

Identify subscription, tenant, region and affected resources. Preserve policy/network/identity boundaries; use scoped previews and document rollback limits, never implicit provisioning.

## Conditional topic inventory

These are investigation topics, not a setup plan, required dependencies, acceptance
criteria or instructions to execute changes. No universal latency, coverage,
deployment or architecture target applies. Load only relevant sections.

### Azure Resource Architecture

- Resource group strategy, tagging, naming standards
- VM, storage, networking, NSG, firewall configuration
- Governance via Azure Policies and management groups

### Hybrid Identity + Entra ID Integration

- Sync architecture (AAD Connect / Cloud Sync)
- Conditional Access strategy
- Secure service principal and managed identity usage

### Automation & IaC

- PowerShell Az module automation
- ARM/Bicep resource modeling
- Infrastructure pipelines (GitHub Actions, Azure DevOps)
