# JSON Schemas

Modified 2026-09-17 from Anthropic skill-creator (Apache-2.0): project-owned
locations, optional telemetry, and portable benchmark contract; see provenance.md.

This document preserves upstream evaluation, comparison, and analysis schemas.
The portable helper differences below take precedence over illustrative examples.
All files belong in a project workspace, not the installed skill.

## Portable benchmark differences

The benchmark/report helpers implement the contract in [authoring.md](authoring.md).
They retain runs, configuration, result, expectations, notes, and run_summary.
Optional metrics and their statistics are null when unavailable; each statistic
includes its actual measured count. Delta values are numbers or null. Metadata
contains observed run_count and evals_run rather than a fabricated fixed count.
Model fields are null unless known; generation time is recorded. Each run includes
its source-relative grading location. Grading summary, when present, must agree
with expectations. A rounded pass_rate tolerance of 0.005 is accepted.
Other schemas guide human/assistant evaluation; helpers do not run models or
validate every optional comparison/analysis field. The HTML viewer is not shipped.

---

## evals.json

Defines the evals for a skill. Located at `evals/evals.json` within the project evaluation workspace.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's example prompt",
      "expected_output": "Description of expected result",
      "files": ["evals/files/sample1.pdf"],
      "expectations": [
        "The output includes X",
        "The skill used script Y"
      ]
    }
  ]
}
```

**Fields:**
- `skill_name`: Name matching the skill's frontmatter
- `evals[].id`: Unique integer identifier
- `evals[].prompt`: The task to execute
- `evals[].expected_output`: Human-readable description of success
- `evals[].files`: Optional list of input file paths (relative to project evaluation workspace)
- `evals[].expectations`: List of verifiable statements

---

## history.json

Tracks version progression in Improve mode. Located at workspace root.

```json
{
  "started_at": "2026-01-15T10:30:00Z",
  "skill_name": "pdf",
  "current_best": "v2",
  "iterations": [
    {
      "version": "v0",
      "parent": null,
      "expectation_pass_rate": 0.65,
      "grading_result": "baseline",
      "is_current_best": false
    },
    {
      "version": "v1",
      "parent": "v0",
      "expectation_pass_rate": 0.75,
      "grading_result": "won",
      "is_current_best": false
    },
    {
      "version": "v2",
      "parent": "v1",
      "expectation_pass_rate": 0.85,
      "grading_result": "won",
      "is_current_best": true
    }
  ]
}
```

**Fields:**
- `started_at`: ISO timestamp of when improvement started
- `skill_name`: Name of the skill being improved
- `current_best`: Version identifier of the best performer
- `iterations[].version`: Version identifier (v0, v1, ...)
- `iterations[].parent`: Parent version this was derived from
- `iterations[].expectation_pass_rate`: Pass rate from grading
- `iterations[].grading_result`: "baseline", "won", "lost", or "tie"
- `iterations[].is_current_best`: Whether this is the current best version

---

## grading.json

Output from the grader agent. Located at `<run-dir>/grading.json`.

```json
{
  "expectations": [
    {
      "text": "The output includes the name 'John Smith'",
      "passed": true,
      "evidence": "Found in transcript Step 3: 'Extracted names: John Smith, Sarah Johnson'"
    },
    {
      "text": "The spreadsheet has a SUM formula in cell B10",
      "passed": false,
      "evidence": "No spreadsheet was created. The output was a text file."
    }
  ],
  "summary": {
    "passed": 1,
    "failed": 1,
    "total": 2,
    "pass_rate": 0.5
  },
  "execution_metrics": {
    "tool_calls": {
      "Read": 5,
      "Write": 2,
      "Bash": 8
    },
    "total_tool_calls": 15,
    "total_steps": 6,
    "errors_encountered": 0,
    "output_chars": 12450,
    "transcript_chars": 3200
  },
  "timing": {
    "executor_duration_seconds": 165.0,
    "grader_duration_seconds": 26.0,
    "total_duration_seconds": 191.0
  },
  "claims": [
    {
      "claim": "The form has 12 fillable fields",
      "type": "factual",
      "verified": true,
      "evidence": "Counted 12 fields in field_info.json"
    }
  ],
  "user_notes_summary": {
    "uncertainties": [
      "Used 2023 data, may be stale"
    ],
    "needs_review": [],
    "workarounds": [
      "Fell back to text overlay for non-fillable fields"
    ]
  },
  "eval_feedback": {
    "suggestions": [
      {
        "assertion": "The output includes the name 'John Smith'",
        "reason": "A hallucinated document that mentions the name would also pass"
      }
    ],
    "overall": "Assertions check presence but not correctness."
  }
}
```

**Fields:**
- `expectations[]`: Graded expectations with evidence
- `summary`: Aggregate pass/fail counts
- `execution_metrics`: Tool usage and output size (from executor's metrics.json)
- `timing`: Wall clock timing (from timing.json)
- `claims`: Extracted and verified claims from the output
- `user_notes_summary`: Issues flagged by the executor
- `eval_feedback`: (optional) Improvement suggestions for the evals, only present when the grader identifies issues worth raising

---

## metrics.json

Output from the executor agent. Located at `<run-dir>/outputs/metrics.json`.

```json
{
  "tool_calls": {
    "Read": 5,
    "Write": 2,
    "Bash": 8,
    "Edit": 1,
    "Glob": 2,
    "Grep": 0
  },
  "total_tool_calls": 18,
  "total_steps": 6,
  "files_created": ["filled_form.pdf", "field_values.json"],
  "errors_encountered": 0,
  "output_chars": 12450,
  "transcript_chars": 3200
}
```

**Fields:**
- `tool_calls`: Count per tool type
- `total_tool_calls`: Sum of all tool calls
- `total_steps`: Number of major execution steps
- `files_created`: List of output files created
- `errors_encountered`: Number of errors during execution
- `output_chars`: Total character count of output files
- `transcript_chars`: Character count of transcript

---

## timing.json

Wall clock timing for a run. Located at `<run-dir>/timing.json`.

**How to capture:** Record only metrics the current runtime actually supplies.
Delegation and token telemetry are optional. Omit unavailable values or use null;
never infer tokens from character counts. Save timing alongside the actual run.

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3,
  "executor_start": "2026-01-15T10:30:00Z",
  "executor_end": "2026-01-15T10:32:45Z",
  "executor_duration_seconds": 165.0,
  "grader_start": "2026-01-15T10:32:46Z",
  "grader_end": "2026-01-15T10:33:12Z",
  "grader_duration_seconds": 26.0
}
```

