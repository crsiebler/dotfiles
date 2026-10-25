# Electron

Apply only to an actual project using this technology. Read the bundle's entry
and requirements first. Project versions, constraints and existing tools override
the topic inventory below; inherited version labels are examples, not minimum
requirements or claims of current support. Verify relevant APIs against official
documentation for the installed version before relying on them.

## Standards

Preserve context isolation and least privilege across main/preload/renderer boundaries. Validate IPC, window lifetimes and native modules; never expose unrestricted shell/filesystem access.

## Conditional topic inventory

These are investigation topics, not a setup plan, required dependencies, acceptance
criteria or instructions to execute changes. No universal latency, coverage,
deployment or architecture target applies. Load only relevant sections.

### Security implementation

- Context isolation mandatory
- Remote module disabled
- WebSecurity enabled
- Preload script API exposure
- IPC channel validation
- Permission request handling
- Certificate pinning
- Secure data storage

### Process architecture

- Main process responsibilities
- Renderer process isolation
- IPC communication patterns
- Shared memory usage
- Worker thread utilization
- Process lifecycle management
- Memory leak prevention
- CPU usage optimization

### Native OS integration

- System menu bar setup
- Context menus
- File associations
- Protocol handlers
- System tray functionality
- Native notifications
- OS-specific shortcuts
- Dock/taskbar integration

### Window management

- Multi-window coordination
- State persistence
- Display management
- Full-screen handling
- Window positioning
- Focus management
- Modal dialogs
- Frameless windows

### Auto-update system

- Update server setup
- Differential updates
- Rollback mechanism
- Silent updates option
- Update notifications
- Version checking
- Download progress
- Signature verification

### Performance optimization

- Startup time under 3 seconds
- Memory usage below 200MB idle
- Smooth animations at 60 FPS
- Efficient IPC messaging
- Lazy loading strategies
- Resource cleanup
- Background throttling
- GPU acceleration

### Build configuration

- Multi-platform builds
- Native dependency handling
- Asset optimization
- Installer customization
- Icon generation
- Build caching
- CI/CD integration
- Platform-specific features

### Design considerations

- Process separation strategy
- IPC communication design
- Native module requirements
- Security boundary definition
- Update mechanism planning
- Data storage approach
- Performance targets
- Distribution method

### Technical decisions

- Electron version selection
- Framework integration
- Build tool configuration
- Native module usage
- Testing strategy
- Packaging approach
- Update server setup
- Monitoring solution

### Platform-specific handling

- Windows registry integration
- macOS entitlements
- Linux desktop files
- Platform keybindings
- Native dialog styling
- OS theme detection
- Accessibility APIs
- Platform conventions

### File system operations

- Sandboxed file access
- Permission prompts
- Recent files tracking
- File watchers
- Drag and drop
- Save dialog integration
- Directory selection
- Temporary file cleanup

### Debugging and diagnostics

- DevTools integration
- Remote debugging
- Crash reporting
- Performance profiling
- Memory analysis
- Network inspection
- Console logging
- Error tracking

### Native module management

- Module compilation
- Platform compatibility
- Version management
- Rebuild automation
- Binary distribution
- Fallback strategies
- Security validation
- Performance impact
