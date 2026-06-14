import json
import os
import sys
from datetime import datetime
from html import escape

import streamlit as st


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "backend"))

from backend.analyser import analyze_performance
from backend.llm_helper import generate_summary


st.set_page_config(
    page_title=" Performance Test Result Narrator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /*
     * Brand colors remain fixed.
     * Content colors and card surfaces inherit Streamlit's active theme.
     */
    :root {
        --qa-brand-blue: #2563eb;
        --qa-brand-blue-light: #93c5fd;
        --qa-sidebar-start: #0f172a;
        --qa-sidebar-end: #1e293b;

        --qa-text: var(--text-color);
        --qa-muted-text: color-mix(
            in srgb,
            var(--text-color) 68%,
            transparent
        );
        --qa-card-bg: color-mix(
            in srgb,
            var(--secondary-background-color) 96%,
            var(--primary-color) 4%
        );
        --qa-hero-bg-start: color-mix(
            in srgb,
            var(--secondary-background-color) 97%,
            var(--primary-color) 3%
        );
        --qa-hero-bg-end: color-mix(
            in srgb,
            var(--secondary-background-color) 86%,
            var(--primary-color) 14%
        );
        --qa-border: color-mix(
            in srgb,
            var(--text-color) 16%,
            transparent
        );
        --qa-blue-border: color-mix(
            in srgb,
            var(--primary-color) 30%,
            var(--secondary-background-color)
        );
        --qa-shadow: color-mix(
            in srgb,
            var(--text-color) 10%,
            transparent
        );
    }

    .stApp {
        background: var(--background-color);
        color: var(--qa-text);
    }

    .block-container {
        max-width: 1440px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Dark-blue branded sidebar */

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            var(--qa-sidebar-start) 0%,
            var(--qa-sidebar-end) 100%
        );
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(248, 250, 252, 0.14);
    }

    .sidebar-project {
        color: var(--qa-brand-blue-light) !important;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .sidebar-title {
        color: #f8fafc;
        font-size: 1.2rem;
        font-weight: 750;
        line-height: 1.35;
        margin: 0.4rem 0 0.35rem;
    }

    .sidebar-description {
        color: #cbd5e1 !important;
        font-size: 0.85rem;
        margin-bottom: 1.4rem;
    }

    .sidebar-label {
        color: #94a3b8 !important;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-top: 1.1rem;
        text-transform: uppercase;
    }

    .sidebar-value {
        color: #f8fafc;
        font-size: 0.92rem;
        font-weight: 600;
        margin-top: 0.2rem;
    }

    /* Branded hero card */

    .hero {
        background: linear-gradient(
            135deg,
            var(--qa-hero-bg-start) 0%,
            var(--qa-hero-bg-end) 100%
        );
        border: 1px solid var(--qa-blue-border);
        border-radius: 20px;
        box-shadow: 0 8px 30px var(--qa-shadow);
        color: var(--qa-text);
        margin-bottom: 1.5rem;
        padding: 2rem 2.2rem;
    }

    .hero-label {
        color: var(--qa-brand-blue);
        font-size: 0.75rem;
        font-weight: 750;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .hero-title {
        color: var(--qa-text);
        font-size: clamp(2rem, 4vw, 3rem);
        font-weight: 780;
        letter-spacing: -0.04em;
        line-height: 1.08;
        margin: 0.5rem 0 0.7rem;
    }

    .hero-text {
        color: var(--qa-muted-text);
        font-size: 1rem;
        line-height: 1.65;
        margin: 0;
        max-width: 790px;
    }

    /* Blue branded headings */

    .section-title {
        color: var(--qa-brand-blue);
        font-size: 1.25rem;
        font-weight: 720;
        margin: 1.7rem 0 0.8rem;
    }

    .section-caption {
        color: var(--qa-muted-text);
        font-size: 0.88rem;
        margin: -0.55rem 0 1rem;
    }

    /* File uploader */

    div[data-testid="stFileUploader"] {
        background: var(--qa-card-bg);
        border: 1px solid var(--qa-border);
        border-radius: 16px;
        box-shadow: 0 4px 18px var(--qa-shadow);
        color: var(--qa-text);
        padding: 0.7rem 1rem 0.9rem;
    }

    div[data-testid="stFileUploader"] section {
        background: color-mix(
            in srgb,
            var(--qa-card-bg) 90%,
            var(--qa-brand-blue) 10%
        );
        border-color: var(--qa-border);
        color: var(--qa-text);
    }

    div[data-testid="stFileUploader"] small,
    div[data-testid="stFileUploader"] span,
    div[data-testid="stFileUploader"] p {
        color: var(--qa-text);
    }

    div[data-testid="stFileUploader"] button {
        background: color-mix(
            in srgb,
            var(--qa-card-bg) 88%,
            var(--qa-brand-blue) 12%
        );
        border-color: var(--qa-blue-border);
        color: var(--qa-text);
    }

    /* Professional metric cards */

    div[data-testid="stMetric"] {
        background: var(--qa-card-bg);
        border: 1px solid var(--qa-border);
        border-radius: 16px;
        box-shadow: 0 4px 18px var(--qa-shadow);
        color: var(--qa-text);
        min-height: 122px;
        padding: 1.15rem 1.2rem;
    }

    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] p {
        color: var(--qa-muted-text) !important;
        font-weight: 650;
    }

    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] > div {
        color: var(--qa-text) !important;
        font-size: 1.7rem;
    }

    div[data-testid="stMetricDelta"] {
        color: var(--qa-text);
    }

    /* SLA status card */

    .sla-card {
        background: var(--qa-card-bg);
        border: 1px solid var(--qa-border);
        border-radius: 16px;
        box-shadow: 0 4px 18px var(--qa-shadow);
        color: var(--qa-text);
        min-height: 122px;
        padding: 1.15rem 1.2rem;
    }

    .sla-label {
        color: var(--qa-muted-text);
        font-size: 0.875rem;
        font-weight: 650;
        margin-bottom: 1rem;
    }

    .sla-badge {
        border-radius: 999px;
        display: inline-flex;
        font-size: 0.95rem;
        font-weight: 750;
        padding: 0.45rem 0.9rem;
    }

    /* Uploaded filename */

    .filename {
        align-items: center;
        background: color-mix(
            in srgb,
            var(--qa-card-bg) 82%,
            var(--qa-brand-blue) 18%
        );
        border: 1px solid var(--qa-blue-border);
        border-radius: 999px;
        color: var(--qa-brand-blue);
        display: inline-flex;
        font-size: 0.82rem;
        font-weight: 650;
        margin-top: 0.65rem;
        padding: 0.38rem 0.8rem;
    }

    /* Chart and AI summary containers */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--qa-card-bg);
        border-color: var(--qa-border);
        border-radius: 16px;
        box-shadow: 0 4px 18px var(--qa-shadow);
        color: var(--qa-text);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] p,
    div[data-testid="stVerticalBlockBorderWrapper"] li,
    div[data-testid="stVerticalBlockBorderWrapper"] strong,
    div[data-testid="stVerticalBlockBorderWrapper"] em,
    div[data-testid="stVerticalBlockBorderWrapper"] h1,
    div[data-testid="stVerticalBlockBorderWrapper"] h2,
    div[data-testid="stVerticalBlockBorderWrapper"] h3,
    div[data-testid="stVerticalBlockBorderWrapper"] h4 {
        color: var(--qa-text);
    }

    .summary-heading {
        color: var(--qa-brand-blue);
        font-size: 0.75rem;
        font-weight: 750;
        letter-spacing: 0.1em;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1.2rem;
        }

        .hero {
            border-radius: 16px;
            padding: 1.5rem;
        }

        div[data-testid="stMetric"],
        .sla-card {
            min-height: 108px;
        }
    }
