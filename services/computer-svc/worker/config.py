from kombu import Queue
from pydantic_settings import BaseSettings


class ComputerSettings(BaseSettings):
    """Use for future"""
    class Config:
        env_file = ".env"
        env_prefix = "COMPUTER_WORKER_"

class CeleryAppConfig:
    enable_utc = True
    timezone = 'Europe/London'

    task_queues = (
        Queue("computer", routing_key="computer"),
        Queue("analytics", routing_key="analytics"),
        Queue("default", routing_key="default"),
    )

    task_routes = {
        "worker.tasks.compute.*": {
            "queue": "computer",
        },
    }

    task_default_exchange = "analytics"
    task_default_routing_key = "analytics"