# Ralph PRD Converter

Converts existing PRDs to the plan.json format that Ralph uses for autonomous execution.

---

## The Job

Take a PRD (markdown file or text) and convert it to `plan.json` in the Ralph
working directory where the `ralph` primary agent expects to read it.

This is a planning adapter, not execution authorization. Approved execution uses
[Bounded Story Execution](story-execution.md) and the full sibling
[Story Review](story-review.md) protocol, loaded relative to the installed
`prepare-implementation` skill. Preserve the JSON keys and types below. Ralph
maps `branchName`, `userStories`, and `passes` to the shared execution contract;
the runner still owns external iterations and their maximum. Prepare a committed
worktree on that exact branch before execution; never use `main`, `master`, or
detached HEAD. Execution and per-story commits require explicit authorization;
migrations and Docker operations still require their own applicable approvals.

If `plan.json` already exists, preserve it and require confirmation for scoped
updates. Do not overwrite an unfinished run with a different feature. Completed
runs use the separately approved [archival procedure](completed-run-archive.md),
after the runner has validated completion and exited, not during conversion.

Keep `plan.json` a stable task source with concise planning context in `notes`,
not execution narratives. Append execution evidence only to worktree-root
`docs/progress.md`; bounded reusable review knowledge stays in root `memory.json`.
Planning creates neither state file and never resets them.

---

## Output Format

```json
{
  "project": "[Project Name]",
  "branchName": "ralph/[feature-name-kebab-case]",
  "description": "[Feature description from PRD title/intro]",
  "userStories": [
    {
      "id": "US-001",
      "title": "[Story title]",
      "description": "As a [user], I want [feature] so that [benefit]",
      "acceptanceCriteria": [
        "Criterion 1",
        "Criterion 2",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": "Recommended agents: @agent-name, @agent-name. Implementation notes: ..."
    }
  ]
}
```

---

## Story Size: The Number One Rule

**Each story must be completable in ONE Ralph iteration (one context window).**

Ralph starts a fresh implementation context per iteration and relies on project-local handoff files. Oversized stories can exceed that context before verification finishes.

### Right-sized stories:
- Add a database column and migration
- Add a UI component to an existing page
- Update a server action with new logic
- Add a filter dropdown to a list

### Too big (split these):
- "Build the entire dashboard" - Split into: schema, queries, UI components, filters
- "Add authentication" - Split into: schema, middleware, login UI, session handling
- "Refactor the API" - Split into one story per endpoint or pattern

**Rule of thumb:** If you cannot describe the change in 2-3 sentences, it is too big.

---

## Story Ordering: Dependencies First

Stories execute in priority order. Earlier stories must not depend on later ones.

**Correct order:**
1. Schema/database changes (migrations)
2. Server actions / backend logic
3. UI components that use the backend
4. Dashboard/summary views that aggregate data

**Wrong order:**
1. UI component (depends on schema that does not exist yet)
2. Schema change

---

## Acceptance Criteria: Must Be Verifiable

Each criterion must be something Ralph can CHECK, not something vague.

### Good criteria (verifiable):
- "Add `status` column to tasks table with default 'pending'"
- "Filter dropdown has options: All, Active, Completed"
- "Clicking delete shows confirmation dialog"
- "Typecheck passes"
- "Tests pass"

### Bad criteria (vague):
- "Works correctly"
- "User can do X easily"
- "Good UX"
- "Handles edge cases"

### Always include as final criterion:
```
"Typecheck passes"
```

For stories with testable logic, also include:
```
"Tests pass"
```

### For stories that change UI, also include:
```
"Verify in browser using verify-interface skill"
```

Frontend stories require browser verification using `verify-interface`.

---

## Conversion Rules

1. **Each user story becomes one JSON entry**
2. **IDs**: Sequential (US-001, US-002, etc.)
3. **Priority**: Based on dependency order, then document order
4. **All stories**: `passes: false`
5. **branchName**: Derive from feature name, kebab-case, prefixed with `ralph/`
6. **Always add**: "Typecheck passes" to every story's acceptance criteria
7. **Recommended agents**: Preserve PRD `Recommended Agents` lines in each
   story's `notes` field so Ralph can optionally invoke the right
   implementation specialists before editing code

