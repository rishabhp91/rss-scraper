#!/bin/sh

set -e

celery -A src.config.celery beat --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler
