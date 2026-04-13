#!/usr/bin/env python3
"""Run all tests and generate a professional HTML test report.

Usage:
    python tests/generate_report.py

Outputs:
    tests/report.html — single-file, dark-themed, shareable test report

Configuration:
    Edit the constants below to customize for your project.
"""

from __future__ import annotations

import datetime
import html
import json
import os
import platform
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

import pytest  # noqa: E402


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONFIGURATION — Edit these for your project
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROJECT_NAME = "Project"
PROJECT_SUBTITLE = "Comprehensive Test Report"

# Extra package versions to display in the report header.
# Format: {"Display Name": "import_name"}
# Example: {"FastAPI": "fastapi", "SQLAlchemy": "sqlalchemy"}
EXTRA_VERSIONS: dict[str, str] = {}

# Output path for the report (relative to ROOT). None = tests/report.html
REPORT_PATH: str | None = None

# Test file paths to run. None = auto-discover test_*.py in tests/
TEST_PATHS: list[str] | None = None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Color palette for auto-assignment to categories
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CATEGORY_COLORS = [
    "#6c5ce7", "#00cec9", "#fd79a8", "#f0932b", "#74b9ff",
    "#55efc4", "#a29bfe", "#ff6b6b", "#ffeaa7", "#81ecec",
]


# ── Data collection ──────────────────────────────────────────────────


@dataclass
class TestResult:
    name: str
    module: str
    status: str  # passed, failed, skipped, error
    duration: float
    error_msg: str = ""
    tool_name: str = ""


@dataclass
class ReportCollector:
    results: list[TestResult] = field(default_factory=list)
    screenshots: dict = field(default_factory=dict)
    outputs: dict = field(default_factory=dict)
    start_time: float = 0.0
    end_time: float = 0.0

    def classify_module(self, cls_name: str) -> str:
        """Convert TestClassName into a human-readable category name.

        Examples:
            TestAuthentication -> Authentication
            TestDatabaseOps -> Database Ops
            TestAPIEndpoints -> API Endpoints
            Unknown -> Uncategorized
        """
        if not cls_name or cls_name == "Unknown":
            return "Uncategorized"
        name = cls_name
        if name.startswith("Test"):
            name = name[4:]
        # Split CamelCase: "DatabaseOps" -> "Database Ops"
        name = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name)
        # Split acronym boundaries: "APIEndpoints" -> "API Endpoints"
        name = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", name)
        return name.strip() or "Uncategorized"

    def tool_from_test(self, test_name: str) -> str:
        """Extract display name from test name."""
        name = test_name
        if name.startswith("test_"):
            name = name[5:]
        return name


class PytestPlugin:
    """Custom pytest plugin that collects test results."""

    def __init__(self, collector: ReportCollector):
        self.collector = collector

    def pytest_sessionstart(self, session):
        self.collector.start_time = time.time()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        report = outcome.get_result()

        if report.when == "call":
            cls_name = item.cls.__name__ if item.cls else "Unknown"
            status = report.outcome  # passed, failed, skipped
            error_msg = ""
            if report.failed:
                error_msg = str(report.longrepr) if report.longrepr else "Unknown error"
            elif report.skipped:
                error_msg = str(report.longrepr) if report.longrepr else "Skipped"

            result = TestResult(
                name=item.name,
                module=self.collector.classify_module(cls_name),
                status=status,
                duration=report.duration,
                error_msg=error_msg,
                tool_name=self.collector.tool_from_test(item.name),
            )
            self.collector.results.append(result)

    def pytest_sessionfinish(self, session, exitstatus):
        """Capture report_data from conftest module-level dict after tests."""
        self.collector.end_time = time.time()
        try:
            from tests.conftest import REPORT_DATA
            self.collector.screenshots = REPORT_DATA.get("screenshots", {})
            self.collector.outputs = REPORT_DATA.get("outputs", {})
        except (ImportError, AttributeError):
            pass


# ── HTML Report Generation ───────────────────────────────────────────


def _get_versions() -> dict[str, str]:
    versions = {
        "python": platform.python_version(),
        "platform": f"{platform.system()} {platform.release()}",
        "pytest": pytest.__version__,
    }
    for display_name, import_name in EXTRA_VERSIONS.items():
        try:
            mod = __import__(import_name)
            versions[display_name] = getattr(mod, "__version__", "unknown")
        except ImportError:
            versions[display_name] = "not installed"
    return versions


def _status_badge(status: str) -> str:
    colors = {
        "passed": ("#00cec9", "PASS"),
        "failed": ("#ff6b6b", "FAIL"),
        "skipped": ("#f0932b", "SKIP"),
        "error": ("#ff6b6b", "ERROR"),
    }
    color, label = colors.get(status, ("#888", status.upper()))
    return f'<span class="badge" style="background:{color}">{label}</span>'


def _escape(text: str) -> str:
    return html.escape(str(text))


def _abbreviate(name: str) -> str:
    """Generate a 2-3 char abbreviation from a category name."""
    words = name.split()
    if len(words) == 1:
        return name[:2].upper()
    return "".join(w[0].upper() for w in words[:3])


def _discover_test_files() -> list[str]:
    """Auto-discover test files in the tests/ directory."""
    test_dir = ROOT / "tests"
    if not test_dir.exists():
        test_dir = ROOT
    files = sorted(
        str(f)
        for f in test_dir.rglob("test_*.py")
        if "generate_report" not in f.name
    )
    return files


def generate_html(collector: ReportCollector) -> str:
    versions = _get_versions()
    total = len(collector.results)
    passed = sum(1 for r in collector.results if r.status == "passed")
    failed = sum(1 for r in collector.results if r.status == "failed")
    skipped = sum(1 for r in collector.results if r.status == "skipped")
    duration = collector.end_time - collector.start_time
    pass_rate = (passed / total * 100) if total > 0 else 0
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build version metadata
    meta_items = "".join(
        f'<span class="meta-item">{_escape(k)}: <code>{_escape(v)}</code></span>'
        for k, v in versions.items()
    )

    # Group results by module
    modules: dict[str, list[TestResult]] = {}
    for r in collector.results:
        modules.setdefault(r.module, []).append(r)

    # Sort categories alphabetically
    module_order = sorted(modules.keys())

    # Assign colors from palette
    module_colors = {}
    for i, mod_name in enumerate(module_order):
        module_colors[mod_name] = CATEGORY_COLORS[i % len(CATEGORY_COLORS)]

    # Build results table per module
    results_html = ""
    for mod_name in module_order:
        tests = modules[mod_name]
        color = module_colors[mod_name]
        abbr = _abbreviate(mod_name)
        mod_passed = sum(1 for t in tests if t.status == "passed")
        mod_total = len(tests)
        results_html += f"""
        <div class="module-section">
            <button class="module-header" onclick="toggleModule(this)">
                <span class="module-badge" style="background:{color}">{abbr}</span>
                <span class="module-name">{_escape(mod_name)}</span>
                <span class="module-stats">{mod_passed}/{mod_total} passed</span>
                <span class="chevron">&#9660;</span>
            </button>
            <div class="module-body">
                <table class="results-table">
                    <thead>
                        <tr>
                            <th>Test</th>
                            <th>Status</th>
                            <th>Duration</th>
                            <th>Details</th>
                        </tr>
                    </thead>
                    <tbody>"""

        for t in tests:
            detail_id = f"detail-{hash(t.name) % 100000}"
            tool_output = collector.outputs.get(t.tool_name, {})
            output_json = json.dumps(tool_output, indent=2, default=str)[:2000] if tool_output else ""
            error_html = ""
            if t.error_msg:
                error_html = f'<pre class="error-text">{_escape(t.error_msg[:1000])}</pre>'
            elif output_json:
                error_html = f'<pre class="output-text">{_escape(output_json)}</pre>'

            has_detail = bool(error_html)
            detail_btn = (
                f'<button class="detail-btn" onclick="toggleDetail(\'{detail_id}\')">Show</button>'
                if has_detail
                else '<span class="no-detail">\u2014</span>'
            )

            results_html += f"""
                        <tr>
                            <td class="tool-name">{_escape(t.tool_name)}</td>
                            <td>{_status_badge(t.status)}</td>
                            <td class="duration">{t.duration:.3f}s</td>
                            <td>{detail_btn}</td>
                        </tr>"""
            if has_detail:
                results_html += f"""
                        <tr id="{detail_id}" class="detail-row" style="display:none">
                            <td colspan="4">{error_html}</td>
                        </tr>"""

        results_html += """
                    </tbody>
                </table>
            </div>
        </div>"""

    # Build screenshot gallery
    screenshot_html = ""
    if collector.screenshots:
        screenshot_html = '<div class="diagram-gallery">'
        for name, data in collector.screenshots.items():
            fmt = data.get("format", "png")
            content = data.get("content", "")
            mime = "image/svg+xml" if fmt == "svg" else f"image/{fmt}"
            screenshot_html += f"""
            <div class="diagram-card">
                <img src="data:{mime};base64,{content}" alt="{_escape(name)}" loading="lazy">
                <div class="diagram-caption">{_escape(name)}</div>
            </div>"""
        screenshot_html += "</div>"

    screenshot_section = ""
    if screenshot_html:
        screenshot_section = f"""
    <h2 class="section-title">Screenshots &amp; Artifacts</h2>
    {screenshot_html}"""

    # Assemble full HTML
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{_escape(PROJECT_NAME)} Test Report</title>
<style>
:root {{
    --bg: #0a0a0f;
    --bg-card: #12121a;
    --bg-hover: #1a1a2e;
    --text: #e2e2e8;
    --text-dim: #8888a0;
    --accent: #6c5ce7;
    --green: #00cec9;
    --red: #ff6b6b;
    --orange: #f0932b;
    --pink: #fd79a8;
    --blue: #74b9ff;
    --border: #2a2a3e;
    --radius: 12px;
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
}}

