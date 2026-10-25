# Markdown implementation checklist

Write project-local `PLAN.md` unless the user specifies another path. Inspect
relevant source and verification commands. Planning does not execute checks,
create execution state, assign runtime models or launch workers.

Use unique story IDs, priorities and explicit dependency edges. Validate the DAG
using [dependency graph](dependency-graph.md). Preserve source acceptance through
[acceptance coverage](../SKILL.md#preserve-acceptance-coverage). Recommend relevant
known agents by expertise only; discovery is not invocation. Include observable
behavior, integration criteria and agent-executable, noninteractive
tests/typecheck/lint/browser checks. Do not add manual verification or routine
deployment gates. Deployment verification must be explicitly in scope and
automatable. Mark unavailable required runtime capabilities as planning blockers;
planned test/automation authoring can be a scoped prerequisite story.
Complete [execution readiness](execution-readiness.md) before calling the plan
ready for unattended launch. Keep its evidence in this plan, not a second tracker.

```markdown
# Implementation plan: <feature>

## Objective and context
- Objective: <observable outcome>
- Sources: <approved request/brief or PRDs and inspected paths>
- Plan revision: <stable scope revision and approved baseline when known>
- Scope / non-goals: <included and excluded work>
- Working branch: <known exact branch or pending preparation>
- Authorization gaps: <missing execution/lifecycle/delivery scope or none>
- Verification: <noninteractive commands/tool procedures, inputs and expected results; planned automation owner>
- Assumptions / open questions: <material gaps or none>

## Execution readiness
- Requested endpoint: <implemented requirements, automated verification, independent agent review and scoped local delivery>
- Audited revision / runtime / environment: <scope and actual capability evidence>
- Unattended readiness: blocked | ready
- Launch: awaits explicit implementation request; planning does not start work

| Gate source / action / affected stories | Target and effect | Authority / resolution evidence | Disposition |
| --- | --- | --- | --- |
| <applicable instruction or manual prerequisite> | <exact scope and limits> | <existing grant, verified completion or approved change> | <resolved: authorized/completed/changed approach, or blocked> |

- Remaining blockers: <exact missing action/decision, owner and completion evidence; or none>
- Recheck at launch: <validity limits or changed conditions that would invalidate readiness>

Remove the example row when no gates apply and explain the inspected evidence.
Do not mark ready with pending human prerequisites or unsupported capabilities.

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
- [ ] <automated check: command/tool procedure, inputs and expected result; prerequisite automation story if needed>
```

Start new completion markers unchecked; preserve completed state on approved
revisions. Keep execution narratives out of the plan. One story owns each split
integrated acceptance outcome. Complete the coverage audit before handoff.
Report the saved path, revision, order/DAG validation, recommended expertise,
source coverage, exclusions, gate resolutions and unattended readiness. Pending
authority or mandatory manual/verification prerequisites keep the plan a draft.
Explicit non-automatable requirements remain planning conflicts, not manual
checkboxes in executable stories. Optional human follow-up is not a completion gate.

Optional [run metadata](run-manifest.md) describes artifact ownership only.
Before replacing a completed plan, verify existing preservation evidence and
current source hashes under the parent skill's preservation guard. Missing or
mismatched evidence blocks replacement. Never archive, remove execution files,
or invoke an execution workflow as a planning side effect.
