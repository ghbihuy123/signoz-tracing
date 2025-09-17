from abc import abstractmethod
import logging
import os

from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter as GrpcLogExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as GrpcTraceExporter,
)
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter as HttpLogExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as HttpTraceExporter,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from otel_tracing.error import InvalidOtelModeError


OTEL_SERVICE_NAME = os.environ.get('OTEL_SERVICE_NAME', 'unknown-service')
OTEL_DEPLOYMENT_ENVIRONMENT = os.environ.get('OTEL_DEPLOYMENT_ENVIRONMENT', 'dev')
OTEL_MODE = os.environ.get('OTEL_MODE', 'grpc')
OTEL_GRPC_ENDPOINT = os.environ.get('OTEL_GRPC_ENDPOINT', 'http://localhost:4317')
OTEL_HTTP_ENDPOINT = os.environ.get('OTEL_HTTP_ENDPOINT', 'http://localhost:4318')


class OpentelemetryTracingBase:
    service_name: str = OTEL_SERVICE_NAME
    environment: str = OTEL_DEPLOYMENT_ENVIRONMENT
    otel_mode: str = OTEL_MODE
    otel_grpc_endpoint: str = OTEL_GRPC_ENDPOINT
    otel_http_endpoint: str = OTEL_HTTP_ENDPOINT
    tracer_provider: TracerProvider
    logger_provider: LoggerProvider

    def __init__(self):
        resource = Resource.create({
            'service.name': self.service_name,
            'deployment.environment': self.environment,
        })
        # Init trace provider
        self.tracer_provider = TracerProvider(resource=resource)
        trace_exporter = self._get_trace_exporter()
        self.tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))

        # Init logs provider
        self.logger_provider = LoggerProvider(resource=resource)
        log_exporter = self._get_logs_exporter()
        self.logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

    def _get_trace_exporter(self):
        if self.otel_mode == 'grpc':
            exporter = GrpcTraceExporter(endpoint=self.otel_grpc_endpoint, insecure=True)
        elif self.otel_mode == 'http':
            exporter = HttpTraceExporter(endpoint=self.otel_http_endpoint)
        else:
            raise InvalidOtelModeError(
                f"Unsupported OTEL mode: {self.otel_mode!r}. Expected 'grpc' or 'http'."
            )
        return exporter

    def _get_logs_exporter(self):
        if self.otel_mode == 'grpc':
            exporter = GrpcLogExporter(endpoint=self.otel_grpc_endpoint, insecure=True)
        elif self.otel_mode == 'http':
            exporter = HttpLogExporter(endpoint=self.otel_http_endpoint)
        else:
            raise InvalidOtelModeError(
                f"Unsupported OTEL mode: {self.otel_mode!r}. Expected 'grpc' or 'http'."
            )
        return exporter

    @abstractmethod
    def configure_tracing(self):
        pass

    def configure_logging_handler(self) -> LoggingHandler:
        return LoggingHandler(level=logging.INFO, logger_provider=self.logger_provider)
