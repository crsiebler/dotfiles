# Coordination Advice

The main session is the only dispatcher and canonical state owner. Advice can
identify independent tasks, dependencies, owned paths, resource conflicts and
capacity needs; it cannot spawn, proxy-dispatch or mutate trackers. Supply
explicit task/candidate/authority/output contracts and reconcile prior
ownership before takeover. Do not dispatch an agent per technology or invent a
context service.

## Choosing useful parallel work

Split only dependency-ready tasks whose outputs can be integrated independently.
Account for packet preparation, review and integration costs; keep tightly coupled
changes in the main loop when parallelism would require repeated synchronization.
Match responsibilities to available native roles and supply domain knowledge
through skills, rather than creating a role or agent for each technology.

Use the existing [task concurrency contract](task-concurrency.md) for roots,
branches, owned paths and shared resources. Prefer fewer workers with clear
ownership over duplicated work. A blocked task does not justify restarting review,
raising budgets or dispatching a replacement owner before reconciling state.

Implementation uses the available native execution agent. A planner may advise on
a design; an auditor may inspect a distinct control question; a reviewer supplies
independent judgment under the workflow's review contract. An operator is only for
separately authorized operational actions. None is a required extra pipeline stage.

Report completed outputs, verified evidence, unresolved dependencies and the next
eligible work to the main session. Use existing task records and native session
controls; do not introduce a scheduler, consensus layer or recovery service solely
to organize a bounded coding task.
