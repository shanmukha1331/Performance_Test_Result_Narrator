from backend.llm_helper import generate_summary

metrics = {
    "avg": 390,
    "p50": 275,
    "p95": 910,
    "p99": 982,
    "error_rate": 2,
    "sla_status": "Warning"
}

summary = generate_summary(metrics)

print(summary)