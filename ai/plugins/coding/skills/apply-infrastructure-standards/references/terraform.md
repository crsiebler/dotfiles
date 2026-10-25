# Terraform

Apply only to an actual project using this technology. Read the bundle's entry
and requirements first. Project versions, constraints and existing tools override
the topic inventory below; inherited version labels are examples, not minimum
requirements or claims of current support. Verify relevant APIs against official
documentation for the installed version before relying on them.

## Standards

Confirm providers, workspace, backend and state ownership. Inspect replacement/destruction and drift in a scoped plan. Preserve locks; apply/import/state/backend changes require actual authority.

## Conditional topic inventory

These are investigation topics, not a setup plan, required dependencies, acceptance
criteria or instructions to execute changes. No universal latency, coverage,
deployment or architecture target applies. Load only relevant sections.

### Module development

- Composable architecture
- Input validation
- Output contracts
- Version constraints
- Provider configuration
- Resource tagging
- Naming conventions
- Documentation standards

### State management

- Remote backend setup
- State locking mechanisms
- Workspace strategies
- State file encryption
- Migration procedures
- Import workflows
- State manipulation
- Disaster recovery

### Multi-environment workflows

- Environment isolation
- Variable management
- Secret handling
- Configuration DRY
- Promotion pipelines
- Approval processes
- Rollback procedures
- Drift detection

### Provider expertise

- AWS provider mastery
- Azure provider proficiency
- GCP provider knowledge
- Kubernetes provider
- Helm provider
- Vault provider
- Custom providers
- Provider versioning

### Security compliance

- Policy as code
- Compliance scanning
- Secret management
- IAM least privilege
- Network security
- Encryption standards
- Audit logging
- Security benchmarks

### Cost management

- Cost estimation
- Budget alerts
- Resource tagging
- Usage tracking
- Optimization recommendations
- Waste identification
- Chargeback support
- FinOps integration

### Testing strategies

- Unit testing
- Integration testing
- Compliance testing
- Security testing
- Cost testing
- Performance testing
- Disaster recovery testing
- End-to-end validation

### CI/CD integration

- Pipeline automation
- Plan/apply workflows
- Approval gates
- Automated testing
- Security scanning
- Cost checking
- Documentation generation
- Version management

### Enterprise patterns

- Mono-repo vs multi-repo
- Module registry
- Governance framework
- RBAC implementation
- Audit requirements
- Change management
- Knowledge sharing
- Team collaboration

### Advanced features

- Dynamic blocks
- Complex conditionals
- Meta-arguments
- Provider aliases
- Module composition
- Data source patterns
- Local provisioners
- Custom functions

### Terraform patterns

- Keep modules small
- Use semantic versioning
- Implement validation
- Follow naming conventions
- Tag all resources
- Test continuously
- Refactor regularly

### Module patterns

- Root module design
- Child module structure
- Data-only modules
- Composite modules
- Facade patterns
- Factory patterns
- Registry modules
- Version strategies

### State strategies

- Backend configuration
- State file structure
- Locking mechanisms
- Partial backends
- State migration
- Cross-region replication
- Backup procedures
- Recovery planning

### Variable patterns

- Variable validation
- Type constraints
- Default values
- Variable files
- Environment variables
- Sensitive variables
- Complex variables
- Locals usage

### Resource management

- Resource targeting
- Resource dependencies
- Count vs for_each
- Dynamic blocks
- Provisioner usage
- Null resources
- Time-based resources
- External data sources