---

## Recommended Agent Notes

Ralph reads each selected story's `notes` before implementation and treats
`Recommended agents:` entries as optional guidance. Convert each PRD story's
recommended agents into the JSON `notes` field using exact configured agent
names with `@` prefixes.

Use this format:

```json
"notes": "Recommended agents: @agent-a, @agent-b. Implementation notes: concise context Ralph should preserve."
```

If the PRD does not include recommended agents, infer 0-2 relevant development
specialists from the story scope. Omit recommended agents for trivial,
mechanical, docs-only, or low-risk stories. Keep recommendations focused and
avoid business, planning, sales, legal, marketing, research-only, and
orchestration agents.

These are candidate names, not proof of runtime availability. Preserve supplied
`@agent-name` hints as optional notes; verify configured names before adding new
ones. Discovery does not load or invoke an agent. Do not require delegation.

These notes select optional read-only implementation advisors, not the staged
review role. The shared mode/risk budget selects self-review or the exact native
`ralph-reviewer` in OpenCode (`story-reviewer` for Codex Goal Markdown execution).
When native review is required, missing role availability blocks execution;
never substitute an arbitrary or general-purpose reviewer from these examples.

Use this scope matrix:

- General implementation: `@backend-developer`, `@frontend-developer`,
  `@fullstack-developer`, `@cli-developer`, `@tooling-engineer`
- Debugging and quality: `@debugger`, `@test-automator`,
  `@refactoring-specialist`, `@architect-reviewer`, `@performance-engineer`
- Build and dependencies: `@build-engineer`, `@dependency-manager`
- Security and compliance: `@security-engineer`, `@security-auditor`,
  `@compliance-auditor`
- Documentation: `@documentation-engineer`, `@technical-writer`
- UI, UX, and accessibility: `@react-specialist`, `@nextjs-developer`,
  `@vue-expert`, `@angular-architect`, `@ui-designer`, `@ux-researcher`,
  `@accessibility-tester`
- API and backend architecture: `@api-designer`, `@graphql-architect`,
  `@websocket-engineer`, `@microservices-architect`
- Databases and data: `@sql-pro`, `@postgres-pro`, `@database-optimizer`,
  `@database-administrator`, `@data-engineer`
- DevOps and infrastructure: `@devops-engineer`, `@deployment-engineer`,
  `@kubernetes-specialist`, `@terraform-engineer`, `@cloud-architect`,
  `@platform-engineer`, `@sre-engineer`
- Language and framework specialists: `@typescript-pro`, `@javascript-pro`,
  `@python-pro`, `@golang-pro`, `@rust-engineer`, `@java-architect`,
  `@spring-boot-engineer`, `@csharp-developer`, `@dotnet-core-expert`,
  `@php-pro`, `@laravel-specialist`, `@rails-expert`, `@django-developer`
- Mobile and native: `@mobile-developer`, `@flutter-expert`,
  `@swift-expert`, `@kotlin-specialist`, `@electron-pro`
- AI and integrations: `@ai-engineer`, `@ml-engineer`, `@llm-architect`,
  `@nlp-engineer`, `@mcp-developer`, `@payment-integration`,
  `@slack-expert`, `@wordpress-master`

Examples:

- Schema or query story: `Recommended agents: @database-optimizer, @sql-pro.`
- React UI story: `Recommended agents: @react-specialist, @accessibility-tester.`
- CLI tool story: `Recommended agents: @cli-developer, @test-automator.`
- Dependency story: `Recommended agents: @dependency-manager, @build-engineer.`

---

## Splitting Large PRDs

If a PRD has big features, split them:

**Original:**
> "Add user notification system"

