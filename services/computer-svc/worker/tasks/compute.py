from celery import shared_task

@shared_task(name="worker.tasks.compute.add_task")
def add_task(a: float, b: float) -> float:
    return a + b