---

## benchmark.json

Supported portable benchmark example. Generated from the grading example above
under `eval-1/with_skill/run-1/grading.json`. Values are illustrative, not measurements
from an actual model evaluation. This is the current helper contract; no historical
HTML viewer schema is used by this distribution.

```json
{
  "metadata": {
    "timestamp": "2026-01-15T10:30:00+00:00",
    "executor_model": null,
    "analyzer_model": null,
    "evals_run": [
      1
    ],
    "run_count": 1
  },
  "runs": [
    {
      "eval_id": 1,
      "configuration": "with_skill",
      "run_number": 1,
      "source": "eval-1/with_skill/run-1/grading.json",
      "result": {
        "passed": 1,
        "failed": 1,
        "total": 2,
        "pass_rate": 0.5,
        "time_seconds": 191.0,
        "tokens": null,
        "tool_calls": 15,
        "errors": 0
      },
      "expectations": [
        {
          "text": "The output includes the name 'John Smith'",
          "passed": true,
          "evidence": "Found in transcript Step 3: 'Extracted names: John Smith, Sarah Johnson'"
        },
        {
          "text": "The spreadsheet has a SUM formula in cell B10",
          "passed": false,
          "evidence": "No spreadsheet was created. The output was a text file."
        }
      ],
      "notes": []
    }
  ],
  "run_summary": {
    "with_skill": {
      "pass_rate": {
        "count": 1,
        "mean": 0.5,
        "stddev": 0.0,
        "min": 0.5,
        "max": 0.5
      },
      "time_seconds": {
        "count": 1,
        "mean": 191.0,
        "stddev": 0.0,
        "min": 191.0,
        "max": 191.0
      },
      "tokens": {
        "count": 0,
        "mean": null,
        "stddev": null,
        "min": null,
        "max": null
      }
    },
    "without_skill": {
      "pass_rate": {
        "count": 0,
        "mean": null,
        "stddev": null,
        "min": null,
        "max": null
      },
      "time_seconds": {
        "count": 0,
        "mean": null,
        "stddev": null,
        "min": null,
        "max": null
      },
      "tokens": {
        "count": 0,
        "mean": null,
        "stddev": null,
        "min": null,
        "max": null
      }
    },
    "delta": {
      "pass_rate": null,
      "time_seconds": null,
      "tokens": null
    }
  },
  "notes": [
    "Illustrative data only, not a recorded evaluation.",
    "Unavailable token telemetry remains null."
  ]
}
```

