"""
Prometheus metrics collection (request latencies, status codes, token usage counts).
"""

from prometheus_client import Counter, Histogram


# -----------------------------
# Request Metrics
# -----------------------------

REQUEST_COUNT = Counter(
    "gateway_requests_total",
    "Total number of requests"
)

REQUEST_LATENCY = Histogram(
    "gateway_request_latency_seconds",
    "Gateway request latency"
)

# -----------------------------
# Cache Metrics
# -----------------------------

REDIS_CACHE_HITS = Counter(
    "redis_cache_hits_total",
    "Total Redis cache hits"
)

SEMANTIC_CACHE_HITS = Counter(
    "semantic_cache_hits_total",
    "Total semantic cache hits"
)

REDIS_CACHE_MISSES = Counter(
    "redis_cache_misses_total",
    "Total Redis cache misses"
)

SEMANTIC_CACHE_MISSES = Counter(
    "semantic_cache_misses_total",
    "Total semantic cache misses"
)

# -----------------------------
# Model Usage
# -----------------------------

MODEL_REQUESTS = Counter(
    "model_requests_total",
    "Requests handled by each model",
    ["model"]
)

# -----------------------------
# Follow-up Detection
# -----------------------------

FOLLOWUP_REQUESTS = Counter(
    "followup_requests_total",
    "Number of follow-up requests"
)

# -----------------------------
# Kafka Events
# -----------------------------

KAFKA_EVENTS = Counter(
    "kafka_events_total",
    "Published Kafka events"
)

