# Mobile Developer topics

Use only topics relevant to the requested task and actual stack. These are
conditional review/design prompts, not mandatory architecture or authority to
operate services. Verify version-sensitive details against project evidence.

### Platform optimization standards
- Cold start time under 1.5 seconds
- Memory usage below 120MB baseline
- Battery consumption: use an agreed, measured project target
- 120 FPS for ProMotion displays (60 FPS minimum)
- Efficient image caching with modern formats (WebP, AVIF)
- Background task optimization
- Network request batching and HTTP/3 support

### Native module integration
- Camera and photo library access (with privacy manifests)
- GPS and location services
- Biometric authentication (Face ID, Touch ID, Fingerprint)
- Device sensors (accelerometer, gyroscope, proximity)
- Bluetooth Low Energy (BLE) connectivity
- Local storage encryption (Keychain, EncryptedSharedPreferences)
- Background services and WorkManager
- Platform-specific APIs (HealthKit, Google Fit, etc.)

### Offline synchronization
- Local database implementation (SQLite, Realm, WatermelonDB)
- Queue management for actions
- Conflict resolution strategies (last-write-wins, vector clocks)
- Delta sync mechanisms
- Retry logic with exponential backoff and jitter
- Data compression techniques (gzip, brotli)
- Cache invalidation policies (TTL, LRU)
- Progressive data loading and pagination

### UI/UX platform patterns
- iOS Human Interface Guidelines (iOS 17+)
- Material Design 3 for Android 14+
- Platform-specific navigation (SwiftUI-like, Material 3)
- Native gesture handling and haptic feedback
- Adaptive layouts and responsive design
- Dynamic type and scaling support
- Dark mode and system theme support
- Accessibility features (VoiceOver, TalkBack, Dynamic Type)

### Testing methodology
- Unit tests for business logic (Jest, Flutter test)
- Integration tests for native modules
- E2E tests with Detox/Maestro/Patrol
- Platform-specific test suites
- Performance profiling with Flipper/DevTools
- Memory leak detection with LeakCanary/Instruments
- Battery usage analysis
- Crash testing scenarios and chaos engineering

### Build configuration
- iOS code signing with automatic provisioning
- Android keystore management with Play App Signing
- Build flavors and schemes (dev, staging, production)
- Environment-specific configs (.env support)
- ProGuard/R8 optimization with proper rules
- App thinning strategies (asset catalogs, on-demand resources)
- Bundle splitting and dynamic feature modules
- Asset optimization (image compression, vector graphics)

### Deployment pipeline
- Automated build processes (Fastlane, Codemagic, Bitrise)
- Beta testing distribution (TestFlight, Firebase App Distribution)
- App store submission with automation
- Crash reporting setup (Sentry, Firebase Crashlytics)
- Analytics integration (Amplitude, Mixpanel, Firebase Analytics)
- A/B testing framework (Firebase Remote Config, Optimizely)
- Feature flag system (LaunchDarkly, Firebase)
- Rollback procedures and staged rollouts

### Modern architecture patterns
- Clean Architecture separation
- Repository pattern for data access
- Dependency injection (GetIt, Provider)
- MVVM or MVI patterns
- Reactive programming (RxDart, React hooks)
- Code generation (build_runner, CodeGen)

### Modern performance techniques
- Hermes engine for React Native
- RAM bundles and inline requires
- Image prefetching and lazy loading
- List virtualization (FlashList, ListView.builder)
- Memoization and React.memo usage
- Web workers for heavy computations
- Metal/Vulkan graphics optimization

### Performance monitoring
- Frame rate tracking (120 FPS support)
- Memory usage alerts and leak detection
- Crash reporting with symbolication
- ANR detection and reporting
- Network performance and API monitoring
- Battery drain analysis
- Startup time metrics (cold, warm, hot)
- User interaction tracking and Core Web Vitals

### Platform-specific features
- iOS widgets (WidgetKit) and Live Activities
- Android app shortcuts and adaptive icons
- Platform notifications with rich media
- Share extensions and action extensions
- Siri Shortcuts/Google Assistant Actions
- Apple Watch companion app (watchOS 10+)
- Wear OS support
- CarPlay/Android Auto integration
- Platform-specific security (App Attest, SafetyNet)

### Modern development tools
- React Native New Architecture (Fabric, TurboModules)
- Flutter Impeller rendering engine
- Hot reload and fast refresh
- Flipper/DevTools for debugging
- Metro bundler optimization
- Gradle 8+ with configuration cache
- Swift Package Manager integration
- Kotlin Multiplatform Mobile (KMM) for shared code

### Code signing and certificates
- iOS provisioning profiles with automatic signing
- Apple Developer Program enrollment
- Android signing config with Play App Signing
- Certificate management and rotation
- Entitlements configuration (push, HealthKit, etc.)
- App ID registration and capabilities
- Bundle identifier setup
- Keychain and secrets management
- CI/CD signing automation (Fastlane match)

### App store preparation
- Screenshot generation across devices (including tablets)
- App Store Optimization (ASO)
- Keyword research and localization
- Privacy policy and data handling disclosures
- Privacy nutrition labels
- Age rating determination
- Export compliance documentation
- Beta testing setup (TestFlight, Firebase)
- Release notes and changelog
- App Store Connect API integration

### Security best practices
- Certificate pinning for API calls
- Secure storage (Keychain, EncryptedSharedPreferences)
- Biometric authentication implementation
- Jailbreak/root detection
- Code obfuscation (ProGuard/R8)
- API key protection
- Deep link validation
- Privacy manifest files (iOS)
- Data encryption at rest and in transit
- OWASP MASVS compliance
