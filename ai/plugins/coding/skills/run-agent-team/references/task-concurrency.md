# Native task concurrency

This reference applies to the parallel Markdown checklist workflow.

## Team execution ownership

For authorized parallel/team execution, follow this bundle's team entry
contract. The main thread owns Git, worktree lifecycle, integration and canonical
task state and is the only dispatcher admitting and assigning work. Direct native
worker/reviewer calls require no custom coordinator or nested manager. Never run
competing loops, proxy-spawn for a child or delegate orchestration. Review,
authority and delivery gates remain unchanged. Release dependencies only after
verified main-thread integration delivery, never worker completion claims.

## Admission and ownership

The dispatcher validates the complete dependency graph before dispatch: unique IDs,
known references, no self-dependency or cycle. Use Kahn-style readiness, ordering
ready stories by priority then document order. A predecessor is delivered only
after integration checks, its bounded review and authorized story commit pass.
A worker completion claim, local patch or isolated commit does not release it.
On resumption reconcile markers with delivery evidence; never infer success from
an idle worker. Preserve blocked candidates and consumed review passes.

Assign exactly one integration owner for the plan, integration branch/index,
completion markers, append-only progress and bounded memory. Workers return
changes and evidence, not competing journals or completion trackers. Record each
assignment in the existing execution checkpoint, not a new registry or plan
narrative:

- Stable story ID, scope, acceptance and exact verification commands.
- Absolute task worktree path, exact task branch and approved full base commit.
- Bounded repository-relative owned paths and agreed shared interface contracts.
- Private build/output roots; shared output owner and host resource coordination.
- Actual native worker identity and supported runtime/model/effort when observed.
- Current phase: active implementation, awaiting integration, integrating,
  remediation or review; candidate/write owner and relevant check/reviewer session.

Allocate shared source paths to one owner or serialize their changes. Directory
ownership includes descendants. Logical path checks are not symlink containment;
verify actual paths stay within the assigned worktree and authorized scope.

## Capacity and queue control

Use min(requested worker limit, safely available native slots, model-use budget,
project resource capacity), targeting up to four implementation workers by default.
Use the runtime's documented session-capacity semantics and exposed inspection
controls. Count the main session only if the reported limit includes it; account
for advisors and retained sessions according to those semantics. Reserve one slot
for required review; an occupied reviewer already satisfies that reservation.
For a runtime counting all these sessions, four total slots allow two workers plus
main/reviewer; six allow four workers.

Record observed occupied capacity separately from uncertainty. Idle, completed or
pending-init labels alone prove neither occupation nor release. Reconcile stale or
uncertain results using supported inspection before admission or retry; never
duplicate a possibly-live owner. Use only supported lifecycle controls within
existing authority. Never terminate a live writer, discard pending work, or release
a reviewer required for its permitted same-session continuation. A finished initial
review is not evidence that its session can be released. If uncertainty persists,
record its concrete effect (for example, one unconfirmed slot prevents another
spawn) and continue work that is safely eligible without relying on that slot.

Set an explicit completed-candidate queue limit in the existing checkpoint:
default to one when only one worker is feasible, otherwise two. Lower it for tight
build/storage resources; explain the chosen value using worker capacity and project
resources. This small buffer feeds serial integration without admitting unlimited
unfinished delivery. Do not raise it merely to hide a backlog or fill slots.
Count all handed-off candidates outside the single integration/review lane,
including source-only results and candidates returned for worker remediation;
changing their phase does not erase queue pressure. Keep phase distinct from
qualification evidence. No new registry or background scheduler.

At or above the limit, stop admitting additional stories and prioritize
qualification, remediation and delivery in dependency/priority order, preserving
required review capacity. Already active isolated workers may finish; simultaneous
handoffs can temporarily exceed the limit. Preserve those results and drain the
queue below the limit before new admission, without terminating writers or
discarding work.
Consider imminent handoffs and actual integration/resource availability before
refilling. A free native slot alone is not a reason to start another story.

## Event checkpoints

Reassess ready tasks, exclusive ownership, observed capacity and uncertainty,
resource use and queue pressure when a worker hands off, a long-running check
yields control, remediation finishes, review finishes, or a story is committed.
Update only changed facts in the existing checkpoint; avoid repetitive bookkeeping.
Before waiting again, dispatch useful independent work if authorization, dependency
bases, capacity, resources and the queue limit permit. Reuse the running check's
handle and result; do not restart it, launch duplicate checks, busy poll or split
tiny work to manufacture occupancy. Use supported yielding checks and bounded
event waits where available. A long verification command alone does not justify
pausing unrelated isolated work. If the tool cannot yield, dispatch eligible work
before starting it and record the actual coordination limitation.

## Prepared worktrees and native paths

The main session may create task branches and worktrees only under an explicit scoped lifecycle grant.

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
silently copy dirty work or commit unrelated/pre-existing implementation to
manufacture a baseline. The initial approved-plan/checkpoint commit is permitted
under [commit authority](story-execution.md#authorization-and-prepared-branch);
finish it before admitting workers against the resulting clean committed base.
Other dirty-checkout changes require reconciliation, preservation and authority.
Do not create a worktree outside approved filesystem roots to bypass a denial.

Do not assume native child spawn binds cwd or creates isolation; inspect the
actual tool schema and verify the assigned root. Supply the absolute worktree
in the worker packet; use explicit assigned paths for file
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
Required native roles/tools and explicit user model constraints remain prerequisites.
Preferred models and unknown telemetry alone do not block; follow
[runtime selection](runtime-selection.md). Source instructions do not activate
installed skills or model-routing settings.

## Existing Python environment

The optional reference below uses only Python's standard library. Prefer the
already active Conda `python` when that is the host's configured interpreter;
validate `python -c 'import sys; assert sys.version_info >= (3, 11)'` before use.
An existing newer interpreter exposed only as `python3` is equally valid after
validation. Noninteractive commands need not source personal shell configuration.
Use the repository's existing Conda environment for its own checks; never create
an environment or install Python just to run this optional example.

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
