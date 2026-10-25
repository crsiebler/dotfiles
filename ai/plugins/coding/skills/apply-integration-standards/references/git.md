# Git repositories and automation

Inspect repository instructions, current branch, index/worktree state, remotes
and history before selecting an operation. Preserve unrelated work. Technology
knowledge does not authorize branch deletion, history changes or external writes.
Use the advertised manage-changes skill for authorized commit/push/PR delivery;
this reference adds no shipping loop or approval policy.

## Standards

Follow the repository's branch and merge policy. Resolve conflicts by preserving
both intended behaviors, not by blindly selecting one side. Verify the combined
result. Check hooks, generated files, submodules and large-file handling only
when relevant. Preserve protections and do not bypass failing hooks or checks.
Distinguish local state, remote state and proposed operations in the handoff.
Never imply a push, review, merge, release or deployment occurred without evidence.

## Conditional topic inventory

These topics are options to assess against actual requirements, not a mandate
to adopt Git Flow, rewrite history, install hooks, release or automate merges.
Inspect version-sensitive commands against the installed Git and official docs.

### Branching strategies

- Git Flow implementation
- GitHub Flow setup
- GitLab Flow configuration
- Trunk-based development
- Feature branch workflow
- Release branch management
- Hotfix procedures
- Environment branches

### Merge management

- Conflict resolution strategies
- Merge vs rebase policies
- Squash merge guidelines
- Fast-forward enforcement
- Cherry-pick procedures
- History rewriting rules
- Bisect strategies
- Revert procedures

### Git hooks

- Pre-commit validation
- Commit message format
- Code quality checks
- Security scanning
- Test execution
- Documentation updates
- Branch protection
- CI/CD triggers

### PR/MR automation

- Template configuration
- Label automation
- Review assignment
- Status checks
- Auto-merge setup
- Conflict detection
- Size limitations
- Documentation requirements

### Release management

- Version tagging
- Changelog generation
- Release notes automation
- Asset attachment
- Branch protection
- Rollback procedures
- Deployment triggers
- Communication automation

### Repository maintenance

- Size optimization
- History cleanup
- LFS management
- Archive strategies
- Mirror setup
- Backup procedures
- Access control
- Audit logging

### Automation tools

- Pre-commit hooks
- Husky configuration
- Commitizen setup
- Semantic release
- Changelog generation
- Auto-merge bots
- PR automation
- Issue linking

### Monorepo strategies

- Repository structure
- Subtree management
- Submodule handling
- Sparse checkout
- Partial clone
- Performance optimization
- CI/CD integration
- Release coordination

### Branching best practices

- Clear naming conventions
- Branch protection rules
- Merge requirements
- Review policies
- Cleanup automation
- Stale branch handling
- Fork management
- Mirror synchronization

### Commit conventions

- Format standards
- Message templates
- Type prefixes
- Scope definitions
- Breaking changes
- Footer format
- Sign-off requirements
- Verification rules

### Automation examples

- Commit validation
- Branch creation
- PR templates
- Label management
- Milestone tracking
- Release automation
- Changelog generation
- Notification workflows

### Conflict prevention

- Early integration
- Small changes
- Clear ownership
- Communication protocols
- Rebase strategies
- Lock mechanisms
- Architecture boundaries
- Team coordination

### Security practices

- Signed commits
- GPG verification
- Access control
- Audit logging
- Secret scanning
- Dependency checking
- Branch protection
- Review requirements
