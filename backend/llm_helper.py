from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=GROQ_API_KEY
)

def generate_summary(metrics):
    time_series_insights = metrics.get("time_series_insights")
    time_series_context = ""
    if time_series_insights:
        time_series_context = f"""
Time-Series Observations:
Highest Latency: {time_series_insights['highest_latency']} ms at {time_series_insights['highest_time']}
Lowest Latency: {time_series_insights['lowest_latency']} ms at {time_series_insights['lowest_time']}
Percentage Increase: {time_series_insights['percentage_increase'] if time_series_insights['percentage_increase'] is not None else 'Not calculable'}
Time-Series Narrative: {time_series_insights['narrative']}
"""

    prompt = f"""
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
{time_series_context}

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
- Reference the supplied time-series observations when available.
- Do not speculate.
- Keep the total response under 180 words.
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
