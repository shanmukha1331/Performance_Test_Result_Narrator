# AI Usage Note

## AI Model

This project uses the Groq API with the Llama model for executive summary generation.

## Purpose of AI

The AI component converts technical performance metrics into business-friendly summaries.

## Input to AI

The following metrics are supplied to the model:

- Average Response Time
- P50 Latency
- P95 Latency
- P99 Latency
- Error Rate
- SLA Status

## Output Generated

The AI produces:

- Executive Summary
- Key Observations
- Risk Assessment
- Recommended Actions

## Human Oversight

The AI output is intended as an assistive analysis tool and should be reviewed before being used for production decision-making.

## Limitation

The AI only analyzes the metrics provided. It does not have access to infrastructure, application logs, databases, or system monitoring data.