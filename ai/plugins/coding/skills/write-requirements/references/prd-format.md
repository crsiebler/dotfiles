# Requirements formats

Define clear, actionable outcomes and acceptance; scale the document to the work.

---

## The Job

1. Receive a feature description from the user
2. Ask only unresolved questions that materially affect requirements; lettered options can help
3. Generate a bounded-task brief or fuller PRD based on scope and answers
4. Save to the requested path when file creation was requested or confirmed;
   propose `tasks/prd-[feature-name].md` for a fuller PRD

**Important:** Do NOT start implementing. Just create the PRD.

If the user requested a conversational draft, return it without a save prompt.
A request to create or save a document authorizes a new project-local file in
scope; resolve routine naming from the request and project. Apply the preservation
guard before every save.

## PRD lifecycle and preservation

PRDs record approved requirements, requirement changes, and open questions; label
drafts and assumptions rather than presenting them as approved. Once execution
begins, implementation outcomes and checkpoints belong in worktree-root
`progress.md`. Approved requirement changes update the PRD and should be
cross-referenced from that journal during execution. Do not bloat the PRD with
execution notes or require/create the journal while drafting requirements.

1. Check whether the exact target PRD exists before saving. Never automatically
   overwrite, move, or archive existing files. A new PRD request is not approval
   to replace one. Explicit revisions of the same PRD update only approved scope.
2. For replacement, preview the existing path, a unique project-local archive
   destination such as `archive/YYYY-MM-DD-feature-name-prd/tasks/prd-feature.md`,
   and the proposed replacement. Carry forward existing exact-path
   archival/replacement approval when unchanged; otherwise obtain the missing
   scope before writing the replacement. Never overwrite an archive.
3. Recheck source/destination and approved scope, copy the existing PRD to the
   archive, and verify identical contents before replacing the active file. Do
   not follow out-of-project symlinks. If approval is withheld or preservation
   fails, leave the original unchanged and return the draft in the response.
4. Never archive `PLAN.md`, `plan.json`, `memory.json`, or `progress.md` as a
   drafting side effect. Completed-run archival belongs to execution's
   deterministic helper after verified execution, including the run-owned PRDs.
   PRD replacement is a separate preservation guard. Preserve unrelated files.

## Choose the smallest complete format

Use a bounded-task brief when the outcome and affected behavior are clear and the
work fits a small number of focused changes. A supplied approved request may
already contain this brief; avoid requiring another document before planning.
Include every in-scope condition, edge case, constraint and exclusion:

```markdown
# Task: <name>
- Outcome / users: <problem solved and who benefits>
- Scope / exclusions: <included and excluded behavior>
- Acceptance: <observable condition/action and expected result for each outcome>
- Constraints / dependencies: <known compatibility, preservation and prerequisites>
- Assumptions / open questions: <material gaps or none>
```

Use the fuller PRD below for larger or interdependent outcomes, significant
uncertainty or coordination, or an explicit PRD request. Do not drop acceptance
coverage because a brief is shorter. Do not invent phases, task-source adapters,
prepared branch names, run IDs, archive manifests, execution logs or launch grants.
Downstream planning owns story/DAG data; execution owns lifecycle enrollment and can optionally
enroll saved PRDs for deterministic archival. Preserve any existing work-run
metadata unchanged while revising requirements; report a conflict rather than
silently rebinding it. A new requirements document needs no work-run block.

---

## Step 1: Clarifying Questions

Ask only critical questions where the initial prompt is ambiguous. Focus on:

- **Problem/Goal:** What problem does this solve?
- **Core Functionality:** What are the key actions?
- **Scope/Boundaries:** What should it NOT do?
- **Success Criteria:** How do we know it's done?

### Format Questions Like This:

```
1. What is the primary goal of this feature?
   A. Improve user onboarding experience
   B. Increase user retention
   C. Reduce support burden
   D. Other: [please specify]

2. Who is the target user?
   A. New users only
   B. Existing users only
   C. All users
   D. Admin users only

3. What is the scope?
   A. Minimal viable version
   B. Full-featured implementation
   C. Just the backend/API
   D. Just the UI
```

This lets users respond with "1A, 2C, 3B" for quick iteration. Remember to indent the options.

