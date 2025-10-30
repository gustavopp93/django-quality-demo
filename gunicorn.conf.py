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
        from qualitydemo.otel_config import configure_opentelemetry
        configure_opentelemetry()
        server.log.info(f"OpenTelemetry initialized in worker {worker.pid}")
