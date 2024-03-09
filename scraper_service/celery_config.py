from celery import Celery
import os


def make_celery(app_name=__name__):
    backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    broker = os.environ.get('BROKER_URL', 'redis://localhost:6379/0')
    return Celery(app_name, backend=backend, broker=broker)


celery = make_celery()