</style>  """,
    unsafe_allow_html=True,
)


def render_sidebar(uploaded_file):
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-title">Performance Test Result Narrator</div>
            <div class="sidebar-description">
                AI-assisted performance analysis and reporting
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()

        st.markdown(
            '<div class="sidebar-value">Performance Test Result Narrator</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sidebar-label">AI Model</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-value">Groq</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-label">Upload Status</div>', unsafe_allow_html=True)
        if uploaded_file is None:
            st.warning("Awaiting JSON file")
        else:
            st.success("File uploaded")
            st.caption(uploaded_file.name)


def render_metric_cards(metrics):
    first_row = st.columns(3, gap="medium")
    first_row[0].metric("Average Response Time", f"{metrics['avg']:,.2f} ms")
    first_row[1].metric("P50 Latency", f"{metrics['p50']:,.2f} ms")
    first_row[2].metric("P95 Latency", f"{metrics['p95']:,.2f} ms")

    second_row = st.columns(3, gap="medium")
    second_row[0].metric("P99 Latency", f"{metrics['p99']:,.2f} ms")
    second_row[1].metric("Error Rate", f"{metrics['error_rate']:,.2f}%")

    status = metrics["sla_status"]
    status_colors = {
        "Healthy": ("#dcfce7", "#166534"),
        "Warning": ("#fef3c7", "#92400e"),
        "Critical": ("#fee2e2", "#991b1b"),
    }
    background, foreground = status_colors.get(status, ("#e2e8f0", "#334155"))

    second_row[2].markdown(
        f"""
        <div class="sla-card">
            <div class="sla-label">SLA Status</div>
            <span class="sla-badge" style="background:{background}; color:{foreground};">
                {status}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_recommended_actions(metrics):
    actions = []

    if metrics["p95"] >= 1000:
        actions.append(
            "Prioritize investigation of the slowest requests contributing to critical P95 latency."
        )
    elif metrics["p95"] >= 500:
        actions.append(
            "Review high-latency transactions and optimize the paths contributing to P95 response time."
        )
    else:
        actions.append(
            "Continue monitoring P95 latency to confirm that current response-time performance remains stable."
        )

    if metrics["error_rate"] > 0:
        actions.append(
            "Analyze failed requests by endpoint and error type, then retest after corrective changes."
        )
    else:
        actions.append(
            "Maintain error-rate monitoring in future test runs to detect reliability regressions."
        )

    actions.append(
        "Review this result alongside future test runs before approving production-impacting changes."
    )
    return actions