.container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}

/* Header */
.header {{
    text-align: center;
    padding: 3rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}}
.header h1 {{
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--green));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}}
.header .subtitle {{
    color: var(--text-dim);
    font-size: 0.95rem;
}}
.meta-row {{
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-top: 1rem;
    flex-wrap: wrap;
}}
.meta-item {{
    color: var(--text-dim);
    font-size: 0.85rem;
}}
.meta-item code {{
    background: var(--bg-card);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.8rem;
    color: var(--text);
}}

/* Summary Cards */
.summary-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}}
.summary-card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    text-align: center;
}}
.summary-card .value {{
    font-size: 2.5rem;
    font-weight: 800;
    line-height: 1;
}}
.summary-card .label {{
    font-size: 0.85rem;
    color: var(--text-dim);
    margin-top: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

/* Section Headers */
.section-title {{
    font-size: 1.4rem;
    font-weight: 700;
    margin: 2.5rem 0 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--accent);
    display: inline-block;
}}

/* Module Sections */
.module-section {{
    margin-bottom: 0.75rem;
}}
.module-header {{
    width: 100%;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.25rem;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    cursor: pointer;
    color: var(--text);
    font-size: 1rem;
    transition: background 0.2s;
}}
.module-header:hover {{ background: var(--bg-hover); }}
.module-badge {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px; height: 36px;
    border-radius: 8px;
    font-weight: 800;
    font-size: 0.75rem;
    color: #fff;
    flex-shrink: 0;
}}
.module-name {{ font-weight: 600; flex: 1; text-align: left; }}
.module-stats {{ color: var(--text-dim); font-size: 0.85rem; }}
.chevron {{ transition: transform 0.3s; font-size: 0.7rem; color: var(--text-dim); }}
.module-header.open .chevron {{ transform: rotate(180deg); }}
.module-body {{
    display: none;
    padding: 0.5rem 0;
}}
.module-header.open + .module-body {{ display: block; }}

/* Results Table */
.results-table {{
    width: 100%;
    border-collapse: collapse;
    background: var(--bg-card);
    border-radius: var(--radius);
    overflow: hidden;
    border: 1px solid var(--border);
}}
.results-table th {{
    text-align: left;
    padding: 0.75rem 1rem;
    background: var(--bg);
    color: var(--text-dim);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
.results-table td {{
    padding: 0.6rem 1rem;
    border-top: 1px solid var(--border);
    font-size: 0.9rem;
}}
.tool-name {{ font-family: 'SF Mono', 'Consolas', monospace; font-size: 0.85rem; }}
.duration {{ color: var(--text-dim); font-size: 0.85rem; }}
.badge {{
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
    color: #fff;
    letter-spacing: 0.5px;
}}
.detail-btn {{
    background: var(--bg);
    border: 1px solid var(--border);
    color: var(--text-dim);
    padding: 3px 10px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.75rem;
    transition: all 0.2s;
}}
.detail-btn:hover {{ background: var(--bg-hover); color: var(--text); }}
.no-detail {{ color: var(--border); }}
.detail-row td {{
    padding: 0;
}}
.error-text, .output-text {{
    background: var(--bg);
    padding: 1rem;
    font-family: 'SF Mono', 'Consolas', monospace;
    font-size: 0.75rem;
    line-height: 1.5;
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-all;
    max-height: 300px;
    overflow-y: auto;
    margin: 0.5rem 1rem;
    border-radius: 8px;
}}
.error-text {{ color: var(--red); }}
.output-text {{ color: var(--green); }}

/* Screenshot Gallery */
.diagram-gallery {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 1.5rem;
    margin: 1.5rem 0;
}}
.diagram-card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
}}
.diagram-card img {{
    width: 100%;
    max-height: 500px;
    object-fit: contain;
    background: #fff;
    padding: 1rem;
}}
.diagram-caption {{
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
    color: var(--text-dim);
    border-top: 1px solid var(--border);
}}

