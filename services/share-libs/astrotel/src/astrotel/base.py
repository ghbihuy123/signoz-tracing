from abc import ABC, abstractmethod
import logging

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

from astrotel.config import AstrotelSettings
from astrotel.error import InvalidOtelModeError

settings = AstrotelSettings()

class OtelTracingBase(ABC):
    service_name: str = settings.service_name
    environment: str = settings.deployment_environment
    otel_mode: str = settings.mode
    otel_grpc_endpoint: str = settings.grpc_endpoint
    otel_http_endpoint: str = settings.http_endpoint
    tracer_provider: TracerProvider
    logger_provider: LoggerProvider
    logs_ship_level: str = settings.logs_ship_level
    def __init__(self):
        # Init resource with name and deploy environment
        resource = Resource.create({
            'service.name': self.service_name,
            'deployment.environment': self.environment,
        })

        # Init self.tracer_provider
        self.tracer_provider = TracerProvider(resource=resource)
        trace_exporter = self._get_trace_exporter()
        self.tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))

        # Init self.logger_provider
        self.logger_provider = LoggerProvider(resource=resource)
        log_exporter = self._get_logs_exporter()
        self.logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

    def _get_trace_exporter(self):
        """Init trace exporter"""
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
        """Init logs exporter"""
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
        level = getattr(logging, self.logs_ship_level, logging.INFO)
        return LoggingHandler(level=level, logger_provider=self.logger_provider)