def build_executive_report(project_title, filename, metrics, ai_summary):
    generated_at = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    recommended_actions = get_recommended_actions(metrics)
    action_items = "".join(
        f"<li>{escape(action)}</li>" for action in recommended_actions
    )
    time_series_section = ""
    if metrics.get("time_series_insights"):
        time_series_section = f"""
        <section>
            <h2>Time-Series Insights</h2>
            <p>{escape(metrics['time_series_insights']['narrative'])}</p>
        </section>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(project_title)}</title>
    <style>
        body {{ font-family: Arial, sans-serif; color: #1e293b; line-height: 1.6;
                max-width: 900px; margin: 0 auto; padding: 40px; background: #f8fafc; }}
        main {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;
                padding: 32px; }}
        h1, h2 {{ color: #2563eb; }}
        .meta {{ color: #64748b; margin-bottom: 28px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
        th, td {{ border: 1px solid #e2e8f0; padding: 10px 12px; text-align: left; }}
        th {{ background: #eff6ff; }}
        .status {{ display: inline-block; font-weight: bold; padding: 6px 12px;
                   border-radius: 999px; background: #eff6ff; color: #1d4ed8; }}
        .summary {{ white-space: pre-wrap; }}
    </style>
</head>
<body>
<main>
    <h1>{escape(project_title)}</h1>
    <div class="meta">
        <strong>Generated:</strong> {escape(generated_at)}<br>
        <strong>Source Report:</strong> {escape(filename)}
    </div>
    <section>
        <h2>Performance Metrics</h2>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Average Response Time</td><td>{metrics['avg']:,.2f} ms</td></tr>
            <tr><td>P50 Latency</td><td>{metrics['p50']:,.2f} ms</td></tr>
            <tr><td>P95 Latency</td><td>{metrics['p95']:,.2f} ms</td></tr>
            <tr><td>P99 Latency</td><td>{metrics['p99']:,.2f} ms</td></tr>
            <tr><td>Error Rate</td><td>{metrics['error_rate']:,.2f}%</td></tr>
        </table>
    </section>
    <section>
        <h2>SLA Status</h2>
        <span class="status">{escape(metrics['sla_status'])}</span>
    </section>
    {time_series_section}
    <section>
        <h2>AI Executive Summary</h2>
        <div class="summary">{escape(ai_summary)}</div>
    </section>
    <section>
        <h2>Recommendations</h2>
        <ol>{action_items}</ol>
    </section>
</main>
</body>
</html>
"""


st.markdown(
    """
    <div class="hero">
        <div class="hero-label">Performance Intelligence</div>
        <h1 class="hero-title">Performance Test Result Narrator</h1>
        <p class="hero-text">
            Convert raw performance test results into clear latency metrics,
            SLA health indicators, and an AI-generated executive assessment.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Upload Test Results</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-caption">Upload a supported performance result in JSON format.</div>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload Performance Result",
    type=["json"],
    help="Upload the performance report to analyze.",
)

render_sidebar(uploaded_file)

if uploaded_file is None:
    st.info("Upload a performance JSON file to generate the dashboard.")
    st.stop()

st.markdown(
    f'<div class="filename">Uploaded file: {uploaded_file.name}</div>',
    unsafe_allow_html=True,
)

try:
    performance_data = json.load(uploaded_file)

    with st.spinner("Analyzing performance results and generating the executive summary..."):
        metrics = analyze_performance(performance_data)
        ai_summary = generate_summary(metrics)

    st.markdown('<div class="section-title">Performance Overview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">Key response-time, reliability, and SLA indicators.</div>',
        unsafe_allow_html=True,
    )
    render_metric_cards(metrics)

    st.markdown('<div class="section-title">AI Executive Summary</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">Groq-generated interpretation based on the calculated metrics.</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown('<div class="summary-heading">Executive Summary</div>', unsafe_allow_html=True)
        st.markdown(ai_summary)

    executive_report = build_executive_report(
        "Performance Test Result Narrator - Executive Report",
        uploaded_file.name,
        metrics,
        ai_summary,
    )
    report_filename = f"{os.path.splitext(uploaded_file.name)[0]}_executive_report.html"
    st.download_button(
        label="Download Executive Report",
        data=executive_report,
        file_name=report_filename,
        mime="text/html",
        use_container_width=True,
    )

except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
    st.error(
        "The uploaded file could not be analyzed. "
        "Confirm that it contains valid performance-result JSON."
    )
    st.caption(f"Details: {error}")
except Exception as error:
    st.error(
        "The analysis could not be completed. "
        "Check the application configuration and try again."
    )
    st.caption(f"Details: {error}")
