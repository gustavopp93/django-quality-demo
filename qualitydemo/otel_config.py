"""
OpenTelemetry configuration for Django application.
This module sets up traces, logs, and metrics exporters to Grafana Alloy.
"""

import os
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor


def configure_opentelemetry():
    """
    Configure OpenTelemetry with OTLP exporters for traces and metrics.
    This function is designed to be called from Gunicorn's post_fork hook
    to ensure each worker process has its own instrumentation.
    """
    # Get configuration from environment variables
    otlp_endpoint = os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://alloy:4318')
    service_name = os.environ.get('OTEL_SERVICE_NAME', 'django-quality-demo')
    service_version = os.environ.get('OTEL_SERVICE_VERSION', '0.1.0')
    environment = os.environ.get('OTEL_ENVIRONMENT', 'development')

    # Create resource with service information
    resource = Resource.create({
        SERVICE_NAME: service_name,
        SERVICE_VERSION: service_version,
        "deployment.environment": environment,
    })

    # Configure Tracer Provider (for traces)
    tracer_provider = TracerProvider(resource=resource)
    trace_exporter = OTLPSpanExporter(endpoint=f"{otlp_endpoint}/v1/traces")
    tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
    trace.set_tracer_provider(tracer_provider)

    # Configure Meter Provider (for metrics)
    metric_exporter = OTLPMetricExporter(endpoint=f"{otlp_endpoint}/v1/metrics")
    metric_reader = PeriodicExportingMetricReader(metric_exporter)
    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[metric_reader]
    )
    metrics.set_meter_provider(meter_provider)

    # Instrument Psycopg (PostgreSQL) - can be done early
    PsycopgInstrumentor().instrument()

    print(f"OpenTelemetry configured: {service_name} -> {otlp_endpoint}", flush=True)
