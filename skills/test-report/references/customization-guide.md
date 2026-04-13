# Test Report Customization Guide

## Configuration Constants

Edit the top of `tests/generate_report.py` to customize:

```python
PROJECT_NAME = "MyApp"                           # Report title
PROJECT_SUBTITLE = "API Test Suite"              # Subtitle text
EXTRA_VERSIONS = {"FastAPI": "fastapi"}          # Package versions to show
REPORT_PATH = "docs/test-report.html"            # Output path (default: tests/report.html)
TEST_PATHS = ["tests/test_api.py"]               # Specific files (default: auto-discover)
```

---

## Collecting Test Outputs

### Setup in conftest.py

```python
REPORT_DATA = {"screenshots": {}, "outputs": {}}

@pytest.fixture(scope="session")
def report_data():
    return REPORT_DATA
```

### Store outputs in tests

```python
def test_create_user(self, report_data):
    result = api.create_user(name="Alice")
    assert result["id"]
    report_data["outputs"]["create_user"] = result  # key matches test name minus 'test_'
```

The output appears as expandable JSON in the report detail row.

---

## Embedding Screenshots

Store base64-encoded images in `report_data["screenshots"]`:

```python
import base64

def test_render_chart(self, report_data):
    chart_bytes = render_chart()
    report_data["screenshots"]["Revenue Chart"] = {
        "format": "png",  # or "svg", "jpg"
        "content": base64.b64encode(chart_bytes).decode(),
    }
```

These appear in the "Screenshots & Artifacts" gallery section.

---

## Custom Category Classification

By default, test class names are split from CamelCase into category labels:
- `TestAuthentication` -> "Authentication"
- `TestDatabaseOps` -> "Database Ops"
- `TestAPIEndpoints` -> "API Endpoints"

To override, edit `ReportCollector.classify_module()` in your project's copy:

```python
def classify_module(self, cls_name: str) -> str:
    custom = {
        "TestOARead": "Operational Analysis",
        "TestOAWrite": "Operational Analysis",
        "TestSARead": "System Analysis",
    }
    return custom.get(cls_name, super().classify_module(cls_name))
```

---

## Adding a Project Info Section

Add a custom HTML section after the summary grid. In `generate_html()`, build a section string and insert it:

```python
info_html = f"""
<div style="background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:1.5rem;margin:2rem 0">
    <h3>API Server</h3>
    <p style="color:var(--text-dim)">Base URL: <code>{base_url}</code></p>
    <p style="color:var(--text-dim)">Endpoints: <code>{endpoint_count}</code></p>
</div>
"""
```

Insert it in the HTML template between the summary grid and results section.

---

## Adding Custom Summary Cards

In the `generate_html()` function, add cards to the summary grid:

```html
<div class="summary-card">
    <div class="value" style="color:#55efc4">{custom_value}</div>
    <div class="label">Custom Metric</div>
</div>
```

---

## Custom Color Palette

Edit the `CATEGORY_COLORS` list in the script:

```python
CATEGORY_COLORS = [
    "#6c5ce7",  # Purple
    "#00cec9",  # Teal
    "#fd79a8",  # Pink
    "#f0932b",  # Orange
    "#74b9ff",  # Blue
    "#55efc4",  # Mint
    "#a29bfe",  # Lavender
    "#ff6b6b",  # Red
    "#ffeaa7",  # Yellow
    "#81ecec",  # Cyan
]
```

Colors are assigned by category index (alphabetical order).

---

## Non-Python Projects (Jest / Vitest)

The report generator is Python/pytest-specific. For JavaScript projects, adapt the pattern:

1. Run tests with JSON reporter: `jest --json --outputFile=results.json`
2. Write a Node.js script that reads `results.json` and generates the same HTML template
3. Use the same CSS/JS from the template — it's framework-agnostic
4. Map test suites to categories, test cases to rows
