from backend.analyser import analyze_performance

data = {
    "response_times": [120,150,180,200,250,300,400,500,800,1000],
    "requests": 1000,
    "failed": 20
}

print(analyze_performance(data))