---
name: test-report
description: |
  Generate comprehensive tests and a professional single-file dark-themed HTML test report for any Python project. Use this skill when the user asks to "run tests and generate a report", "create a test report", "generate HTML test report", "test everything and show results", "run all tests with a report", "create test dashboard", "test summary HTML", "/test-report", or wants a visual overview of test results with screenshots. Also trigger when the user says "document test results", "generate test documentation", or "test report with screenshots".
---

# Test Report Generator

Create comprehensive tests and generate a professional, single-file, dark-themed HTML test report for any Python project. The report includes a summary dashboard, grouped results with pass/fail badges, expandable details, and optional screenshot gallery.

---

## Phase 1: Project Discovery

Before generating anything, explore the project thoroughly.

### Detect test framework
- Check `pyproject.toml` for `[tool.pytest]` section
- Check for `pytest.ini`, `setup.cfg [tool:pytest]`, `tox.ini`
- Look for test files: glob `**/test_*.py` and `**/*_test.py`
- If no Python test framework found, inform the user and suggest pytest

### Identify project metadata
- Extract project name from `pyproject.toml` `[project] name`, `setup.py`, `setup.cfg`, or root directory name
- Extract project description if available
- Find key packages to detect versions: look at imports in source files for `__version__` attributes

### Map existing tests
- Count test files and test functions/classes
- Identify test organization: by module, by feature, by class
- Check for existing `conftest.py` files and shared fixtures
- Check for existing report generators (avoid duplicating)

---

## Phase 2: Test Assessment & Generation

### If tests exist and have adequate coverage
- Skip to Phase 3
- Note: "adequate" means the user's code modules have corresponding test files

### If tests are missing or sparse
Generate comprehensive tests following these principles:

**Organization:**
- One test file per source module or logical grouping
- Use test classes to group related tests — the class name becomes the report category
- Name classes descriptively: `TestAuthentication`, `TestDatabaseOps`, `TestAPIEndpoints`, `TestModels`, etc.
- Keep `test_` prefix on all test functions

**Coverage:**
- Positive tests (happy path)
- Edge cases and boundary conditions
- Error handling (expected failures, invalid inputs)
- If the project has API endpoints, test each endpoint
- If the project has CLI tools, test each command

**Fixtures (conftest.py):**
- Create or update `tests/conftest.py` with shared fixtures
- Add the shared report data collector:
  ```python
  REPORT_DATA = {"screenshots": {}, "outputs": {}}

  @pytest.fixture(scope="session")
  def report_data():
      return REPORT_DATA
  ```
- Add project-specific fixtures (database connections, API clients, test data)

**Collecting outputs for the report:**
In tests where the output is worth showing in the report, have the test populate `report_data`:
```python
def test_some_feature(self, report_data):
    result = do_something()
    assert result["status"] == "ok"
    report_data["outputs"]["some_feature"] = result
```

For screenshots or rendered artifacts:
```python
report_data["screenshots"]["Feature Preview"] = {
    "format": "png",  # or "svg"
    "content": base64_encoded_string,
}
```

---

## Phase 3: Install Report Generator

### Copy the template script
Read the template from this skill's bundled script:
```
~/.claude/skills/test-report/scripts/generate_report.py
```

Copy it to the project's `tests/generate_report.py`.

### Adapt the configurable constants
Edit the top of the copied file:

```python
PROJECT_NAME = "ActualProjectName"         # From Phase 1 discovery
PROJECT_SUBTITLE = "Comprehensive Test Report"  # Or project description
EXTRA_VERSIONS = {
    "Display Name": "import_name",          # e.g., {"FastAPI": "fastapi"}
}
```

### Ensure conftest.py has REPORT_DATA
The report generator imports `REPORT_DATA` from `tests.conftest`. If conftest.py doesn't have it, add:

```python
REPORT_DATA = {"screenshots": {}, "outputs": {}}

@pytest.fixture(scope="session")
def report_data():
    return REPORT_DATA
```

### Verify test discoverability
- Ensure `tests/` directory is a package (has `__init__.py` if needed)
- Ensure test files follow `test_*.py` naming convention
- Run `python -m pytest tests/ --collect-only` to verify discovery

---

## Phase 4: Run Tests & Generate Report

Execute the report generator:
```bash
python tests/generate_report.py
```

### Handle common issues
- **Import errors**: fix missing dependencies or sys.path issues
- **Collection errors**: check test file naming, fixture availability
- **Test failures**: these are expected — the report captures them with details
- **Permission errors**: ensure write access to `tests/report.html`

The generator will:
1. Run all discovered tests via pytest with the custom plugin
2. Collect results: test name, category, status, duration, errors
3. Import `REPORT_DATA` for screenshots and outputs
4. Generate `tests/report.html` — a single self-contained HTML file

---

## Phase 5: Review & Share

### Open the report
The script auto-opens the browser. If it doesn't:
```bash
# Windows
start tests/report.html
# macOS
open tests/report.html
# Linux
xdg-open tests/report.html
```

### Report contents
The HTML report includes:
- **Header**: project name, timestamp, Python/package versions
- **Summary dashboard**: total/passed/failed/skipped counts, pass rate, duration
- **Results by category**: collapsible sections grouped by test class name, each test shows status badge, duration, and expandable output/error details
- **Screenshots gallery**: any base64-embedded images from `REPORT_DATA["screenshots"]`
- **Footer**: generation metadata

### Share
The report is a single `.html` file with all CSS/JS/images embedded. Share by:
- Email attachment
- Slack upload
- Git commit (e.g., `docs/test-report.html`)
- Static hosting

---

## Quick Reference

| What | Where |
|------|-------|
| Report generator template | `~/.claude/skills/test-report/scripts/generate_report.py` |
| Generated report | `tests/report.html` in the project |
| Test data collector | `REPORT_DATA` in `tests/conftest.py` |
| Customization guide | `~/.claude/skills/test-report/references/customization-guide.md` |
