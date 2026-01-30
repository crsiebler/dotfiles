# Personal Agent Configuration

## Communication Style
- Technical and concise responses
- No emojis unless explicitly requested
- GitHub-flavored markdown formatting
- Focus on facts over validation

## Coding Standards
- Always run typecheck before committing
- Follow existing code patterns in project
- Edit existing files over creating new ones

## Git Workflow
**Mandatory Format**: `<type>(<scope>): <description>`

**Types**: feat, fix, docs, style, refactor, test, chore

**Body (Optional)**: Explains motivation, context, and differences from previous behavior

**Footer (Optional)**: Breaking changes (`BREAKING CHANGE:`) or issue tracking (`Fixes #123`)

## Testing
- Write tests before implementation for new features
- Run tests when modifying logic
- Integration tests for critical paths

## Boundaries

### Security (Absolute)
- Never commit secrets or credentials
- Never expose sensitive information in logs or error messages
- Never disable security features
- Never modify authentication/authorization logic

### Git Operations
**Absolute**:
- Never force push (`git push --force`)
- Never modify git history (rebase, amend) on shared branches
- Never push directly to `main`/`master` branch

**Confirmatory**:
- Do not delete branches without confirmation

### File System
**Absolute**:
- Never modify files outside the project directory
- Never use `/tmp/` - always use working directory for temp files
- Never modify system files or global configurations

**Confirmatory**:
- Do not delete files without confirmation

### Database Operations
**Absolute**:
- Never execute DELETE/DROP SQL statements without confirmation
- Never modify production database connections

**Confirmatory**:
- Do not run database migrations without confirmation

### Package Management
- Do not run `npm install`, `yarn install`, `pnpm install`, `bun install` without confirmation
- Do not modify `package.json` dependencies without confirmation
- Do not update package versions without confirmation

### Configuration Files
- Do not modify `.env` files without confirmation
- Do not modify `.gitignore` without confirmation
- Do not modify CI/CD configuration files (`.github/`, `.gitlab-ci.yml`, etc.) without confirmation
- Do not modify Docker configuration files without confirmation
- Do not modify `tsconfig.json` or build configuration without confirmation

### External Services
**Absolute**:
- Never deploy to production without confirmation
- Never send emails or notifications without confirmation

**Confirmatory**:
- Do not create cloud resources (AWS, GCP, Azure) without confirmation
- Do not make external API calls that modify state without confirmation

### Process Management
- Do not kill running processes without confirmation
- Do not restart services without confirmation
- Do not modify system services without confirmation

## Tool Usage
- Prefer specialized tools over bash commands
- Use parallel tool calls when operations are independent
- Task tool for complex multi-step operations

## Environment
- Secrets location: `$HOME/.env`
- MCP servers: Jira, PostgreSQL, Playwright, Chrome DevTools, Jam
- Global commands: `ralph`, `subagents`
