"""
OpenTelemetry instrumentation setup for distributed tracing across services.
"""
from opentelemetry import trace

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)


resource = Resource.create(
    {
        "service.name": "ai-gateway"
    }
)

provider = TracerProvider(
    resource=resource
)

trace.set_tracer_provider(provider)

otlp_exporter = OTLPSpanExporter(
    endpoint="localhost:4317",
    insecure=True,
)

provider.add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

tracer = trace.get_tracer(__name__)