import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from backend.analyser import analyze_performance

def test_analyze_performance():

    data = {
        "response_times": [100, 200, 300, 400, 500],
        "requests": 1000,
        "failed": 20
    }

    result = analyze_performance(data)

    assert result["error_rate"] == 2.0
    assert result["sla_status"] == "Healthy"