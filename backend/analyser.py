import numpy as np

def analyze_performance(data):

    # k6 format support
    if "metrics" in data:

        avg_response_time = data["metrics"]["http_req_duration"]["values"]["avg"]

        p50 = data["metrics"]["http_req_duration"]["values"]["p(50)"]
        p95 = data["metrics"]["http_req_duration"]["values"]["p(95)"]
        p99 = data["metrics"]["http_req_duration"]["values"]["p(99)"]

        error_rate = (
            data["metrics"]["http_req_failed"]["values"]["rate"] * 100
        )

    # Existing custom JSON support
    else:

        response_times = data["response_times"]

        requests = data["requests"]
        failed = data["failed"]

        avg_response_time = np.mean(response_times)

        p50 = np.percentile(response_times, 50)
        p95 = np.percentile(response_times, 95)
        p99 = np.percentile(response_times, 99)

        error_rate = (failed / requests) * 100

    if p95 < 500:
        sla_status = "Healthy"
    elif p95 < 1000:
        sla_status = "Warning"
    else:
        sla_status = "Critical"

    return {
        "avg": round(float(avg_response_time), 2),
        "p50": round(float(p50), 2),
        "p95": round(float(p95), 2),
        "p99": round(float(p99), 2),
        "error_rate": round(float(error_rate), 2),
        "sla_status": sla_status
    }