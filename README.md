# 🚀 Performance Test Result Narrator

## 1. Project Overview

Performance Test Result Narrator is an AI-powered application that transforms raw performance testing results into business-friendly insights. The system analyzes uploaded performance reports, computes key latency and reliability metrics, evaluates SLA health, performs optional time-series analysis, and generates executive-level summaries using a Large Language Model (LLM).

The application helps performance engineers, QA teams, project managers, and stakeholders quickly understand application health without manually interpreting complex performance metrics.

### End-to-End Workflow

Input Report → Analysis Engine → SLA Evaluation → AI Narration → HTML Executive Report → Dashboard Output

---

## 2. Problem Statement

Performance testing tools such as k6 and JMeter generate large amounts of technical performance data.

Typical reports contain metrics such as:

* Average Response Time
* P50 Latency
* P95 Latency
* P99 Latency
* Error Rate

While these metrics are useful for performance engineers, non-technical stakeholders often struggle to answer questions such as:

* Is the application healthy?
* Are response times acceptable?
* Is the SLA being met?
* What business risk exists?
* What corrective actions should be taken?

Manual interpretation takes time and often depends on experienced performance engineers.

This project automates that process using AI-powered narration.

---

## 3. Team Information

### Project Title

QA-07 Quality Assurance – Performance Test Result Narrator

### Team Members

* Polisetty Jahnavi
* Vasantha Rayapureddy
* Ramireddy Shanmukha

---

## 4. Objectives

The objectives of this project are:

* Read performance testing result files
* Support custom JSON and k6 JSON formats
* Calculate key performance indicators
* Evaluate SLA health
* Detect time-series latency patterns when available
* Generate AI-powered executive summaries
* Produce downloadable executive reports
* Present results through an intuitive dashboard

---

## 5. Features Implemented

### Input Processing

* JSON File Upload
* Custom JSON Support
* k6 JSON Support
* Optional Time-Series JSON Support

### Performance Metrics

The system calculates:

* Average Response Time
* P50 Latency
* P95 Latency
* P99 Latency
* Error Rate

### SLA Health Assessment

| SLA Status | Condition              |
| ---------- | ---------------------- |
| Healthy    | P95 < 500 ms           |
| Warning    | 500 ms ≤ P95 < 1000 ms |
| Critical   | P95 ≥ 1000 ms          |

### Time-Series Analysis

When timestamped latency data is available:

* Peak latency detection
* Lowest latency detection
* Latency variation analysis
* Time-series performance narration

### AI-Powered Analysis

Using Groq LLM:

* Executive Summary Generation
* Performance Observation Extraction
* Risk Assessment
* Recommended Actions
* Time-Series Insight Narration

### HTML Executive Report

* Downloadable HTML report
* Metrics summary
* SLA status
* Time-series insights
* AI executive summary
* Recommendations

### Dashboard

The Streamlit dashboard provides:

* File Upload Interface
* Performance Overview
* Metric Cards
* SLA Status Indicator
* AI Executive Summary
* HTML Report Download

---

## 6. Architecture Overview

```text
k6 / JSON Results
        │
        ▼
 Data Ingestion Layer
        │
        ▼
 Metrics Engine
 (Avg, P50, P95, P99, Error Rate)
        │
        ▼
 Time Series Analyzer
        │
        ▼
 SLA Health Analyzer
        │
        ▼
 Groq LLM Narrator Agent
        │
        ▼
 HTML Executive Report Generator
        │
        ▼
 Executive Dashboard
```

---

## 7. Technology Stack

| Layer                 | Technology    |
| --------------------- | ------------- |
| Language              | Python        |
| Frontend              | Streamlit     |
| Backend               | FastAPI       |
| AI Model              | Groq Llama    |
| Data Processing       | NumPy         |
| Environment Variables | python-dotenv |
| Testing               | Pytest        |
| Version Control       | GitHub        |

---

## 8. Project Structure

```text
Performance_Test_Result_Narrator/
│
├── app.py
├── requirements.txt
├── README.md
├── prompts.md
├── ai_usage_note.md
│
├── backend/
│   ├── analyser.py
│   ├── llm_helper.py
│   ├── main.py
│   └── __init__.py
│
├── sample_data/
│   ├── healthy.json
│   ├── warning.json
│   ├── critical.json
│   ├── healthyk6.json
│   ├── sample_k6.json
│   ├── healthy_timeseries.json
│   ├── warning_timeseries.json
│   └── critical_timeseries.json
│
├── outputs/
│
└── tests/
    └── test_basic.py
```

---

## 9. Supported Input Formats

### Custom JSON

```json
{
  "response_times": [120,150,180,200,250],
  "requests": 1000,
  "failed": 20
}
```

### Time-Series JSON

```json
{
  "response_times": [120,150,180,200,250],
  "requests": 1000,
  "failed": 20,
  "time_series": [
    {"time":"10:00","latency":120},
    {"time":"11:00","latency":180},
    {"time":"12:00","latency":250},
    {"time":"13:00","latency":450},
    {"time":"14:00","latency":850}
  ]
}
```

### k6 JSON

```json
{
  "metrics": {
    "http_req_duration": {
      "values": {
        "avg": 390,
        "p(50)": 275,
        "p(95)": 910,
        "p(99)": 982
      }
    }
  }
}
```

---

## 10. Sample Test Scenarios

### Healthy System

Expected:

* Low latency
* Low error rate
* Healthy SLA

### Warning System

Expected:

* Moderate latency
* Moderate risk
* Warning SLA

### Critical System

Expected:

* High latency
* High error rate
* Critical SLA

### Time-Series Analysis

Expected:

* Peak latency identification
* Trend narration
* Time-based performance insights

---

## 11. AI Capability Demonstrated

* LLM Integration
* Prompt Engineering
* Structured AI Output
* Automated Performance Analysis
* Time-Series Insight Generation
* AI-Assisted Performance Narration
* HTML Executive Report Generation
* AI-Assisted Decision Support

---

## 12. Assumptions

* Uploaded files are valid JSON
* Input follows supported schema
* Groq API is available
* Internet connectivity exists during AI generation

---

## 13. Limitations

* Prototype implementation
* No persistent database storage
* Limited input formats
* No automated bottleneck root-cause analysis
* AI output quality depends on supplied metrics

---

## 14. Future Enhancements

* SQLite report history
* Automated bottleneck detection
* Multi-file comparison
* Historical performance dashboard
* PDF report generation
* Full JMeter XML support
* AI anomaly detection
* Team collaboration features

---

## 15. Setup Instructions

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

```env
GROQ_API_KEY=your_api_key
```

### Run Application

```bash
streamlit run app.py
```

---

## 16. Demo Flow

1. Launch Streamlit application
2. Upload performance report
3. Metrics are calculated automatically
4. SLA health is evaluated
5. Time-series analysis is performed if available
6. Groq LLM generates executive summary
7. Results are displayed on dashboard
8. HTML executive report can be downloaded

---

## 17. Demo Video
Drive Link : 

---

## 18. Repository

GitHub Repository:

https://github.com/JahnaviPolisetty/Performance_Test_Result_Narrator

---

## 19. Live Application

https://jahnavipolisetty-performance-test-result-narrator-app-8srvmf.streamlit.app/
