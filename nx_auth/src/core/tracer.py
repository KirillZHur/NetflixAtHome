import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)


def setup_tracer():
    if trace.get_tracer_provider().__class__.__name__ != "ProxyTracerProvider":
        return

    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://jaeger:4317")
    service_name = os.getenv("OTEL_SERVICE_NAME", "nx_auth")
    resource = Resource.create({"service.name": service_name})

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint=endpoint, insecure=True)
    )
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)


def configure_tracer(config: dict) -> None:
    trace.set_tracer_provider(
        TracerProvider(resource=Resource.create({"service.name": "auth-service"}))
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                collector_endpoint="http://{host}:{port}/api/traces".format(**config),
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )
