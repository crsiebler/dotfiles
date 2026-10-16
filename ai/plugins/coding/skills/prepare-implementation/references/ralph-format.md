# Ralph implementation plan

Convert approved requirements into `plan.json`. Preserve the JSON keys/types
below. This adapter produces task data only; it does not launch Ralph, run
checks, assign models, create execution state or invoke another skill.

Use bounded task details or approved PRDs. Preserve source criteria, stable
revision and useful phase/dependency references in existing description/notes.
Recommend available specialist agents by expertise. No separate PRD or manifest
is required for a bounded task. Optional [run metadata](run-manifest.md) describes
ownership without granting execution or archival authority.

Validate unique IDs and the complete [dependency graph](dependency-graph.md).
Order prerequisites before dependents using numeric priorities and explicit IDs
in notes; do not add JSON keys. Record a known branch or report preparation as
pending; planning creates or switches no branches. Preserve existing completion
markers during scoped revisions, and never replace an unfinished run.

Before replacing a completed plan, verify existing archive/preservation receipts
and current hashes. Missing/mismatched evidence blocks replacement. Planning
does not perform archival, remove execution state or invoke execution workflows.

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

Ralph executes serially in priority order; this format is not a concurrent DAG
runtime. Encode dependencies as exact existing story IDs in notes and order their
prerequisites earlier. Validate missing references, self-dependencies and cycles
before handoff; reject any dependency on a later story or inconsistent order.
Do not add dependency keys to the JSON schema. Larger planning may describe a
dependency graph, but the current worker still serializes the ordered stories.

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
Apply [acceptance coverage](../SKILL.md#preserve-acceptance-coverage): preserve
source outcomes and constraints in `acceptanceCriteria`; identify the approved request/brief or PRD path
and source criteria in existing `notes`. For split behavior, name contributing
stories and its integration owner there, ordering that owner after prerequisites.
Typecheck, tests, and browser checks accompany behavioral criteria; they do not
replace them.

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

1. **Each bounded implementation story becomes one JSON entry**; PRD stories
   may split or combine when source acceptance coverage and dependencies remain clear
2. **IDs**: Sequential (US-001, US-002, etc.)
3. **Priority**: Based on dependency order, then document order
4. **All stories**: `passes: false`
5. **branchName**: Record the exact existing prepared branch; never invent, create
   or switch it. Examples below illustrate already prepared `ralph/...` branches.
   Missing branch preparation is an execution blocker, not a routing heuristic.
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

If a PRD has big features, split them while preserving its complete behavior:

**Original:**
> "Store user notifications, show unread counts in a header bell, list notifications
> in a dropdown, and let users mark them read. The count and read state survive reload."

**Split into:**
1. US-001: Add notifications table to database
2. US-002: Create notification read/list/update service
3. US-003: Add notification bell icon to header
4. US-004: Create notification dropdown panel
5. US-005: Connect mark-as-read and verify the integrated notification flow

Each is one focused change that can be completed and verified independently.
US-005 depends on US-001 through US-004 and owns verifying that marking a listed
notification read updates the bell's unread count and preserves both after reload.
Do not infer delivery channels or a preferences page from this source.

---

## Example

**Illustrative input PRD and inspected context:**
```markdown
# Task Status Feature

Add ability to mark tasks with different statuses. Source: tasks/prd-task-status.md.

## Requirements
- FR-1: Toggle between pending/in-progress/done on task list and update the badge
- FR-2: Filter list by status; All shows every task and a selected status shows only matches
- FR-3: Show each task's saved status in its badge
- FR-4: Persist status in database so a changed status is retained after reload

Inspected project context: tasks use a relational table and the existing migration
tool; new tasks currently default to pending. Preserve that default.
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
      "notes": "Source: tasks/prd-task-status.md FR-4; inspected task default is pending. Phase 1 storage. US-001 and US-003 contribute; US-003 owns persisted status verification through the task list. Recommended agents: @database-optimizer, @sql-pro."
    },
    {
      "id": "US-002",
      "title": "Display status badge on task cards",
      "description": "As a user, I want to see task status at a glance.",
      "acceptanceCriteria": [
        "Each task card's badge displays its saved pending, in-progress, or done status",
        "Typecheck passes",
        "Verify in browser using verify-interface skill"
      ],
      "priority": 2,
      "passes": false,
      "notes": "Source: tasks/prd-task-status.md FR-3. Phase 2 display; depends on US-001. US-003 integrates status changes with this badge. Recommended agents: @react-specialist, @accessibility-tester."
    },
    {
      "id": "US-003",
      "title": "Add status toggle to task list rows",
      "description": "As a user, I want to change task status directly from the list.",
      "acceptanceCriteria": [
        "Each row has status dropdown or toggle",
        "Selecting pending, in-progress, or done saves that status and updates the row's badge",
        "After changing a task's status and reloading the list, its badge and control display the saved status",
        "Tests pass",
        "Typecheck passes",
        "Verify in browser using verify-interface skill"
      ],
      "priority": 3,
      "passes": false,
      "notes": "Source: tasks/prd-task-status.md FR-1 and FR-4. Phase 3 integration; depends on US-001 storage and US-002 badge. Owns verifying status change, persistence and display together. Recommended agents: @frontend-developer, @accessibility-tester."
    },
    {
      "id": "US-004",
      "title": "Filter tasks by status",
      "description": "As a user, I want to filter the list to see only certain statuses.",
      "acceptanceCriteria": [
        "Filter dropdown: All | Pending | In Progress | Done",
        "Selecting a status displays only tasks with that saved status; All displays every task",
        "Tests pass",
        "Typecheck passes",
        "Verify in browser using verify-interface skill"
      ],
      "priority": 4,
      "passes": false,
      "notes": "Source: tasks/prd-task-status.md FR-2. Phase 4 filtering; depends on US-001 through US-003. Owns verifying filter selection against saved task statuses. Filter persistence is not specified. Recommended agents: @frontend-developer, @ux-researcher."
    }
  ]
}
```

---

## Checklist before saving

- [ ] Source criteria, revision and dependencies mapped without new JSON keys
- [ ] Acceptance coverage and integrated acceptance owners verified
- [ ] Stories are bounded, uniquely identified and dependency ordered
- [ ] Complete dependency graph has no unknown edges, self-dependencies or cycles
- [ ] Relevant tests, typecheck, lint and browser criteria recorded honestly
- [ ] Useful known agents recommended without invoking them or selecting models
- [ ] New stories start with `passes: false`; existing completion state preserved
- [ ] Output parses as valid JSON
- [ ] No unfinished plan replaced; prior completed bytes have verified preservation
