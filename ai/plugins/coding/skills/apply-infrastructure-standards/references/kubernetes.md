# Kubernetes

Apply only to an actual project using this technology. Read the bundle's entry
and requirements first. Project versions, constraints and existing tools override
the topic inventory below; inherited version labels are examples, not minimum
requirements or claims of current support. Verify relevant APIs against official
documentation for the installed version before relying on them.

## Standards

Identify cluster/context, namespace and API versions. Check workload ownership, probes, rollout/disruption, resources, storage and network/RBAC boundaries; manifests do not prove live health.

## Conditional topic inventory

These are investigation topics, not a setup plan, required dependencies, acceptance
criteria or instructions to execute changes. No universal latency, coverage,
deployment or architecture target applies. Load only relevant sections.

### Cluster architecture

- Control plane design
- Multi-master setup
- etcd configuration
- Network topology
- Storage architecture
- Node pools
- Availability zones
- Upgrade strategies

### Workload orchestration

- Deployment strategies
- StatefulSet management
- Job orchestration
- CronJob scheduling
- DaemonSet configuration
- Pod design patterns
- Init containers
- Sidecar patterns

### Resource management

- Resource quotas
- Limit ranges
- Pod disruption budgets
- Horizontal pod autoscaling
- Vertical pod autoscaling
- Cluster autoscaling
- Node affinity
- Pod priority

### Networking

- CNI selection
- Service types
- Ingress controllers
- Network policies
- Service mesh integration
- Load balancing
- DNS configuration
- Multi-cluster networking

### Storage orchestration

- Storage classes
- Persistent volumes
- Dynamic provisioning
- Volume snapshots
- CSI drivers
- Backup strategies
- Data migration
- Performance tuning

### Security hardening

- Pod security standards
- RBAC configuration
- Service accounts
- Security contexts
- Network policies
- Admission controllers
- OPA policies
- Image scanning

### Observability

- Metrics collection
- Log aggregation
- Distributed tracing
- Event monitoring
- Cluster monitoring
- Application monitoring
- Cost tracking
- Capacity planning

### Multi-tenancy

- Namespace isolation
- Resource segregation
- Network segmentation
- RBAC per tenant
- Resource quotas
- Policy enforcement
- Cost allocation
- Audit logging

### Service mesh

- Istio implementation
- Linkerd deployment
- Traffic management
- Security policies
- Observability
- Circuit breaking
- Retry policies
- A/B testing

### GitOps workflows

- ArgoCD setup
- Flux configuration
- Helm charts
- Kustomize overlays
- Environment promotion
- Rollback procedures
- Secret management
- Multi-cluster sync

### Kubernetes patterns

- Design for failure
- Implement least privilege
- Use declarative configs
- Enable auto-scaling
- Monitor everything
- Automate operations
- Version control configs
- Test disaster recovery

### Production patterns

- Blue-green deployments
- Canary releases
- Rolling updates
- Circuit breakers
- Health checks
- Readiness probes
- Graceful shutdown
- Resource limits

### Troubleshooting

- Pod failures
- Network issues
- Storage problems
- Performance bottlenecks
- Security violations
- Resource constraints
- Cluster upgrades
- Application errors

### Advanced features

- Custom resources
- Operator development
- Admission webhooks
- Custom schedulers
- Device plugins
- Runtime classes
- Pod security policies
- Cluster federation

### Cost optimization

- Resource right-sizing
- Spot instance usage
- Cluster autoscaling
- Namespace quotas
- Idle resource cleanup
- Storage optimization
- Network efficiency
- Monitoring overhead
