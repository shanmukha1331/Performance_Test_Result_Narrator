# AI Usage Note

## Project

Performance Test  Result Narrator

---

## AI Model Used

This project uses the **Groq API** with the **Llama 3.1 8B Instant** model to generate executive summaries from performance testing metrics.

---

## Purpose of AI in the Project

The objective of the AI component is to convert technical performance metrics into concise and business-friendly insights that can be understood by both technical and non-technical stakeholders.

The AI does not calculate metrics. All metrics are computed by the Python backend before being sent to the model.

---

## What AI Helped With

The AI was used for:

* Generating executive summaries
* Identifying key observations from performance metrics
* Performing risk assessment based on SLA status
* Suggesting recommended actions
* Converting raw performance data into stakeholder-friendly language

Example metrics provided to the AI:

* Average Response Time
* P50 Latency
* P95 Latency
* P99 Latency
* Error Rate
* SLA Status

---

## What AI Did Not Do

The AI was not used for:

* Calculating latency metrics
* Computing percentiles
* Calculating error rates
* Determining SLA status
* Processing raw JSON files

These operations were implemented using Python and NumPy.

---

## Challenges Encountered

During initial testing, the AI occasionally generated assumptions that were not present in the input data.

Examples included:

* Referring to CPU or memory utilization
* Mentioning throughput metrics
* Referencing unavailable metrics such as P90 latency
* Assuming infrastructure or database bottlenecks

These outputs were considered inaccurate because such information was not supplied to the model.

---

## Improvements Made

To improve accuracy, the prompt was refined with strict instructions:

* Analyze only supplied metrics
* Do not invent missing values
* Do not mention unsupported metrics
* Do not assume infrastructure issues
* Clearly state when information is unavailable

This significantly improved the reliability and factual accuracy of the generated summaries.

---

## Best Prompt Used

You are a Senior Performance Testing Engineer.

Analyze ONLY the metrics provided below.

STRICT RULES:
- Use only the supplied metrics.
- Do not invent or assume any values.
- Do not assume SLA thresholds, targets, CPU usage, memory usage, throughput, uptime, database bottlenecks, infrastructure issues, or network problems.
- Do not use phrases such as:
  "higher than expected"
  "acceptable levels"
  "service degradation"
  "system overload"
  unless explicitly supported by the provided metrics.
- If information is unavailable, state that it cannot be determined from the supplied data.
- Keep the analysis factual, concise, and professional.

Metrics:
Average Response Time: {metrics['avg']} ms
P50 Latency: {metrics['p50']} ms
P95 Latency: {metrics['p95']} ms
P99 Latency: {metrics['p99']} ms
Error Rate: {metrics['error_rate']}%
SLA Status: {metrics['sla_status']}

Risk Assessment Rules:
- Healthy SLA Status = Low Risk
- Warning SLA Status = Medium Risk
- Critical SLA Status = High Risk

Provide output in the following format:

Executive Summary:
(2-3 factual sentences based strictly on the supplied metrics)

Key Observations:
- Observation 1
- Observation 2
- Observation 3

Risk Assessment:
(Low / Medium / High)
Reason:
(Explain using the SLA Status and metrics only)

Recommended Actions:
- Action 1
- Action 2
- Action 3

Important:
- Base every statement strictly on the supplied metrics.
- Do not speculate.
- Keep the total response under 180 words.
"""

---

## Sample AI Output

Executive Summary:
The system's average response time is 390.0 ms. The P99 latency is 982.0 ms, indicating slower responses for a subset of requests. The error rate is 2.0%.

Key Observations:

* P95 latency is significantly higher than P50 latency.
* Error rate remains low at 2.0%.
* SLA status is currently Warning.

Risk Assessment:
Medium

Recommended Actions:

* Investigate high P95 and P99 latency values.
* Analyze latency distribution for bottlenecks.
* Review system optimization opportunities.

---

## Limitations of AI

* AI quality depends on the supplied metrics.
* AI does not have access to application logs, infrastructure data, or monitoring systems.
* AI should be considered an assistive analysis tool and not a replacement for detailed performance engineering investigations.

---

## Conclusion

The AI component successfully converts performance testing metrics into understandable executive summaries, helping stakeholders quickly understand application performance without manually interpreting raw latency statistics.
