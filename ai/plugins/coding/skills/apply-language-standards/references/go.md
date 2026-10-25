# Go

Apply only to an actual project using this technology. Read the bundle's entry
and requirements first. Project versions, constraints and existing tools override
the topic inventory below; inherited version labels are examples, not minimum
requirements or claims of current support. Verify relevant APIs against official
documentation for the installed version before relying on them.

## Standards

Honor module/toolchain targets. Preserve wrapped error identity; own goroutine lifetime, context cancellation, channel closure and cleanup. Use project race/tests/benchmarks where applicable.

## Conditional topic inventory

These are investigation topics, not a setup plan, required dependencies, acceptance
criteria or instructions to execute changes. No universal latency, coverage,
deployment or architecture target applies. Load only relevant sections.

### Idiomatic Go patterns

- Interface composition over inheritance
- Accept interfaces, return structs
- Channels for orchestration, mutexes for state
- Error values over exceptions
- Explicit over implicit behavior
- Small, focused interfaces
- Dependency injection via interfaces
- Configuration through functional options

### Concurrency mastery

- Goroutine lifecycle management
- Channel patterns and pipelines
- Context for cancellation and deadlines
- Select statements for multiplexing
- Worker pools with bounded concurrency
- Fan-in/fan-out patterns
- Rate limiting and backpressure
- Synchronization with sync primitives

### Performance optimization

- CPU and memory profiling with pprof
- Benchmark-driven development
- Zero-allocation techniques
- Object pooling with sync.Pool
- Efficient string building
- Slice pre-allocation
- Compiler optimization understanding
- Cache-friendly data structures

### Testing methodology

- Table-driven test patterns
- Subtest organization
- Test fixtures and golden files
- Interface mocking strategies
- Integration test setup
- Benchmark comparisons
- Fuzzing for edge cases
- Race detector in CI

### Microservices patterns

- gRPC service implementation
- REST API with middleware
- Service discovery integration
- Circuit breaker patterns
- Distributed tracing setup
- Health checks and readiness
- Graceful shutdown handling
- Configuration management

### Cloud-native development

- Container-aware applications
- Kubernetes operator patterns
- Service mesh integration
- Cloud provider SDK usage
- Serverless function design
- Event-driven architectures
- Message queue integration
- Observability implementation

### Memory management

- Understanding escape analysis
- Stack vs heap allocation
- Garbage collection tuning
- Memory leak prevention
- Efficient buffer usage
- String interning techniques
- Slice capacity management
- Map pre-sizing strategies

### Build and tooling

- Module management best practices
- Build tags and constraints
- Cross-compilation setup
- CGO usage guidelines
- Go generate workflows
- Makefile conventions
- Docker multi-stage builds
- CI/CD optimization

### Development patterns

- Start with working code, then optimize
- Write benchmarks before optimizing
- Use go generate for repetitive code
- Implement graceful shutdown
- Add context to all blocking operations
- Create examples for complex APIs
- Follow project layout standards

### Advanced patterns

- Functional options for APIs
- Embedding for composition
- Type assertions with safety
- Reflection for frameworks
- Code generation patterns
- Plugin architecture design
- Custom error types
- Pipeline processing

### Database patterns

- Connection pool management
- Prepared statement caching
- Transaction handling
- Migration strategies
- SQL builder patterns
- NoSQL best practices
- Caching layer design
- Query optimization

### Observability setup

- Structured logging with slog
- Metrics with Prometheus
- Distributed tracing
- Error tracking integration
- Performance monitoring
- Custom instrumentation
- Dashboard creation
- Alert configuration

### Security practices

- Input validation
- SQL injection prevention
- Authentication middleware
- Authorization patterns
- Secret management
- TLS best practices
- Security headers
- Vulnerability scanning
