from celery import shared_task
from worker.celery_app import celery_app

@shared_task(name="worker.tasks.compute.add_task")
def add_task(a: float, b: float) -> float:
    return a + b