# Native Codex task concurrency

This reference applies only to CodexGoalMarkdown. RalphJSON remains serial under
story-execution.md. Requirements, stable story IDs, acceptance, authorization,
review budgets and per-story delivery gates remain shared. Use native subagents;
add no scheduler, background controller, duplicate task store or nested Ralph loop.

## Team execution ownership

For authorized Codex parallel/team execution, discover and load run-agent-team
relative to its advertised installed base. That skill owns native role/model
preflight, bounded capacity and dispatch-before-wait procedure. This reference
remains canonical for dependency readiness, task worktrees and integration.
There is one dispatch owner and one integration owner, both the designated batch
lead. In delegated mode this is native multi-agent-coordinator, not its parent;
the parent supervises scope without another dispatch loop or canonical writes.
In supported parent-direct mode the parent is the sole lead and explicitly
reports adoption of the coordinator guidance. Never create recursive managers.
Workers follow bounded packets, not team entry routing. No mode waives native
reviewer availability, authorization or the shared delivery gates.

## Admission and ownership

The lead validates the complete dependency graph before dispatch: unique IDs,
known references, no self-dependency or cycle. Use Kahn-style readiness, ordering
ready stories by priority then document order. A predecessor is delivered only
after integration checks, its bounded review and authorized story commit pass.
A worker completion claim, local patch or isolated commit does not release it.
On resumption reconcile markers with delivery evidence; never infer success from
an idle worker. Preserve blocked candidates and consumed review passes.

Assign exactly one integration owner for the plan, integration branch/index,
completion markers, append-only progress and bounded memory. Workers return
changes and evidence, not competing journals or completion trackers. Record each
assignment in the existing plan/checkpoint, not a new registry:

- Stable story ID, scope, acceptance and exact verification commands.
- Absolute task worktree path, exact task branch and approved full base commit.
- Bounded repository-relative owned paths and agreed shared interface contracts.
- Private build/output roots; shared output owner and host resource coordination.
- Actual native worker identity and supported runtime/model/effort when observed.

Allocate shared source paths to one owner or serialize their changes. Directory
ownership includes descendants. Logical path checks are not symlink containment;
verify actual paths stay within the assigned worktree and authorized scope.

## Prepared worktrees and native paths

Before any worker writes, require an established clean committed baseline and
verify its recorded base, exact branch, absolute worktree and status. Reject
detached HEAD, main/master, branch mismatch and unrelated existing changes.
Before dispatch, verify each delivered predecessor's integration commit is an
ancestor of the assigned base, using `git merge-base --is-ancestor` in the assigned
repository. Record the prerequisite delivery revisions and ancestry evidence.
A pre-created worktree with a stale base is not eligible merely because its graph
dependencies are delivered. Under the lifecycle grant, prepare a suitable clean
task worktree/base containing those revisions; preserve any pending work rather
than silently resetting or rebasing it. Missing ancestry evidence blocks dispatch.
A clear launch may explicitly authorize necessary task branch/worktree creation
from approved existing commits. Otherwise reuse a suitable prepared worktree or
report the missing lifecycle grant. Never switch/reset the user's checkout,
silently copy dirty work or commit it to manufacture a baseline. Changes needed
from a dirty checkout require separate reconciliation, preservation and authority.
Do not create a worktree outside approved filesystem roots to bypass a denial.

Native child spawn does not bind cwd or create automatic child isolation. Supply
the absolute worktree in the worker packet; use explicit assigned paths for file
operations, command workdir and Git (`git -C <assigned-worktree>`). Verify root,
branch and status before writes and delivery. A task label is not path isolation.
Worktree creation/removal and local commits remain within their actual grants;
never remove a worktree holding pending or unrelated work merely to free capacity.

## Build resources and integration

Separate worktrees do not isolate host RAM/CPU, services, SDKs, caches or output
directories reached through absolute paths/symlinks. Prefer private build/output
roots per task. For shared mutable resources, designate one owner and use the
project's cross-worktree coordination mechanism before conflicting commands.
Record resource identity, command scope and release/cleanup responsibility.
If exclusive ownership or a required project mechanism cannot be established,
serialize the conflicting operations or report a blocker. Do not invent locks,
start services or enlarge permissions here. Optional hooks are guardrails, not
automatic cwd isolation or a replacement for resource coordination.

The lead integrates one bounded worker result into the integration worktree,
excluding unrelated work. Only that owner stages or mutates its index. Run the
required integration checks and existing staged review against the exact candidate
there, supplying its absolute root to the dedicated reviewer. Freeze that candidate
and conflicting resources through review and commit. Unrelated implementation in
separate task worktrees may continue; do not impose a blanket worker pause.

Record base/integrated revisions, checks, reviewer identity and consumed passes.
Changed integration content invalidates earlier checks/review; preserve the one
initial and at most one targeted same-session pass per attempt. Do not reset an
exhausted budget or replace the reviewer to obtain another pass. Dependencies
become ready only after verified integration delivery and the lead's marker update.
Missing native roles/tools or effective model selection are runtime prerequisites;
source instructions do not activate installed skills or model-routing settings.

## Optional deterministic reference

This Python 3.11+ standard-library example operates on normalized plan records in
memory. It validates readiness and logical ownership; it performs no dispatch,
Git operation, locking or persistence. No Python helper is required to plan: use
equivalent explicit graph checks when unavailable. This is not runtime enforcement.

```python
from graphlib import TopologicalSorter
from pathlib import PurePosixPath


def ready_story_ids(stories, delivered):
    ids = [story["id"] for story in stories]
    if any(not isinstance(key, str) or not key for key in ids):
        raise ValueError("nonempty story IDs required")
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate story ID")
    graph = {}
    for story in stories:
        deps = story["depends_on"]
        if not isinstance(deps, (list, tuple)):
            raise ValueError("dependency list required")
        if any(not isinstance(dep, str) or dep not in ids for dep in deps):
            raise ValueError("missing dependency reference")
        if len(deps) != len(set(deps)):
            raise ValueError("duplicate dependency reference")
        if type(story["priority"]) is not int:
            raise ValueError("integer priority required")
        graph[story["id"]] = tuple(deps)
    TopologicalSorter(graph).prepare()  # Kahn validation; cycles raise ValueError.
    finished = set(delivered)
    if not finished <= graph.keys():
        raise ValueError("unknown delivered story")
    if any(not set(graph[key]) <= finished for key in finished):
        raise ValueError("delivered dependencies require evidence reconciliation")
    remaining = {key: tuple(dep for dep in deps if dep not in finished)
                 for key, deps in graph.items() if key not in finished}
    sorter = TopologicalSorter(remaining)
    sorter.prepare()
    ready = set(sorter.get_ready())
    return [story["id"] for _, story in sorted(
        enumerate(stories), key=lambda item: (item[1]["priority"], item[0]))
        if story["id"] in ready]


def owned_paths_conflict(left, right):
    def canonical(raw):
        if not isinstance(raw, str) or raw in ("", "."):
            raise ValueError("explicit owned path required")
        path = PurePosixPath(raw)
        if (path.is_absolute() or ".." in path.parts or str(path) != raw
                or any(char in raw for char in "\\\x00*?[]")):
            raise ValueError("canonical relative owned path required")
        return path
    left, right = list(map(canonical, left)), list(map(canonical, right))
    if not left or not right:
        raise ValueError("nonempty ownership required")
    return any(a == b or a in b.parents or b in a.parents
               for a in left for b in right)
```