**Split into:**
1. US-001: Add notifications table to database
2. US-002: Create notification service for sending notifications
3. US-003: Add notification bell icon to header
4. US-004: Create notification dropdown panel
5. US-005: Add mark-as-read functionality
6. US-006: Add notification preferences page

Each is one focused change that can be completed and verified independently.

---

## Example

**Input PRD:**
```markdown
# Task Status Feature

Add ability to mark tasks with different statuses.

## Requirements
- Toggle between pending/in-progress/done on task list
- Filter list by status
- Show status badge on each task
- Persist status in database
```

**Output plan.json:**
```json
{
  "project": "TaskApp",
  "branchName": "ralph/task-status",
  "description": "Task Status Feature - Track task progress with status indicators",
  "userStories": [
    {
      "id": "US-001",
      "title": "Add status field to tasks table",
      "description": "As a developer, I need to store task status in the database.",
      "acceptanceCriteria": [
        "Add status column: 'pending' | 'in_progress' | 'done' (default 'pending')",
        "Generate and run migration successfully",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": "Recommended agents: @database-optimizer, @sql-pro. Implementation notes: preserve the status enum values and default from the PRD."
    },
    {
      "id": "US-002",
      "title": "Display status badge on task cards",
      "description": "As a user, I want to see task status at a glance.",
      "acceptanceCriteria": [
        "Each task card shows colored status badge",
        "Badge colors: gray=pending, blue=in_progress, green=done",
        "Typecheck passes",
         "Verify in browser using verify-interface skill"
      ],
      "priority": 2,
      "passes": false,
      "notes": "Recommended agents: @react-specialist, @accessibility-tester. Implementation notes: reuse existing badge patterns if present."
    },
    {
      "id": "US-003",
      "title": "Add status toggle to task list rows",
      "description": "As a user, I want to change task status directly from the list.",
      "acceptanceCriteria": [
        "Each row has status dropdown or toggle",
        "Changing status saves immediately",
        "UI updates without page refresh",
        "Typecheck passes",
         "Verify in browser using verify-interface skill"
      ],
      "priority": 3,
      "passes": false,
      "notes": "Recommended agents: @frontend-developer, @accessibility-tester. Implementation notes: keep status updates immediate and visible."
    },
    {
      "id": "US-004",
      "title": "Filter tasks by status",
      "description": "As a user, I want to filter the list to see only certain statuses.",
      "acceptanceCriteria": [
        "Filter dropdown: All | Pending | In Progress | Done",
        "Filter persists in URL params",
        "Typecheck passes",
         "Verify in browser using verify-interface skill"
      ],
      "priority": 4,
      "passes": false,
      "notes": "Recommended agents: @frontend-developer, @ux-researcher. Implementation notes: preserve filter state in URL params."
    }
  ]
}
```

---

## Archiving Completed Runs

After all stories pass checks/review and their commits succeed, wait for runner
completion validation and exit. Offer the [shared archival procedure](completed-run-archive.md)
for `plan.json`, `docs/progress.md`, and existing `memory.json` together. It requires
explicit approval and verified preservation before active-copy removal. Do not
archive inside an iteration, reset the journal, or assume automatic runner cleanup.

---

## Checklist Before Saving

Before writing plan.json, verify:

- [ ] No unfinished run is being replaced; completed-run archival is separately approved
- [ ] Each story is completable in one iteration (small enough)
- [ ] Stories are ordered by dependency (schema to backend to UI)
- [ ] Every story has "Typecheck passes" as criterion
- [ ] Stories with testable logic have "Tests pass" as criterion
- [ ] UI stories have "Verify in browser using verify-interface skill" as criterion
- [ ] Each story's `notes` includes 0-2 relevant recommended development agents
- [ ] Acceptance criteria are verifiable (not vague)
- [ ] No story depends on a later story
- [ ] Story IDs are unique
- [ ] Priorities are ordered by dependency and execution sequence
- [ ] Every story starts with `passes: false`
- [ ] Generated output is valid JSON
- [ ] Existing `plan.json` overwrite or archive behavior was confirmed when needed
