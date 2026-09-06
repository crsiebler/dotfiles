# pytest execution

Use the repository runner or Make target first. Inspect `pyproject.toml`,
`pytest.ini`, `conftest.py`, markers, environment, and test database fixtures.
Use the configured environment without installing dependencies implicitly.

Direct command shapes when pytest is installed:

```sh
pytest path/to/test_file.py
pytest path/to/test_file.py::test_name
pytest -k 'specific_behavior'
pytest
```

For failures, read the traceback, assertion diff, captured output, and fixture
setup/teardown. Distinguish collection errors from behavior failures; rerun the
smallest reproducer before widening scope. Respect markers for integration or
slow tests; report exclusions. Do not change environment or shared data blindly.

If `pytest-cov` is already available and configured:

```sh
pytest --cov --cov-report=term-missing
pytest --cov --cov-report=html
```

Request HTML only when useful; keep generated output project-local. Missing
coverage plugins are a limitation, not permission to install them. Inspect
uncovered branches for meaningful behavioral gaps rather than padding coverage.
