import json
import os
import sys

import pandas as pd
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
        .stApp {
            background: #f5f7fb;
        }

        .block-container {
            max-width: 1440px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc;
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.14);
        }

        .sidebar-project {
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: #93c5fd !important;
        }

        .sidebar-title {
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
            font-size: 0.92rem;
            font-weight: 600;
            margin-top: 0.2rem;
        }

        .hero {
            background: linear-gradient(135deg, #ffffff 0%, #eff6ff 100%);
            border: 1px solid #dbeafe;
            border-radius: 20px;
            box-shadow: 0 8px 30px rgba(15, 23, 42, 0.06);
            margin-bottom: 1.5rem;
            padding: 2rem 2.2rem;
        }

        .hero-label {
            color: #2563eb;
            font-size: 0.75rem;
            font-weight: 750;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .hero-title {
            color: #0f172a;
            font-size: clamp(2rem, 4vw, 3rem);
            font-weight: 780;
            letter-spacing: -0.04em;
            line-height: 1.08;
            margin: 0.5rem 0 0.7rem;
        }

        .hero-text {
            color: #64748b;
            font-size: 1rem;
            line-height: 1.65;
            margin: 0;
            max-width: 790px;
        }

        .section-title {
            color: #0f172a;
            font-size: 1.25rem;
            font-weight: 720;
            margin: 1.7rem 0 0.8rem;
        }

        .section-caption {
            color: #64748b;
            font-size: 0.88rem;
            margin: -0.55rem 0 1rem;
        }

        div[data-testid="stFileUploader"] {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            box-shadow: 0 4px 18px rgba(15, 23, 42, 0.04);
            padding: 0.7rem 1rem 0.9rem;
        }

        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            box-shadow: 0 4px 18px rgba(15, 23, 42, 0.04);
            min-height: 122px;
            padding: 1.15rem 1.2rem;
        }

        div[data-testid="stMetricLabel"] {
            color: #64748b;
            font-weight: 650;
        }

        div[data-testid="stMetricValue"] {
            color: #0f172a;
            font-size: 1.7rem;
        }

        .sla-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            box-shadow: 0 4px 18px rgba(15, 23, 42, 0.04);
            min-height: 122px;
            padding: 1.15rem 1.2rem;
        }

        .sla-label {
            color: #64748b;
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

        .filename {
            align-items: center;
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 999px;
            color: #1d4ed8;
            display: inline-flex;
            font-size: 0.82rem;
            font-weight: 650;
            margin-top: 0.65rem;
            padding: 0.38rem 0.8rem;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 4px 18px rgba(15, 23, 42, 0.04);
        }

        .summary-heading {
            color: #2563eb;
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
    </style>
    """,
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
    "Upload performance JSON file",
    type=["json"],
    label_visibility="collapsed",
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
