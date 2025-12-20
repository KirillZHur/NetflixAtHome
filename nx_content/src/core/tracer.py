from os import getenv

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_tracer():
    if trace.get_tracer_provider().__class__.__name__ != "ProxyTracerProvider":
        return

    exporter_endpoint = getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://jaeger:4317")
    service_name = getenv("OTEL_SERVICE_NAME", "nx_content")

    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=exporter_endpoint, insecure=True))
    provider.add_span_processor(span_processor)

    trace.set_tracer_provider(provider)