---

## Step 2: PRD Structure

For the fuller PRD, use these sections when they add information:

### 1. Introduction/Overview
Brief description of the feature and the problem it solves.

### 2. Goals
Specific, measurable objectives (bullet list).

### 3. User Stories
Each outcome story needs:
- **Title:** Short descriptive name
- **Description:** "As a [user], I want [feature] so that [benefit]"
- **Acceptance Criteria:** Verifiable checklist of what "done" means
- **Recommended Agents:** Optional specialist hints when supplied or useful;
  planning checks availability and decides bounded advisor use

Requirements stories describe outcomes. prepare-implementation owns the bounded
implementation-story breakdown and dependency ordering.

Use the parent's [autonomous acceptance scope](../SKILL.md#acceptance-for-autonomous-implementation).
Acceptance checks must be agent-executable and noninteractive. Do not introduce
manual test verification, human sign-off or routine deployment checks. Explicit
non-automatable source requirements remain visible as unresolved scope/method
conflicts, not silently removed requirements or manual completion checkboxes.
Deployment checks require explicit scope and an automatable path. Planning
resolves concrete commands and runtime readiness; drafting need not prove a
future test already exists. Optional human follow-up is outside goal completion.

**Format:**
```markdown
### US-001: [Title]
**Description:** As a [user], I want [feature] so that [benefit].

**Acceptance Criteria:**
- [ ] Specific verifiable criterion
- [ ] Another criterion
- [ ] Applicable automated typecheck passes
- [ ] Automated tests verify the specified behavior and edge cases
- [ ] **[UI stories only]** Agent-executable browser checks verify the affected flow using verify-interface

**Recommended Agents:** @reviewer
```

**Important:**
- Acceptance criteria must be verifiable, not vague. "Works correctly" is bad. "Button shows confirmation dialog before deleting" is good.
- Include relevant technical verification needs; planning resolves actual commands
  and whether typecheck is applicable. Do not invent an unavailable check.
- For testable behavior, include automated checks of the stated outcome and edge
  cases; tests passing alone is not the product requirement.
- For UI changes, require agent-executable browser verification with
  verify-interface, not a person clicking through the flow or approving results.

### Optional role and skill hints

For each implementation story, include 0-2 role hints only when they clarify
ownership or independent assessment. Verify actual native availability first;
hints neither invoke agents nor grant authority. Custom role hints use researcher,
planner, reviewer, auditor or operator.

Ordinary source work stays in the main session or an available native execution
agent, with an independent reviewer when required. Codex uses worker; OpenCode
delegation can use general. Record the actual choice during execution preflight,
not as an assumed custom role or mandatory delegation step.
Researcher investigates; planner authors a plan without starting it. Auditor
preserves inspection-only scope. Operator is for explicitly authorized live
operations, not an automatic part of a code story. The main session coordinates.

Select knowledge separately through matching advertised skills and only relevant
references. Examples: React uses apply-web-standards; database changes use
apply-database-standards; AI work uses apply-ai-standards; MCP uses
create-mcp-server. Do not add a role per technology or require every custom role.

Examples:
- React interface story: Recommended Agents: @reviewer;
  relevant knowledge: apply-web-standards and verify-interface.
- Database query repair: Recommended Agents: @reviewer;
  relevant knowledge: apply-database-standards.
- Inspection-only control assessment: Recommended Agents: @auditor;
  relevant knowledge: assess-controls.
- Authorized service recovery: Recommended Agents: @operator;
  relevant knowledge: operate-systems and relevant infrastructure standards.

### 4. Functional Requirements
Numbered list of specific functionalities:
- "FR-1: The system must allow users to..."
- "FR-2: When a user clicks X, the system must..."

Be explicit and unambiguous.

### 5. Non-Goals (Out of Scope)
What this feature will NOT include. Critical for managing scope.

### 6. Design Considerations (Optional)
- UI/UX requirements
- Link to mockups if available
- Relevant existing components to reuse

### 7. Technical Considerations (Optional)
- Known constraints or dependencies
- Integration points with existing systems
- Performance requirements

### 8. Success Metrics
Define observable success from the user's goals. Include numerical targets only
when supplied or agreed; otherwise identify the measurement and unresolved target.

