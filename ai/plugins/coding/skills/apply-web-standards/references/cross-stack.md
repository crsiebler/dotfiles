# Fullstack Developer topics

Use only topics relevant to the requested task and actual stack. These are
conditional review/design prompts, not mandatory architecture or authority to
operate services. Verify version-sensitive details against project evidence.

### Data flow architecture
- Database design with proper relationships
- API endpoints following RESTful/GraphQL patterns
- Frontend state management synchronized with backend
- Optimistic updates with proper rollback
- Caching strategy across all layers
- Real-time synchronization when needed
- Consistent validation rules throughout
- Type safety from database to UI

### Cross-stack authentication
- Session management with secure cookies
- JWT implementation with refresh tokens
- SSO integration across applications
- Role-based access control (RBAC)
- Frontend route protection
- API endpoint security
- Database row-level security
- Authentication state synchronization

### Real-time implementation
- WebSocket server configuration
- Frontend WebSocket client setup
- Event-driven architecture design
- Message queue integration
- Presence system implementation
- Conflict resolution strategies
- Reconnection handling
- Scalable pub/sub patterns

### Testing strategy
- Unit tests for business logic (backend & frontend)
- Integration tests for API endpoints
- Component tests for UI elements
- End-to-end tests for complete features
- Performance tests across stack
- Load testing for scalability
- Security testing throughout
- Cross-browser compatibility

### Architecture decisions
- Monorepo vs polyrepo evaluation
- Shared code organization
- API gateway implementation
- BFF pattern when beneficial
- Microservices vs monolith
- State management selection
- Caching layer placement
- Build tool optimization

### Performance optimization
- Database query optimization
- API response time improvement
- Frontend bundle size reduction
- Image and asset optimization
- Lazy loading implementation
- Server-side rendering decisions
- CDN strategy planning
- Cache invalidation patterns

### Deployment pipeline
- Infrastructure as code setup
- CI/CD pipeline configuration
- Environment management strategy
- Database migration automation
- Feature flag implementation
- Blue-green deployment setup
- Rollback procedures
- Monitoring integration

### Development activities
- Database schema implementation
- API endpoint creation
- Frontend component building
- Authentication integration
- State management setup
- Real-time features if needed
- Comprehensive testing
- Documentation creation

### Technology selection matrix
- Frontend framework evaluation
- Backend language comparison
- Database technology analysis
- State management options
- Authentication methods
- Deployment platform choices
- Monitoring solution selection
- Testing framework decisions

### Shared code management
- TypeScript interfaces for API contracts
- Validation schema sharing (Zod/Yup)
- Utility function libraries
- Configuration management
- Error handling patterns
- Logging standards
- Style guide enforcement
- Documentation templates

### Feature specification approach
- User story definition
- Technical requirements
- API contract design
- UI/UX mockups
- Database schema planning
- Test scenario creation
- Performance targets
- Security considerations

### Integration patterns
- API client generation
- Type-safe data fetching
- Error boundary implementation
- Loading state management
- Optimistic update handling
- Cache synchronization
- Real-time data flow
- Offline capability
