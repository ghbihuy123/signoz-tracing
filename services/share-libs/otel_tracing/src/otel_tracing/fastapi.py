
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

from otel_tracing.base import OpentelemetryTracingBase


class FastAPIOpentelemetryTracing(OpentelemetryTracingBase):
    def configure_tracing(self, app: FastAPI):
        # Instrument FastAPI
        FastAPIInstrumentor.instrument_app(app, tracer_provider=self.tracer_provider)

        # Instrument requests (sync HTTP client)
        RequestsInstrumentor().instrument(tracer_provider=self.tracer_provider)

        # Instrument httpx (async HTTP client)
        HTTPXClientInstrumentor().instrument(tracer_provider=self.tracer_provider)
