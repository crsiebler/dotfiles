"""Adapted from Anthropic skill-creator, Apache-2.0; see ../LICENSE.txt.
Modified 2026-09-17: validate evidence, retain unavailable metrics as null, bound
inputs, preserve source locations, and compute explicit with/without deltas.
"""
import math
import re
from datetime import datetime, timezone
from skill_io import SkillError, read_json, tree_files


def calculate_stats(values):
    values = [v for v in values if v is not None]
    if not values:
        return dict(count=0, mean=None, stddev=None, min=None, max=None)
    n = len(values)
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / (n - 1) if n > 1 else 0
    return dict(count=n, mean=round(mean, 4), stddev=round(math.sqrt(variance), 4),
                min=min(values), max=max(values))


def metric(value, *, integer=False):
    if value is None:
        return None
    if (type(value) not in (int, float) or not math.isfinite(value) or value < 0
            or integer and type(value) is not int):
        raise SkillError(5, 'validation: metrics must be finite nonnegative measurements')
    return value


def inspect_grading(data):
    if not isinstance(data, dict):
        raise SkillError(5, 'validation: grading must be an object')
    expectations = data.get('expectations')
    if not isinstance(expectations, list) or not expectations:
        raise SkillError(5, 'validation: nonempty expectations required')
    for row in expectations:
        if (not isinstance(row, dict) or type(row.get('passed')) is not bool
                or any(not isinstance(row.get(k), str) or not row[k].strip()
                       for k in ('text', 'evidence'))):
            raise SkillError(5, 'validation: each expectation needs text, boolean passed, and evidence')
    passed = sum(row['passed'] for row in expectations)
    result = dict(passed=passed, failed=len(expectations) - passed,
                  total=len(expectations), pass_rate=passed / len(expectations))
    if 'summary' in data:
        summary = data['summary']
        if not isinstance(summary, dict):
            raise SkillError(5, 'validation: summary must be an object')
        for key, actual in result.items():
            given = summary.get(key)
            if type(given) not in (int, float) or not math.isfinite(given):
                raise SkillError(5, 'validation: invalid grading summary')
            tolerance = 0.005 if key == 'pass_rate' else 0
            if abs(actual - given) > tolerance:
                raise SkillError(5, 'validation: grading summary disagrees with evidence')
    return result, expectations


def generate_benchmark(path):
    files = tree_files(path)
    search = path / 'runs' if (path / 'runs').is_dir() else path
    runs = []
    for file in files:
        if file.name != 'grading.json':
            continue
        relative = file.relative_to(search) if file.is_relative_to(search) else None
        if relative is None or len(relative.parts) != 4:
            raise SkillError(5, 'validation: unexpected grading location')
        evaluation, config, run, _ = relative.parts
        if (not re.fullmatch(r'eval-[0-9]+', evaluation)
                or config not in ('with_skill', 'without_skill')
                or not re.fullmatch(r'run-[0-9]+', run)):
            raise SkillError(5, 'validation: unsupported evaluation/run layout')
        data = read_json(file)
        result, expectations = inspect_grading(data)
        timing_path = file.parent / 'timing.json'
        timing = read_json(timing_path) if timing_path.exists() else data.get('timing', {})
        metrics = data.get('execution_metrics', {})
        if not isinstance(timing, dict) or not isinstance(metrics, dict):
            raise SkillError(5, 'validation: timing and metrics must be objects')
        result.update(time_seconds=metric(timing.get('total_duration_seconds')),
                      tokens=metric(timing.get('total_tokens'), integer=True),
                      tool_calls=metric(metrics.get('total_tool_calls'), integer=True),
                      errors=metric(metrics.get('errors_encountered'), integer=True))
        runs.append(dict(eval_id=int(evaluation[5:]), configuration=config,
                         run_number=int(run[4:]), source=file.relative_to(path).as_posix(),
                         result=result, expectations=expectations, notes=[]))
    # A run directory without grading is not a successful or silently omitted run.
    expected_dirs = list(search.glob('eval-*/*/run-*'))
    if not runs or any(not (p / 'grading.json').is_file() for p in expected_dirs):
        raise SkillError(5, 'validation: no runs or incomplete run evidence')
    identities = {(r['eval_id'], r['configuration'], r['run_number']) for r in runs}
    if len(identities) != len(runs):
        raise SkillError(5, 'validation: duplicate run identity')
    summary = {}
    for config in ('with_skill', 'without_skill'):
        selected = [r['result'] for r in runs if r['configuration'] == config]
        summary[config] = {key: calculate_stats([r[key] for r in selected])
                           for key in ('pass_rate', 'time_seconds', 'tokens')}
    summary['delta'] = {}
    for key in ('pass_rate', 'time_seconds', 'tokens'):
        a = summary['with_skill'][key]['mean']
        b = summary['without_skill'][key]['mean']
        summary['delta'][key] = a - b if a is not None and b is not None else None
    return dict(metadata=dict(timestamp=datetime.now(timezone.utc).isoformat(),
                              executor_model=None, analyzer_model=None,
                              evals_run=sorted({r['eval_id'] for r in runs}),
                              run_count=len(runs)),
                runs=runs, run_summary=summary,
                notes=['Unavailable metrics are null; sample counts describe measured runs only.'])
