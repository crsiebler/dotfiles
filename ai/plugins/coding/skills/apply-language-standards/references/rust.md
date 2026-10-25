# Rust

Apply only to an actual project using this technology. Read the bundle's entry
and requirements first. Project versions, constraints and existing tools override
the topic inventory below; inherited version labels are examples, not minimum
requirements or claims of current support. Verify relevant APIs against official
documentation for the installed version before relying on them.

## Standards

Honor edition, minimum compiler and features. Preserve ownership/error contracts; document unsafe/FFI invariants. Check Send/Sync, executor blocking, cancellation and cleanup.

## Conditional topic inventory

These are investigation topics, not a setup plan, required dependencies, acceptance
criteria or instructions to execute changes. No universal latency, coverage,
deployment or architecture target applies. Load only relevant sections.

### Ownership and borrowing mastery

- Lifetime elision and explicit annotations
- Interior mutability patterns
- Smart pointer usage (Box, Rc, Arc)
- Cow for efficient cloning
- Pin API for self-referential types
- PhantomData for variance control
- Drop trait implementation
- Borrow checker optimization

### Error handling patterns

- Custom error types with thiserror
- Error propagation with ?
- Result combinators mastery
- Recovery strategies
- anyhow for applications
- Error context preservation
- Panic-free code design
- Fallible operations design

### Async programming

- tokio/async-std ecosystem
- Future trait understanding
- Pin and Unpin semantics
- Stream processing
- Select! macro usage
- Cancellation patterns
- Executor selection
- Async trait workarounds

### Performance optimization

- Zero-allocation APIs
- SIMD intrinsics usage
- Const evaluation maximization
- Link-time optimization
- Profile-guided optimization
- Memory layout control
- Cache-efficient algorithms
- Benchmark-driven development

### Memory management

- Stack vs heap allocation
- Custom allocators
- Arena allocation patterns
- Memory pooling strategies
- Leak detection and prevention
- Unsafe code guidelines
- FFI memory safety
- No-std development

### Testing methodology

- Unit tests with #[cfg(test)]
- Integration test organization
- Property-based testing with proptest
- Fuzzing with cargo-fuzz
- Benchmark with criterion
- Doctest examples
- Compile-fail tests
- Miri for undefined behavior

### Systems programming

- OS interface design
- File system operations
- Network protocol implementation
- Device driver patterns
- Embedded development
- Real-time constraints
- Cross-compilation setup
- Platform-specific code

### Macro development

- Declarative macro patterns
- Procedural macro creation
- Derive macro implementation
- Attribute macros
- Function-like macros
- Hygiene and spans
- Quote and syn usage
- Macro debugging techniques

### Build and tooling

- Workspace organization
- Feature flag strategies
- build.rs scripts
- Cross-platform builds
- CI/CD with cargo
- Documentation generation
- Dependency auditing
- Release optimization

### Safety evaluation

- Identify unsafe blocks
- Review FFI boundaries
- Check thread safety
- Analyze panic points
- Verify drop correctness
- Assess allocation patterns
- Review error handling
- Document invariants

### Development patterns

- Start with safe abstractions
- Benchmark before optimizing
- Use cargo expand for macros
- Test with miri regularly
- Profile memory usage
- Check assembly output
- Verify optimization assumptions
- Create comprehensive examples

### Advanced patterns

- Type state machines
- Const generic matrices
- GATs implementation
- Async trait patterns
- Lock-free data structures
- Custom DSTs
- Phantom types
- Compile-time guarantees

### Embedded patterns

- no_std compliance
- Heap allocation avoidance
- Const evaluation usage
- Interrupt handlers
- DMA safety
- Real-time guarantees
- Power optimization
- Hardware abstraction

### WebAssembly

- wasm-bindgen usage
- Size optimization
- JS interop patterns
- Memory management
- Performance tuning
- Browser compatibility
- WASI compliance
- Module design

### Concurrency patterns

- Lock-free algorithms
- Actor model with channels
- Shared state patterns
- Work stealing
- Rayon parallelism
- Crossbeam utilities
- Atomic operations
- Thread pool design
