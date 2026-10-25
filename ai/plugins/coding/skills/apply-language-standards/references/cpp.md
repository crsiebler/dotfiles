# C++

Apply only to an actual project using this technology. Read the bundle's entry
and requirements first. Project versions, constraints and existing tools override
the topic inventory below; inherited version labels are examples, not minimum
requirements or claims of current support. Verify relevant APIs against official
documentation for the installed version before relying on them.

## Standards

Honor compiler/standard targets, RAII, ownership, ABI and exception guarantees. Check iterator invalidation and data races; justify unsafe/low-level optimization with evidence.

## Conditional topic inventory

These are investigation topics, not a setup plan, required dependencies, acceptance
criteria or instructions to execute changes. No universal latency, coverage,
deployment or architecture target applies. Load only relevant sections.

### Modern C++ mastery

- Concepts and constraints usage
- Ranges and views library
- Coroutines implementation
- Modules system adoption
- Three-way comparison operator
- Designated initializers
- Template parameter deduction
- Structured bindings everywhere

### Template metaprogramming

- Variadic templates mastery
- SFINAE and if constexpr
- Template template parameters
- Expression templates
- CRTP pattern implementation
- Type traits manipulation
- Compile-time computation
- Concept-based overloading

### Performance optimization

- Cache-friendly algorithms
- SIMD intrinsics usage
- Branch prediction hints
- Loop optimization techniques
- Inline assembly when needed
- Compiler optimization flags
- Profile-guided optimization
- Link-time optimization

### Concurrency patterns

- std::thread and std::async
- Lock-free data structures
- Atomic operations mastery
- Memory ordering understanding
- Condition variables usage
- Parallel STL algorithms
- Thread pool implementation
- Coroutine-based concurrency

### Systems programming

- OS API abstraction
- Device driver interfaces
- Embedded systems patterns
- Real-time constraints
- Interrupt handling
- DMA programming
- Kernel module development
- Bare metal programming

### STL and algorithms

- Container selection criteria
- Algorithm complexity analysis
- Custom iterator design
- Allocator awareness
- Range-based algorithms
- Execution policies
- View composition
- Projection usage

### Error handling patterns

- Exception safety guarantees
- noexcept specifications
- Error code design
- std::expected usage
- RAII for cleanup
- Contract programming
- Assertion strategies
- Compile-time checks

### Build system mastery

- CMake modern practices
- Compiler flag optimization
- Cross-compilation setup
- Package management with Conan
- Static/dynamic linking
- Build time optimization
- Continuous integration
- Sanitizer integration

### Advanced techniques

- Fold expressions
- User-defined literals
- Reflection experiments
- Metaclasses proposals
- Contracts usage
- Modules best practices
- Coroutine generators
- Ranges composition

### Low-level optimization

- Assembly inspection
- CPU pipeline optimization
- Vectorization hints
- Prefetch instructions
- Cache line padding
- False sharing prevention
- NUMA awareness
- Huge page usage

### Embedded patterns

- Interrupt safety
- Stack size optimization
- Static allocation only
- Compile-time configuration
- Power efficiency
- Real-time guarantees
- Watchdog integration
- Bootloader interface

### Graphics programming

- OpenGL/Vulkan wrapping
- Shader compilation
- GPU memory management
- Render loop optimization
- Asset pipeline
- Physics integration
- Scene graph design
- Performance profiling

### Network programming

- Zero-copy techniques
- Protocol implementation
- Async I/O patterns
- Buffer management
- Endianness handling
- Packet processing
- Socket abstraction
- Performance tuning
