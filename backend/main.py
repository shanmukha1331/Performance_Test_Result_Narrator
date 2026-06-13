import numpy as np
from llm_helper import generate_summary
from fastapi import FastAPI, UploadFile, File
import json

app = FastAPI()

@app.get("/")
def home():
    return {
        "project": "QA-07 Performance Test Result Narrator",
        "status": "running"
    }

@app.post("/upload")
async def upload_json(file: UploadFile = File(...)):
    content = await file.read()

    data = json.loads(content)

    response_times = data["response_times"]

    requests = data["requests"]
    failed = data["failed"]

    p50 = np.percentile(response_times, 50)
    p95 = np.percentile(response_times, 95)
    p99 = np.percentile(response_times, 99)

    avg_response_time = np.mean(response_times)

    error_rate = (failed / requests) * 100

    if p95 < 500:
       sla_status = "Healthy"
    elif p95 < 1000:
       sla_status = "Warning"
    else:
       sla_status = "Critical"

    metrics = {
    "avg": round(float(avg_response_time), 2),
    "p50": round(float(p50), 2),
    "p95": round(float(p95), 2),
    "p99": round(float(p99), 2),
    "error_rate": round(float(error_rate), 2),
    "sla_status": sla_status
}

    ai_summary = generate_summary(metrics)

    return {
    "Performance Summary": {
        "Average Response Time (ms)": metrics["avg"],
        "P50 Latency (ms)": metrics["p50"],
        "P95 Latency (ms)": metrics["p95"],
        "P99 Latency (ms)": metrics["p99"],
        "Error Rate (%)": metrics["error_rate"],
        "SLA Status": metrics["sla_status"]
    },
    "AI Summary": ai_summary
}
