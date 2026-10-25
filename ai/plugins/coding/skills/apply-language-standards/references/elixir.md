# Elixir and OTP

Apply only to an actual project using this technology. Read the bundle's entry
and requirements first. Project versions, constraints and existing tools override
the topic inventory below; inherited version labels are examples, not minimum
requirements or claims of current support. Verify relevant APIs against official
documentation for the installed version before relying on them.

## Standards

Confirm runtime/OTP versions. Model process ownership, supervision, restart effects, mailbox bounds and message ordering. Test distributed partial failure before adding macros or processes.

## Conditional topic inventory

These are investigation topics, not a setup plan, required dependencies, acceptance
criteria or instructions to execute changes. No universal latency, coverage,
deployment or architecture target applies. Load only relevant sections.

### Functional programming mastery

- Immutable data transformations
- Pipeline operator for data flow
- Pattern matching in all contexts
- Guard clauses for constraints
- Higher-order functions with Enum/Stream
- Recursion with tail-call optimization
- Protocols for polymorphism
- Behaviours for contracts

### Concurrency patterns

- Lightweight process architecture
- Message passing design
- Process linking and monitoring
- Timeout handling strategies
- Backpressure with GenStage
- Flow for parallel processing
- Broadway for data pipelines
- Process pooling with Poolboy

### Error handling philosophy

- "Let it crash" with supervision
- Tagged tuples {:ok, value} | {:error, reason}
- with statements for happy path
- Rescue only at boundaries
- Graceful degradation patterns
- Circuit breaker implementation
- Retry strategies with exponential backoff
- Error logging with Logger

### Phoenix framework

- Context-based architecture
- LiveView real-time UIs
- Channels for WebSockets
- Plugs and middleware
- Router design patterns
- Controller best practices
- Component architecture
- PubSub for messaging

### LiveView expertise

- Server-rendered real-time UIs
- LiveComponent composition
- Hooks for JavaScript interop
- Streams for large collections
- Uploads handling
- Presence tracking
- Form handling patterns
- Optimistic UI updates

### Ecto mastery

- Schema design and associations
- Changesets for validation
- Query composition
- Multi-tenancy patterns
- Migrations best practices
- Repo configuration
- Connection pooling
- Transaction management

### Performance optimization

- BEAM scheduler understanding
- Process hibernation
- Binary optimization
- ETS for hot data
- Lazy evaluation with Stream
- Profiling with :observer
- Memory analysis
- Benchmark with Benchee

### Testing methodology

- ExUnit test organization
- Doctests for examples
- Property-based testing with StreamData
- Mox for behavior mocking
- Sandbox for database tests
- Integration test patterns
- LiveView testing
- Wallaby for browser tests

### Macro and metaprogramming

- Quote and unquote mechanics
- AST manipulation
- Compile-time code generation
- use, import, alias patterns
- Custom DSL creation
- Macro hygiene
- Module attributes
- Code reflection

### Build and tooling

- Mix task creation
- Umbrella project organization
- Release configuration with Mix releases
- Environment configuration
- Dependency management with Hex
- Documentation with ExDoc
- Static analysis with Dialyzer
- Code quality with Credo

### Implementation approach

- Design supervision tree first
- Implement GenServer behaviors
- Use contexts for boundaries
- Apply pattern matching extensively
- Create pipelines for transforms
- Handle errors at proper level
- Write specs for Dialyzer
- Document with examples

### Development patterns

- Start with simple processes
- Add supervision incrementally
- Use LiveView for real-time
- Implement with/else for flow
- Leverage protocols for extension
- Create custom Mix tasks
- Use releases for deployment
- Monitor with Telemetry

### Distributed systems

- Node clustering with libcluster
- Distributed Registry patterns
- Horde for distributed supervisors
- Phoenix.PubSub across nodes
- Consistent hashing strategies
- Leader election patterns
- Network partition handling
- State synchronization

### Deployment patterns

- Mix releases configuration
- Distillery migration
- Docker containerization
- Kubernetes deployment
- Hot code upgrades
- Rolling deployments
- Health check endpoints
- Graceful shutdown

### Observability setup

- Telemetry events and metrics
- Logger configuration
- :observer for debugging
- OpenTelemetry integration
- Custom metrics with Prometheus
- LiveDashboard integration
- Error tracking setup
- Performance monitoring

### Security practices

- Input validation with changesets
- CSRF protection in Phoenix
- Authentication with Guardian/Pow
- Authorization patterns
- Secret management
- SSL/TLS configuration
- Rate limiting implementation
- Security headers
