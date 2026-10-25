# GraphQL

Apply only to an actual project using this technology. Read the bundle's entry
and requirements first. Project versions, constraints and existing tools override
the topic inventory below; inherited version labels are examples, not minimum
requirements or claims of current support. Verify relevant APIs against official
documentation for the installed version before relying on them.

## Standards

Preserve schema nullability, validation, resolver errors and compatibility. Assess authorization, request cost and N+1 behavior; own federation/subscription lifetimes where used.

## Conditional topic inventory

These are investigation topics, not a setup plan, required dependencies, acceptance
criteria or instructions to execute changes. No universal latency, coverage,
deployment or architecture target applies. Load only relevant sections.

### Schema design principles

- Domain-driven type modeling
- Nullable field best practices
- Interface and union usage
- Custom scalar implementation
- Directive application patterns
- Field deprecation strategy
- Schema documentation
- Example query provision

### Federation architecture

- Subgraph boundary definition
- Entity key selection
- Reference resolver design
- Schema composition rules
- Gateway configuration
- Query planning optimization
- Error boundary handling
- Service mesh integration

### Query optimization strategies

- DataLoader implementation
- Query depth limiting
- Complexity calculation
- Field-level caching
- Persisted queries setup
- Query batching patterns
- Resolver optimization
- Database query efficiency

### Subscription implementation

- WebSocket server setup
- Pub/sub architecture
- Event filtering logic
- Connection management
- Scaling strategies
- Message ordering
- Reconnection handling
- Authorization patterns

### Type system mastery

- Object type modeling
- Input type validation
- Enum usage patterns
- Interface inheritance
- Union type strategies
- Custom scalar types
- Directive definitions
- Type extensions

### Schema validation

- Naming convention enforcement
- Circular dependency detection
- Type usage analysis
- Field complexity scoring
- Documentation coverage
- Deprecation tracking
- Breaking change detection
- Performance impact assessment

### Client considerations

- Fragment colocation
- Query normalization
- Cache update strategies
- Optimistic UI patterns
- Error handling approach
- Offline support design
- Code generation setup
- Type safety enforcement

### Modeling activities

- Entity relationship mapping
- Type hierarchy design
- Field responsibility assignment
- Service boundary definition
- Shared type identification
- Query pattern analysis
- Mutation design patterns
- Subscription event modeling

### Design validation

- Type cohesion verification
- Query efficiency analysis
- Mutation safety review
- Subscription scalability check
- Federation readiness assessment
- Client usability testing
- Performance impact evaluation
- Security boundary validation

### Schema evolution strategy

- Backward compatibility rules
- Deprecation timeline
- Migration pathways
- Client notification
- Feature flagging
- Gradual rollout
- Rollback procedures
- Version documentation

### Monitoring and observability

- Query execution metrics
- Resolver performance tracking
- Error rate monitoring
- Schema usage analytics
- Client version tracking
- Deprecation usage alerts
- Complexity threshold alerts
- Federation health checks

### Security implementation

- Query depth limiting
- Resource exhaustion prevention
- Field-level authorization
- Token validation
- Rate limiting per operation
- Introspection control
- Query allowlisting
- Audit logging

### Testing methodology

- Schema unit tests
- Resolver integration tests
- Federation composition tests
- Subscription testing
- Performance benchmarks
- Security validation
- Client compatibility tests
- End-to-end scenarios
