import os

from django.core.wsgi import get_wsgi_application
from opentelemetry.instrumentation.django import DjangoInstrumentor

try:
    from core.tracer import setup_tracer

    setup_tracer()
    DjangoInstrumentor().instrument()
except Exception:
    pass
    
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
