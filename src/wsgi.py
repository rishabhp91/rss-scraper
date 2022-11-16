"""
WSGI config for viral project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/gunicorn/
"""
# Python module
import os

# Third party module
from django.core.wsgi import get_wsgi_application

# Set the mandatory environment variable for project
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.local")

application = get_wsgi_application()
