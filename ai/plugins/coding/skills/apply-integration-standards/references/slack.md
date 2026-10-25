# Slack apps

Apply only to an actual project using this technology. Read the bundle's entry
and requirements first. Project versions, constraints and existing tools override
the topic inventory below; inherited version labels are examples, not minimum
requirements or claims of current support. Verify relevant APIs against official
documentation for the installed version before relying on them.

## Standards

Verify SDK/API/transport choices. Preserve signature verification and scopes; acknowledge within the platform deadline, handle retries/deduplication and rate limits. No implicit messaging or OAuth changes.

## Conditional topic inventory

These are investigation topics, not a setup plan, required dependencies, acceptance
criteria or instructions to execute changes. No universal latency, coverage,
deployment or architecture target applies. Load only relevant sections.

### Slack Bolt SDK (@slack/bolt)

- Event handling patterns and best practices
- Middleware architecture and custom middleware creation
- Action, shortcut, and view submission handlers
- Socket Mode vs. HTTP mode trade-offs
- Error handling and graceful degradation
- TypeScript integration and type safety

### Slack APIs

- Web API methods and rate limiting strategies
- Events API subscription and verification
- Conversations API for channel/DM management
- Users API and user presence
- Files API and file sharing
- Admin APIs for Enterprise Grid

### Block Kit & UI

- Block Kit Builder patterns
- Interactive components (buttons, select menus, overflow menus)
- Modal workflows and multi-step forms
- Home tab design and App Home best practices
- Message formatting with mrkdwn
- Attachment vs. Block Kit migration

### Authentication & Security

- OAuth flows supported by the project and current platform
- Bot tokens vs. user tokens
- Token rotation and secure storage
- Scopes and principle of least privilege
- Request signature verification

### Additional platform surfaces (verify availability)

- Workflow Builder custom steps
- Slack Canvas API
- Slack Lists
- Huddles integrations
- Slack Connect for external collaboration

### When reviewing Slack-related code

- Verify proper error handling for API calls
- Check for rate limit handling with backoff
- Ensure request signature verification
- Validate Block Kit JSON structure
- Confirm proper token management
- Look for deprecated API usage
- Assess scalability implications
- Check for security vulnerabilities

### Event-driven design

- Evaluate events versus polling for the supported delivery requirements
- Choose Socket Mode or HTTP based on the project transport
- Implement proper event acknowledgment
- Handle duplicate events gracefully

### Message threading

- Use thread_ts for conversations
- Evaluate whether channel broadcast is requested and authorized
- Handle unfurling appropriately

### Channel organization

- Naming conventions
- Private vs. public decisions
- Slack Connect considerations

### Compatibility and safety

- Choose supported APIs and message layouts for the actual use case.
- Verify deferred-response mechanisms against the interaction type and SDK version.
- Respect rate-limit responses and bounded retry policies.
- Keep tokens in the approved secret mechanism, out of code, logs and output.
- Preserve request verification and existing authorization scopes.
- Sending messages, changing subscriptions or installing an app requires the caller's authority.
