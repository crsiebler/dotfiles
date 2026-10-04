# Run archival and workflow verification

Source changes implement deterministic, manifest-selected, flat run archives,
root progress.md journals, phase/story planning, scoped GitHub shipping, and a
GitHub issue/Projects assessment adapter. Existing installed skills, historical
archives and execution journals were not migrated. No real run was archived.

## Evidence

Checks used the existing Conda dotfiles environment: Python 3.11.16 and PyYAML
6.0.3. No dependencies were installed. The helper itself uses only Python's
standard library, Git and POSIX locks.

- Test-first evidence: archive_run_test.py's read-only preview assertion failed
  against the initial not_implemented scaffold, then passed after implementation.
- archive_run_test.py: 20 tests passed using real disposable project-local Git
  repositories. Coverage includes flat byte preservation, committed evidence,
  repeat invocation, optional memory/custom plan paths, earlier run history,
  staged/unrelated work, main/detached archival, runner locks/state/stop files,
  unsafe paths/collisions, malformed metadata/memory, changed archives, and injected
  copy/removal failures. An isolated skill copy executed from an unrelated working
  directory without modifying its resources. Partial cleanup is never retried automatically.
- story_execution_test.py: 11 passed; story_blocker_test.py: 6 passed;
  ralph_recovery_contract_test.py: 2 passed; coding_workflow_contract_test.py: 5 passed.
- agent_contract_test.py: 20 passed. bash tests/ralph_review_test.sh passed.
- make validate-ai with the Conda Python passed source structure/JSON/TOML checks.
  It did not start a harness or MCP server. macOS launcher cache warnings occurred
  under the sandbox despite the validator completing successfully.
- create-skill's check and validate commands passed for prepare-implementation,
  write-requirements, manage-changes and assess-work-item. This validates metadata
  and bounded trees, not model behavior.
- Local gh help confirmed the documented issue/project read flags and the default
  30-item/field limits. No account, issue or project was accessed.

The broader suite, before the last three archive cases were added, ran 278 tests
and exited 1 with 42 failures, 6 errors and 2 skips. Captured document test
failures/errors report unavailable Pillow, python-docx, python-pptx, ReportLab,
openpyxl, pypdf and XlsxWriter dependencies in this environment. The full suite
is not passing; tests were not weakened or skipped to hide those failures.

Command:

```sh
TMPDIR="$PWD/tests" PYTHONDONTWRITEBYTECODE=1 \
SKILL_TEST_PYTHON=/opt/anaconda3/envs/dotfiles/bin/python \
SKILL_TEST_YAML_PYTHON=/opt/anaconda3/envs/dotfiles/bin/python \
/opt/anaconda3/envs/dotfiles/bin/python -m unittest discover -s tests -p '*test*.py'
```

## PR #67 archive lock correction

The archive lock now lives at Git's per-worktree `archive-run.lock` metadata path.
It remains persistent and exclusively locked, but no longer leaves an untracked
file after the declared closeout files are committed. Linked worktrees resolve
independent locks; nonsymlink directory anchoring and regular-file checks remain.

Four new regression cases failed against the original helper, including the
exact `?? archive/.archive.lock` status after a scoped closeout commit. After the
fix, all 24 archive tests passed in the same Conda environment. They exercise
Ralph's actual clean-candidate check, held-lock refusal and release, linked
worktree isolation, symlink refusal, and a preview that creates no metadata lock.
`make validate-ai` and whitespace validation passed. No dependencies were installed.
The 59 Ralph Python regressions passed after a permission-authorized rerun.
Their initial sandboxed run reported two errors because `ps` was denied during
fixture child-process cleanup checks; no assertions were changed or skipped.

## Limits and activation

No standalone repository typecheck is configured. Ruff/Black are absent from
this Conda environment; no formatter was installed. Python syntax and actual
helper execution are covered by the scoped tests.

Scenario fixtures under tests/fixtures/workflow_skill_evals/ and the updated
implementation_planning_evals.json are unrun model-evaluation inputs. No live
with/without skill comparison, native execution/archival handoff, GitHub posting,
push, PR creation or installed-discovery check was performed. Static instructions
do not prove unattended orchestration or external integration behavior.

The helper validates recorded outcomes and committed task markers; it does not
rerun tests or authenticate review transcripts. Executors must record actual
observations. Ralph archival is invoked by its calling assistant after validated
supervisor exit; CLI-only Ralph has no automatic post-run hook.

Activation requires separately authorized skill/plugin and native Ralph role
refresh, followed by harness restart and fresh discovery. Source delivery does
not change installed copies. Older runs lacking a manifest/structured records
need scoped enrollment with real evidence; do not fabricate or automatically
move their journals. Keep historical archives and needed rollback copies intact.
