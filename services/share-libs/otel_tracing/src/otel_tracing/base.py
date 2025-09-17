import os

from abc import ABC, abstractmethod

OTEL_MODE = os.environ.get('OTEL_MODE', 'grpc')
OTEL_GRPC_ENDPOINT = os.environ.get('OTEL_GRPC_ENDPOINT', 'http://localhost:4317')
OTEL_HTTP_ENDPOINT = os.environ.get('OTEL_HTTP_ENDPOINT', 'http://localhost:4318')


class TracingOpentelemetryBase(ABC):
    def __init__(self, service: str, environment: str, exporter_mode: str):
        self.service_name = self.service_name
        self.environment = self.environment
        self.otel_mode = OTEL_MODE
        self.otel_grpc_endpoint = OTEL_GRPC_ENDPOINT
        self.otel_http_endpoint = OTEL_HTTP_ENDPOINT

    @abstractmethod
    def configure_tracing(self):
        pass

    @abstractmethod
    def configure_logging(self):
        pass
