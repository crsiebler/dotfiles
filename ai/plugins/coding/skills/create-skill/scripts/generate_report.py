"""Report helper adapted from aggregate_benchmark.py in Anthropic skill-creator.
Apache-2.0; see ../LICENSE.txt. Modified 2026-09-17: Markdown-only reports,
explicit missing metrics, observed sample counts, and source-located results.
"""
from aggregate_benchmark import inspect_grading, metric
from skill_io import SkillError


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ').replace('\r', ' ')


def generate_markdown(data):
    if not isinstance(data, dict) or not isinstance(data.get('runs'), list) or not data['runs']:
        raise SkillError(5, 'validation: benchmark must contain nonempty runs')
    lines = ['# Skill evaluation report', '',
             'Counts summarize recorded expectations; they do not establish visual quality.', '',
             '| Source | Configuration | Passed | Seconds | Tokens |',
             '| --- | --- | --- | --- | --- |']
    for row in data['runs']:
        if (not isinstance(row, dict) or not isinstance(row.get('source'), str)
                or row.get('configuration') not in ('with_skill', 'without_skill')):
            raise SkillError(5, 'validation: invalid benchmark run')
        results = row.get('result')
        if not isinstance(results, dict):
            raise SkillError(5, 'validation: missing run results')
        counts, _ = inspect_grading(dict(expectations=row.get('expectations'), summary=results))
        timing = metric(results.get('time_seconds'))
        tokens = metric(results.get('tokens'), integer=True)
        lines.append(f"| {cell(row['source'])} | {row['configuration']} | "
                     f"{counts['passed']}/{counts['total']} | "
                     f"{timing if timing is not None else 'unavailable'} | "
                     f"{tokens if tokens is not None else 'unavailable'} |")
    lines.extend(['', '## Evidence', ''])
    for row in data['runs']:
        lines.append(f"### {cell(row['source'])}")
        for item in row['expectations']:
            verdict = 'pass' if item['passed'] else 'fail'
            lines.append(f"- {verdict}: {cell(item['text'])} — {cell(item['evidence'])}")
        lines.append('')
    return '\n'.join(lines)
