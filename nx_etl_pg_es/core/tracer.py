import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_tracer():
    if trace.get_tracer_provider().__class__.__name__ != "ProxyTracerProvider":
        return

    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    service_name = os.getenv("OTEL_SERVICE_NAME", "nx_etl_pg_es")
    resource = Resource.create({"service.name": service_name})

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint=endpoint, insecure=True)
    )
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)