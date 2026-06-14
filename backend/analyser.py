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

    result = {
        "avg": round(float(avg_response_time), 2),
        "p50": round(float(p50), 2),
        "p95": round(float(p95), 2),
        "p99": round(float(p99), 2),
        "error_rate": round(float(error_rate), 2),
        "sla_status": sla_status
    }

    time_series = data.get("time_series")
    if time_series:
        highest = max(time_series, key=lambda point: float(point["latency"]))
        lowest = min(time_series, key=lambda point: float(point["latency"]))
        highest_latency = float(highest["latency"])
        lowest_latency = float(lowest["latency"])
        percentage_increase = (
            ((highest_latency - lowest_latency) / lowest_latency) * 100
            if lowest_latency != 0
            else None
        )

        if percentage_increase is None:
            insight = (
                f"Latency peaked at {highest['time']} with {highest_latency:,.2f} ms. "
                "The percentage increase over the lowest observed latency cannot be "
                "calculated because the lowest value was 0 ms."
            )
        else:
            insight = (
                f"Latency peaked at {highest['time']} with {highest_latency:,.2f} ms, "
                f"representing a {percentage_increase:,.2f}% increase over the lowest "
                f"observed latency of {lowest_latency:,.2f} ms at {lowest['time']}."
            )

        result["time_series_insights"] = {
            "highest_time": highest["time"],
            "highest_latency": round(highest_latency, 2),
            "lowest_time": lowest["time"],
            "lowest_latency": round(lowest_latency, 2),
            "percentage_increase": (
                round(percentage_increase, 2)
                if percentage_increase is not None
                else None
            ),
            "narrative": insight,
        }

    return result