### 9. Open Questions
Remaining questions or areas needing clarification.

---

## Writing for Junior Developers

The PRD reader may be a junior developer or AI agent. Therefore:

- Be explicit and unambiguous
- Avoid jargon or explain it
- Provide enough detail to understand purpose and core logic
- Number requirements for easy reference
- Use concrete examples where helpful

---

## Output

- **Format:** Markdown (`.md`)
- **Location:** `tasks/`
- **Filename:** `prd-[feature-name].md` (kebab-case)
- **Safety:** Check the target and follow the preservation guard; replacement requires explicit archival approval and verified preservation first.

---

## Example PRD

```markdown
# PRD: Task Priority System

## Introduction

Add priority levels to tasks so users can focus on what matters most. Tasks can be marked as high, medium, or low priority, with visual indicators and filtering to help users manage their workload effectively.

## Goals

- Allow assigning priority (high/medium/low) to any task
- Provide clear visual differentiation between priority levels
- Enable filtering and sorting by priority
- Default new tasks to medium priority

## User Stories

### US-001: Add priority field to database
**Description:** As a developer, I need to store task priority so it persists across sessions.

**Acceptance Criteria:**
- [ ] Add priority column to tasks table: 'high' | 'medium' | 'low' (default 'medium')
- [ ] Automated migration checks preserve existing records and assign medium priority by default in an authorized test environment
- [ ] Typecheck passes

**Recommended Agents:** @reviewer

### US-002: Display priority indicator on task cards
**Description:** As a user, I want to see task priority at a glance so I know what needs attention first.

**Acceptance Criteria:**
- [ ] Each task card shows colored priority badge (red=high, yellow=medium, gray=low)
- [ ] Priority visible without hovering or clicking
- [ ] Typecheck passes
- [ ] Agent-executable browser checks verify the affected flow using verify-interface

**Recommended Agents:** @reviewer

### US-003: Add priority selector to task edit
**Description:** As a user, I want to change a task's priority when editing it.

**Acceptance Criteria:**
- [ ] Priority dropdown in task edit modal
- [ ] Shows current priority as selected
- [ ] Saves immediately on selection change
- [ ] Typecheck passes
- [ ] Agent-executable browser checks verify the affected flow using verify-interface

**Recommended Agents:** @reviewer

### US-004: Filter tasks by priority
**Description:** As a user, I want to filter the task list to see only high-priority items when I'm focused.

**Acceptance Criteria:**
- [ ] Filter dropdown with options: All | High | Medium | Low
- [ ] Filter persists in URL params
- [ ] Empty state message when no tasks match filter
- [ ] Typecheck passes
- [ ] Agent-executable browser checks verify the affected flow using verify-interface

**Recommended Agents:** @researcher

## Functional Requirements

- FR-1: Add `priority` field to tasks table ('high' | 'medium' | 'low', default 'medium')
- FR-2: Display colored priority badge on each task card
- FR-3: Include priority selector in task edit modal
- FR-4: Add priority filter dropdown to task list header
- FR-5: Sort by priority within each status column (high to medium to low)

## Non-Goals

- No priority-based notifications or reminders
- No automatic priority assignment based on due date
- No priority inheritance for subtasks

## Technical Considerations

- Reuse existing badge component with color variants
- Filter state managed via URL search params
- Priority stored in database, not computed

## Success Metrics

- Users can change priority through the agreed task-edit interaction
- High-priority tasks immediately visible at top of lists
- No regression in task list performance

## Open Questions

- Should priority affect task ordering within a column?
- Should we add keyboard shortcuts for priority changes?
```

---

## Checklist

Before saving the PRD:

- [ ] Resolved material ambiguities or labeled assumptions
- [ ] Incorporated user's answers
- [ ] Outcomes are specific and all acceptance conditions are covered
- [ ] Each implementation story recommends 0-2 relevant development agents
- [ ] Functional requirements are numbered and unambiguous
- [ ] Non-goals section defines clear boundaries
- [ ] Existing PRD preserved under the approved revision or archive-before-replace scope
- [ ] No execution checkpoints or state files created during drafting
- [ ] Requested save path honored; no run/archive metadata created
