# Architecture and maintainability

Use for changes to responsibilities, dependency direction, shared rules, control
flow or state that affect reasoning and change cost. Trace actual consumers and
reasons to change; do not demand a preferred pattern or a new layer.

Assess cohesion and information hiding: does a module own a coherent decision,
or must callers know its internal representation? Check coupling through calls,
shared state, schemas and deployment assumptions. Indirection may isolate a useful
boundary or spread knowledge unnecessarily; identify which with concrete examples.
Distinguish duplicated business knowledge (drift changes behavior) from accidental
syntax similarity (forced reuse may couple independently evolving policies).

Use several perspectives on complexity:

- Cyclomatic complexity describes independent control-flow paths under a tool's
  counting conventions. Language constructs and tools count differently. It does
  not measure all reasoning cost, prove understandability, or prescribe a
  sufficient test count. Report a score only when actually measured, with tool,
  configuration and scope; do not run a tool during this review.
- Cognitive difficulty includes nesting, nonlocal jumps and interacting conditions.
  Semantic difficulty includes domain assumptions and hidden contracts even in
  short code. State complexity includes legal transitions, temporal coupling and
  concurrency. Coupling adds reasoning across components. Describe observable
  examples rather than inventing numerical scores for these concerns.
- Respect project-configured thresholds and supplied check results. Distinguish
  a threshold breach from an evidenced defect. Arbitrary extraction can lower a
  metric while making state and dependencies harder to follow; do not recommend it
  merely to improve a number or reach a file-size target.

A one-implementation interface that isolates vendor errors and resource ownership
can reduce change cost. A single-export file may form an appropriate boundary.
Neither is automatically a defect. Conversely, name the concrete consumer churn,
conflicting invariants or fragile reasoning when a simplification is justified.
Preserve useful cohesive code, including naturally large declarative/generated data.

Report defects with triggering contracts and impact. Present optional simplification
separately with affected consumers, preserved behavior, alternatives/trade-offs,
verification and benefit/risk priority. Fewer lines or files alone is not evidence
of improvement. Do not refactor, run metrics, or create an architecture document
as an incidental part of this read-only lens.
