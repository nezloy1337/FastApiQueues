import logging

from celery import Celery

from core import settings

CELERY_BROKER_URL = "pyamqp://guest:guest@localhost//"  # RabbitMQ
CELERY_BACKEND = settings.mongo.url

log = logging.getLogger(__name__)

celery_app = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_BACKEND)

celery_app.conf.task_routes = {
    "tasks.process_log": {"queue": "logs"},
}