**Fields:**
- `metadata`: generation timestamp, known model names or null, observed eval IDs,
  and actual total run_count. No assumed runs-per-configuration value.
- `runs[]`: numeric eval_id/run_number, explicit configuration (`with_skill` or
  `without_skill`), project-workspace-relative source, result counts/metrics,
  evidence-bearing expectations, and notes.
- `result`: passed/failed/total/pass_rate derived from expectations. Optional
  time_seconds/tokens/tool_calls/errors are numbers or null; characters are separate.
- `run_summary`: per-configuration statistics for pass_rate/time_seconds/tokens.
  Each has count/mean/stddev/min/max; no measured values means count 0 and null stats.
- `delta`: numeric with_skill minus without_skill means, or null when either mean
  is unavailable. Compare measured sample counts before interpreting these deltas.
- `notes`: explanatory observations, never fabricated run outcomes.

The report helper requires source/configuration/result/expectations for every run
and verifies counts against evidence. It deliberately refuses missing source
locations and inconsistent example summaries. Use the benchmark command rather
than manually inventing metric values.

---

## comparison.json

Output from blind comparator. Located at `<grading-dir>/comparison-N.json`.

```json
{
  "winner": "A",
  "reasoning": "Output A provides a complete solution with proper formatting and all required fields. Output B is missing the date field and has formatting inconsistencies.",
  "rubric": {
    "A": {
      "content": {
        "correctness": 5,
        "completeness": 5,
        "accuracy": 4
      },
      "structure": {
        "organization": 4,
        "formatting": 5,
        "usability": 4
      },
      "content_score": 4.7,
      "structure_score": 4.3,
      "overall_score": 9.0
    },
    "B": {
      "content": {
        "correctness": 3,
        "completeness": 2,
        "accuracy": 3
      },
      "structure": {
        "organization": 3,
        "formatting": 2,
        "usability": 3
      },
      "content_score": 2.7,
      "structure_score": 2.7,
      "overall_score": 5.4
    }
  },
  "output_quality": {
    "A": {
      "score": 9,
      "strengths": ["Complete solution", "Well-formatted", "All fields present"],
      "weaknesses": ["Minor style inconsistency in header"]
    },
    "B": {
      "score": 5,
      "strengths": ["Readable output", "Correct basic structure"],
      "weaknesses": ["Missing date field", "Formatting inconsistencies", "Partial data extraction"]
    }
  },
  "expectation_results": {
    "A": {
      "passed": 4,
      "total": 5,
      "pass_rate": 0.80,
      "details": [
        {"text": "Output includes name", "passed": true}
      ]
    },
    "B": {
      "passed": 3,
      "total": 5,
      "pass_rate": 0.60,
      "details": [
        {"text": "Output includes name", "passed": true}
      ]
    }
  }
}
```

---

## analysis.json

Output from post-hoc analyzer. Located at `<grading-dir>/analysis.json`.

```json
{
  "comparison_summary": {
    "winner": "A",
    "winner_skill": "path/to/winner/skill",
    "loser_skill": "path/to/loser/skill",
    "comparator_reasoning": "Brief summary of why comparator chose winner"
  },
  "winner_strengths": [
    "Clear step-by-step instructions for handling multi-page documents",
    "Included validation script that caught formatting errors"
  ],
  "loser_weaknesses": [
    "Vague instruction 'process the document appropriately' led to inconsistent behavior",
    "No script for validation, agent had to improvise"
  ],
  "instruction_following": {
    "winner": {
      "score": 9,
      "issues": ["Minor: skipped optional logging step"]
    },
    "loser": {
      "score": 6,
      "issues": [
        "Did not use the skill's formatting template",
        "Invented own approach instead of following step 3"
      ]
    }
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "Replace 'process the document appropriately' with explicit steps",
      "expected_impact": "Would eliminate ambiguity that caused inconsistent behavior"
    }
  ],
  "transcript_insights": {
    "winner_execution_pattern": "Read skill -> Followed 5-step process -> Used validation script",
    "loser_execution_pattern": "Read skill -> Unclear on approach -> Tried 3 different methods"
  }
}
```
