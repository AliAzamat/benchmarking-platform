from prometheus_client import Counter, Histogram, generate_latest

# How many runs we've streamed — the throughput of the platform.
runs_streamed = Counter("runs_streamed_total", "Run events fanned out")

# End-to-end stream latency: published_at → delivered to a client.
stream_latency = Histogram(
    "stream_latency_ms", "Run event stream latency in ms",
    buckets=[5, 10, 25, 50, 100, 250, 500],
)


def metrics_text() -> bytes:
    """Prometheus scrapes this; Grafana charts it."""
    return generate_latest()
