# Markdown implementation checklist

Write project-local `PLAN.md` unless the user specifies another path. Inspect
relevant source and verification commands. Planning does not execute checks,
create execution state, assign runtime models or launch workers.

Use unique story IDs, priorities and explicit dependency edges. Validate the DAG
using [dependency graph](dependency-graph.md). Preserve source acceptance through
[acceptance coverage](../SKILL.md#preserve-acceptance-coverage). Recommend relevant
known agents by expertise only; discovery is not invocation. Include observable
behavior, integration criteria and project-supported tests/typecheck/lint/browser
commands. Mark unavailable checks honestly.

```markdown
# Implementation plan: <feature>

## Objective and context
- Objective: <observable outcome>
- Sources: <approved request/brief or PRDs and inspected paths>
- Plan revision: <stable scope revision and approved baseline when known>
- Scope / non-goals: <included and excluded work>
- Working branch: <known exact branch or pending preparation>
- Authorization gaps: <missing execution/lifecycle/delivery scope or none>
- Verification: <real commands and unavailable checks>
- Assumptions / open questions: <material gaps or none>

## Approach and dependencies
<source-backed approach and prerequisite order; phases only if useful>

## Ordered stories

### US-001 - <bounded story title>
- [ ] Story complete
- Priority: 1
- Depends on: none
- Phase / requirements: <source criteria; phase optional>
- User story: As a <user>, I want <capability> so that <benefit>.
- Relevant paths: <source/test paths>
- Recommended agents: <optional known specialist names and bounded questions>

#### Acceptance criteria
- [ ] <condition/action and expected behavior>
- [ ] <edge cases and integrated outcome; contributing stories and acceptance owner>
- [ ] <required checks with real commands or supported exemptions>
```

Start new completion markers unchecked; preserve completed state on approved
revisions. Keep execution narratives out of the plan. One story owns each split
integrated acceptance outcome. Complete the coverage audit before handoff.
Report the saved path, revision, order/DAG validation, recommended expertise,
source coverage, exclusions and remaining authority or verification gaps.

Optional [run metadata](run-manifest.md) describes artifact ownership only.
Before replacing a completed plan, verify existing preservation evidence and
current source hashes under the parent skill's preservation guard. Missing or
mismatched evidence blocks replacement. Never archive, remove execution files,
or invoke an execution workflow as a planning side effect.
