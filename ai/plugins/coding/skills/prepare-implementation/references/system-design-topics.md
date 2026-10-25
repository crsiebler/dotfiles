# Optional system design topics

These are investigation topics, not required dependencies, architecture,
acceptance targets or instructions to operate systems. Apply only relevant
sections; verify version-sensitive facts against project evidence and official
documentation. Historic product names are not recommendations or support claims.

### Service design principles

- Single responsibility focus
- Domain-driven boundaries
- Database per service
- API-first development
- Event-driven communication
- Stateless service design
- Configuration externalization
- Graceful degradation

### Resilience strategies

- Circuit breaker patterns
- Retry with backoff
- Timeout configuration
- Bulkhead isolation
- Rate limiting setup
- Fallback mechanisms
- Health check endpoints
- Chaos engineering tests

### Data management

- Database per service pattern
- Event sourcing approach
- CQRS implementation
- Distributed transactions
- Eventual consistency
- Data synchronization
- Schema evolution
- Backup strategies

### Service mesh configuration

- Traffic management rules
- Load balancing policies
- Canary deployment setup
- Blue/green strategies
- Mutual TLS enforcement
- Authorization policies
- Observability configuration
- Fault injection testing

### Container orchestration

- Kubernetes deployments
- Service definitions
- Ingress configuration
- Resource limits/requests
- Horizontal pod autoscaling
- ConfigMap management
- Secret handling
- Network policies

### Observability stack

- Distributed tracing setup
- Metrics aggregation
- Log centralization
- Performance monitoring
- Error tracking
- Business metrics
- SLI/SLO definition
- Dashboard creation

### Analysis framework

- Bounded context mapping
- Aggregate identification
- Event storming sessions
- Service dependency analysis
- Data flow mapping
- Transaction boundaries
- Team topology alignment
- Conway's law consideration

### Decomposition strategy

- Monolith analysis
- Seam identification
- Data decoupling
- Service extraction order
- Migration pathway
- Risk assessment
- Rollback planning
- Success metrics

### Implementation priorities

- Service scaffolding
- API contract definition
- Database setup
- Message broker integration
- Service mesh enrollment
- Monitoring instrumentation
- CI/CD pipeline
- Documentation creation

### Deployment strategies

- Progressive rollout patterns
- Feature flag integration
- A/B testing setup
- Canary analysis
- Automated rollback
- Multi-region deployment
- Edge computing setup
- CDN integration

### Security architecture

- Zero-trust networking
- mTLS everywhere
- API gateway security
- Token management
- Secret rotation
- Vulnerability scanning
- Compliance automation
- Audit logging

### Cost optimization

- Resource right-sizing
- Spot instance usage
- Serverless adoption
- Cache optimization
- Data transfer reduction
- Reserved capacity planning
- Idle resource elimination
- Multi-tenant strategies

### Team enablement

- Service ownership model
- On-call rotation setup
- Documentation standards
- Development guidelines
- Testing strategies
- Deployment procedures
- Incident response
- Knowledge sharing
