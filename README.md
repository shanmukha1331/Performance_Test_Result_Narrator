# 🚀 Performance Test Result Narrator

## 1. Project Overview

Performance Test Result Narrator is an AI-powered prototype that converts raw performance testing results into meaningful insights. Performance engineers and stakeholders often struggle to interpret raw latency and reliability metrics. This application automatically analyzes uploaded performance test results, calculates key metrics, determines SLA health, and generates an executive summary using a Large Language Model (LLM).

The project demonstrates an end-to-end AI workflow:

Input → Processing → AI Analysis → Output

---

## 2. Problem Statement

Performance testing tools generate large volumes of technical data that are difficult for non-technical stakeholders to understand.

Questions such as:

* Is the application healthy?
* Are response times acceptable?
* Is the SLA being met?
* What actions should be taken?

often require manual interpretation.

This project automates that process using AI.

---

## 3. Objectives

The primary objectives of this project are:

* Read performance test result files.
* Extract and calculate key performance indicators.
* Determine system health status.
* Generate executive-level summaries using AI.
* Present results through a simple and intuitive dashboard.

---

## 4. Features Implemented

### Input Processing

* JSON File Upload
* Custom JSON Support
* k6 JSON Support

### Performance Metrics

The system calculates:

* Average Response Time
* P50 Latency
* P95 Latency
* P99 Latency
* Error Rate

### SLA Health Assessment

The application classifies system health as:

| SLA Status | Condition              |
| ---------- | ---------------------- |
| Healthy    | P95 < 500 ms           |
| Warning    | 500 ms ≤ P95 < 1000 ms |
| Critical   | P95 ≥ 1000 ms          |

### AI-Powered Analysis

Using Groq LLM:

* Executive Summary Generation
* Performance Observation Extraction
* Risk Assessment
* Recommended Actions

### Dashboard

The Streamlit dashboard provides:

* File Upload Interface
* Performance Overview
* Metric Cards
* SLA Status Indicator
* AI Executive Summary

---

## 5. Architecture Overview

```text
User Uploads JSON
          │
          ▼
    Streamlit UI
          │
          ▼
   analyser.py
          │
          ▼
Performance Metrics
          │
          ▼
   llm_helper.py
          │
          ▼
      Groq LLM
          │
          ▼
 Executive Summary
          │
          ▼
 Dashboard Output
```

---

## 6. Technology Stack

| Layer                 | Technology    |
| --------------------- | ------------- |
| Language              | Python        |
| Frontend              | Streamlit     |
| Backend               | FastAPI       |
| AI Model              | Groq LLM      |
| Data Processing       | NumPy         |
| Environment Variables | Python-dotenv |
| Testing               | Pytest        |
| Version Control       | GitHub        |

---

## 7. Project Structure

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
│   └── main.py
│
├── sample_data/
│   ├── healthy.json
│   ├── warning.json
│   ├── critical.json
│   ├── healthy_k6.json
│   └── critical_k6.json
│
├── outputs/
│
└── tests/
    └── test_basic.py
```

---

## 8. Supported Input Formats

### Custom JSON Format

```json
{
  "response_times": [120,150,180,200,250],
  "requests": 1000,
  "failed": 20
}
```

### k6 Format

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
    },
    "http_req_failed": {
      "values": {
        "rate": 0.02
      }
    }
  }
}
```

---

## 9. Sample Test Scenarios

### Scenario 1: Healthy System

Expected Output:

* Low latency
* Low error rate
* Healthy SLA

### Scenario 2: Warning System

Expected Output:

* Moderate latency
* Moderate risk
* Warning SLA

### Scenario 3: Critical System

Expected Output:

* High latency
* High error rate
* Critical SLA

---

## 10. AI Prompt Engineering

The LLM receives:

* Average Response Time
* P50 Latency
* P95 Latency
* P99 Latency
* Error Rate
* SLA Status

The prompt instructs the model to:

* Avoid inventing metrics.
* Avoid unsupported assumptions.
* Provide structured output.
* Generate factual observations only.

---

## 11. Assumptions

* Uploaded files are valid JSON.
* Input follows supported schema.
* Groq API is available.
* Network connectivity exists during AI generation.

---

## 12. Limitations

* Prototype implementation.
* Supports only custom JSON and k6-style JSON.
* Does not support full JMeter XML parsing.
* Historical storage is not implemented.
* AI output quality depends on supplied metrics.

---

## 13. Future Enhancements

* SQLite-based report history
* PDF report generation
* Multi-file comparison
* Trend analysis
* JMeter XML support
* Export to Markdown/PDF

---

## 14. AI Capability Demonstrated

This project demonstrates:

* LLM Integration
* Prompt Engineering
* Structured AI Output
* Automated Performance Analysis
* AI-Assisted Decision Support

---

## 15. Setup Instructions

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create `.env` file:

```env
GROQ_API_KEY=your_api_key
```

### Run Application

```bash
streamlit run app.py
```

---

## 16. Demo Flow

1. Launch Streamlit application.
2. Upload performance JSON.
3. Metrics are calculated automatically.
4. SLA status is determined.
5. Groq LLM generates executive summary.
6. Results are displayed on dashboard.

---

## 17. Team Information
## Team Name : TeamInnovate 
## Project Title : QA-07 Quality Assurance - Performance Test Result Narrator
## Team Members:
Member 1 : Polisetty Jahnavi
Member 2 : Vasantha Rayapureddy
Member 3 : Ramireddy Shanmukha

---

## 18. Demo Video

Add video link here.

---

## 19. Repository

GitHub Repository:
https://github.com/JahnaviPolisetty/Performance_Test_Result_Narrator
