# Testing quality

Inspect tests and supplied results when correctness claims depend on them. Name
the observable contract each relevant assertion protects and ask whether a
plausible regression would fail it. Assess important success/failure paths,
boundaries, integration points and compatibility rather than fixed test counts,
coverage percentages, or cyclomatic-score-derived requirements.

Keep application logic real in the reasoning. Doubles should isolate the external
or nondeterministic boundary, not replace the behavior under test. A mock returning
its configured value proves little about application behavior; interaction checks
are useful when destination, payload, ordering or call count is the actual contract.
Check realistic success/error shapes, optional fields and downstream-consumed
metadata against the relevant API, not an invented fixture shape.

Inspect isolation, cleanup ownership, partial setup failure and shared mutable
state. Check clock/randomness/scheduling control and restoration of scoped patches.
Distinguish evidence of a product race from fixture contamination or environment
failures. Retries, sleeps, disabled assertions or blanket snapshot regeneration
can hide defects; require a concrete path and impact before reporting a finding.

For refactors, inspect whether baseline and characterization evidence cover the
affected contracts. For changes already implemented, preserve honest test-order
reporting; do not demand discarding work to reenact test-first. Unit success with
doubles does not establish filesystem/database/browser/remote compatibility.
Static configuration merits schema or parsed-contract checks, not incidental
spelling assertions; generators need generated-meaning and runtime-selection tests.

Report verification gaps with the exact unestablished behavior and proposed check.
Separate tests present, reported tests run and independently supplied execution
evidence, including command, revision and scope. Do not run tests, reproduce a
failure, edit assertions, regenerate snapshots or load an implementation workflow
from this lens. A passing suite proves only what its actual assertions exercise.
