import os
from celery import Celery
from worker.config import CeleryAppConfig


RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT", "5672")
RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "rabbitmq")
RABBITMQ_PWD = os.environ.get("RABBITMQ_PWD", "password123")
RABBITMQ_VHOST = os.environ.get("RABBITMQ_VHOST", "computer")

broker_url = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PWD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}"

celery_app = Celery("computer", broker=broker_url)
celery_app.config_from_object(CeleryAppConfig)

celery_app.autodiscover_tasks(["worker.tasks"])