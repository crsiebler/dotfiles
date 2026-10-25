# Requirements

Planning is instruction-only and needs no installed runner or Python package.
Use adequate native reads to inspect approved requirements and project commands.
Git is conditional for revision/branch evidence; no branch or worktree mutations
occur during planning. Resolve harness identity from trusted runtime context, not
installed executables. Dependency/model/runtime setup belongs to the selected
execution environment and is not a dependency of this skill. Still assess that
environment's required capabilities, approval prompts and manual prerequisites
under [execution readiness](execution-readiness.md); missing evidence blocks an
unattended-ready handoff, not the ability to draft a plan.

Do not install tools, source personal shell configuration, execute the plan, or
invoke another coding skill merely to prepare a plan. Report unavailable source
or verification commands as gaps. JSON output must parse using an existing native
parser or available interpreter; the planning workflow has no exact Python binary
name requirement. Existing Conda interpreters may be used without provisioning.
