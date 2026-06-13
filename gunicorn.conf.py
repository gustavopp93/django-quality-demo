"""Gunicorn configuration file."""

import multiprocessing
import os

# Binding
bind = "0.0.0.0:8000"

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "qualitydemo"

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190


# OpenTelemetry initialization hook
def post_fork(server, worker):
    """
    Initialize OpenTelemetry after forking worker processes.
    This ensures each worker has its own instrumentation and exporters.
    """
    if os.environ.get('ENABLE_OTEL', 'true').lower() == 'true':
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

        # Instrument Django - this must happen before Django processes any requests
        DjangoInstrumentor().instrument()

        # Instrument Psycopg (PostgreSQL)
        PsycopgInstrumentor().instrument()

        server.log.info(f"OpenTelemetry initialized in worker {worker.pid}: {service_name} -> {otlp_endpoint}")
