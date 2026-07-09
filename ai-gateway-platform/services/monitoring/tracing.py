"""
OpenTelemetry instrumentation.

LOCAL_MODE:
    Tracing is enabled but no exporter is configured.
    This keeps the terminal clean and removes the
    dependency on Tempo.

PRODUCTION:
    Traces are exported to Tempo via OTLP.
"""

from opentelemetry import trace

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)

from core.config import settings


# ==========================================================
# Resource
# ==========================================================

resource = Resource.create(
    {
        "service.name": settings.APP_NAME,
    }
)

provider = TracerProvider(
    resource=resource
)

trace.set_tracer_provider(provider)


# ==========================================================
# Production Exporter
# ==========================================================

if not settings.LOCAL_MODE:

    otlp_exporter = OTLPSpanExporter(
        endpoint=settings.TEMPO_ENDPOINT,
        insecure=True,
    )

    provider.add_span_processor(
        BatchSpanProcessor(
            otlp_exporter
        )
    )


# ==========================================================
# Tracer
# ==========================================================

tracer = trace.get_tracer(__name__)