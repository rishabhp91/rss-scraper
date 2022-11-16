# Python module
from __future__ import absolute_import
import os

# Third party module
from celery import Celery
from django.conf import settings

# Set the mandatory environment variable for project
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.local")

# Create our project app - Gateway Interface
app = Celery('src.config')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Schedule periodic tasks for automatic updation of RSS feeds
app.conf.beat_schedule = {
    "refresh-rss-every-hour": {
        "task": "src.rss.tasks.refresh_all_rss",
        "schedule": 3600
    }
}
