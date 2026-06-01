from prometheus_client import Counter

# SRP: metric definitions are centralised here so no service imports prometheus directly
risk_summaries_total = Counter(
    "signal_harbor_risk_summaries_total",
    "Number of risk summary requests served",
    ["service_name"],
)
