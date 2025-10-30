"""
WSGI config for qualitydemo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qualitydemo.settings")

application = get_wsgi_application()

# Instrument Django after the application is created
# This ensures Django settings are loaded before instrumentation
if os.environ.get('ENABLE_OTEL', 'true').lower() == 'true':
    from opentelemetry.instrumentation.django import DjangoInstrumentor
    DjangoInstrumentor().instrument()