/* Footer */
.footer {{
    text-align: center;
    padding: 2rem 0;
    margin-top: 3rem;
    border-top: 1px solid var(--border);
    color: var(--text-dim);
    font-size: 0.8rem;
}}

@media (max-width: 768px) {{
    .container {{ padding: 1rem; }}
    .diagram-gallery {{ grid-template-columns: 1fr; }}
    .summary-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .header h1 {{ font-size: 1.8rem; }}
}}
</style>
</head>
<body>
<div class="container">

    <!-- Header -->
    <div class="header">
        <h1>{_escape(PROJECT_NAME)} Test Report</h1>
        <p class="subtitle">{_escape(PROJECT_SUBTITLE)}</p>
        <div class="meta-row">
            <span class="meta-item">Generated: <code>{timestamp}</code></span>
            {meta_items}
        </div>
    </div>

    <!-- Summary -->
    <div class="summary-grid">
        <div class="summary-card">
            <div class="value" style="color:var(--text)">{total}</div>
            <div class="label">Total Tests</div>
        </div>
        <div class="summary-card">
            <div class="value" style="color:var(--green)">{passed}</div>
            <div class="label">Passed</div>
        </div>
        <div class="summary-card">
            <div class="value" style="color:var(--red)">{failed}</div>
            <div class="label">Failed</div>
        </div>
        <div class="summary-card">
            <div class="value" style="color:var(--orange)">{skipped}</div>
            <div class="label">Skipped</div>
        </div>
        <div class="summary-card">
            <div class="value" style="color:var(--accent)">{pass_rate:.0f}%</div>
            <div class="label">Pass Rate</div>
        </div>
        <div class="summary-card">
            <div class="value" style="color:var(--blue)">{duration:.1f}s</div>
            <div class="label">Duration</div>
        </div>
    </div>

    <!-- Test Results -->
    <h2 class="section-title">Test Results</h2>
    {results_html}

    <!-- Screenshots -->
    {screenshot_section}

    <!-- Footer -->
    <div class="footer">
        <p>{_escape(PROJECT_NAME)} Test Report &mdash; Generated {timestamp}</p>
    </div>

</div>

<script>
function toggleModule(btn) {{
    btn.classList.toggle('open');
}}

function toggleDetail(id) {{
    const row = document.getElementById(id);
    if (row) {{
        const visible = row.style.display !== 'none';
        row.style.display = visible ? 'none' : 'table-row';
    }}
}}

// Auto-expand first module
document.addEventListener('DOMContentLoaded', () => {{
    const first = document.querySelector('.module-header');
    if (first) first.classList.add('open');
}});
</script>
</body>
</html>"""


# ── Main Runner ──────────────────────────────────────────────────────


def main():
    collector = ReportCollector()
    plugin = PytestPlugin(collector)

    if TEST_PATHS:
        test_files = TEST_PATHS
    else:
        test_files = _discover_test_files()

    if not test_files:
        print("No test files found. Place test_*.py files in the tests/ directory.")
        return 1

    print(f"Running tests: {len(test_files)} file(s)")
    for f in test_files:
        print(f"  {f}")
    print("=" * 60)

    exit_code = pytest.main(
        [*test_files, "-v", "--tb=short", "-p", "no:cacheprovider"],
        plugins=[plugin],
    )

    print("\n" + "=" * 60)
    print(f"Tests complete: {len(collector.results)} results collected")

    # Generate report
    report_path = Path(REPORT_PATH) if REPORT_PATH else ROOT / "tests" / "report.html"
    html_content = generate_html(collector)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(html_content, encoding="utf-8")
    print(f"Report written to: {report_path}")
    print(f"  Passed: {sum(1 for r in collector.results if r.status == 'passed')}")
    print(f"  Failed: {sum(1 for r in collector.results if r.status == 'failed')}")
    print(f"  Skipped: {sum(1 for r in collector.results if r.status == 'skipped')}")

    # Open in browser
    import webbrowser
    webbrowser.open(report_path.resolve().as_uri())

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
