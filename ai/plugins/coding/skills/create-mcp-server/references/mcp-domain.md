# MCP clients and servers

Apply only to an actual project using this technology. Read the bundle's entry
and requirements first. Project versions, constraints and existing tools override
the topic inventory below; inherited version labels are examples, not minimum
requirements or claims of current support. Verify relevant APIs against official
documentation for the installed version before relying on them.

## Standards

Use create-mcp-server's established procedure. Confirm protocol/SDK/client capabilities; preserve initialization, session/cancellation, pagination and result/error contracts. Annotations do not enforce authorization.

## Conditional topic inventory

These are investigation topics, not a setup plan, required dependencies, acceptance
criteria or instructions to execute changes. No universal latency, coverage,
deployment or architecture target applies. Load only relevant sections.

### Server development

- Resource implementation
- Tool function creation
- Prompt template design
- Transport configuration
- Authentication handling
- Rate limiting setup
- Logging integration
- Health check endpoints

### Client development

- Server discovery
- Connection management
- Tool invocation handling
- Resource retrieval
- Prompt processing
- Session state management
- Error recovery
- Performance monitoring

### Protocol implementation

- JSON-RPC 2.0 compliance
- Message format validation
- Request/response handling
- Notification processing
- Protocol-version-specific batching restrictions; do not assume support
- Error code standards
- Transport abstraction
- Protocol versioning

### SDK mastery

- TypeScript SDK usage
- Python SDK implementation
- Schema definition (Zod/Pydantic)
- Type safety enforcement
- Async pattern handling
- Event system integration
- Middleware development
- Plugin architecture

### Integration patterns

- Database connections
- API service wrappers
- File system access
- Authentication providers
- Message queue integration
- Webhook processors
- Data transformation
- Legacy system adapters

### Security implementation

- Input validation
- Output sanitization
- Authentication mechanisms
- Authorization controls
- Rate limiting
- Request filtering
- Audit logging
- Secure configuration

### Performance optimization

- Connection pooling
- Caching strategies
- Batch processing
- Lazy loading
- Resource cleanup
- Memory management
- Profiling integration
- Scalability planning

### Testing strategies

- Unit test coverage
- Integration testing
- Protocol compliance tests
- Security testing
- Performance benchmarks
- Load testing
- Regression testing
- End-to-end validation

### Deployment practices

- Container configuration
- Environment management
- Service discovery
- Health monitoring
- Log aggregation
- Metrics collection
- Alerting setup
- Rollback procedures

### Protocol design

- Resource schemas
- Tool definitions
- Prompt templates
- Error handling
- Authentication flows
- Rate limiting
- Monitoring hooks
- Documentation structure

### MCP patterns

- Start with simple resources
- Add tools incrementally
- Implement security early
- Test protocol compliance
- Optimize performance
- Plan for scale
- Monitor in production

### Server architecture

- Modular design
- Plugin system
- Configuration management
- Service discovery
- Health checks
- Metrics collection
- Log aggregation
- Error tracking

### Client integration

- SDK usage patterns
- Connection management
- Error handling
- Retry logic
- Caching strategies
- Performance monitoring
- Security controls
- User experience

### Protocol compliance

- JSON-RPC 2.0 adherence
- Message validation
- Error code standards
- Transport compatibility
- Schema enforcement
- Version management
- Backward compatibility
- Standards documentation

### Development tooling

- IDE configurations
- Debugging tools
- Testing frameworks
- Code generators
- Documentation tools
- Deployment scripts
- Monitoring dashboards
- Performance profilers

### Community engagement

- Open source contributions
- Documentation improvements
- Example implementations
- Best practice sharing
- Issue resolution
- Feature discussions
- Standards participation
- Knowledge transfer
