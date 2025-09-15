import httpx
import asyncio
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

# Set up the tracer provider and exporter
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Export spans to the console (for demonstration)
span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument httpx
HTTPXClientInstrumentor().instrument()

url = "https://example.com"

# --- Sync Example ---
with tracer.start_as_current_span("sync-example-span"):
    with httpx.Client() as client:
        response = client.get(url)

        print("\n--- SYNC REQUEST HEADERS ---")
        print(response.request.headers)

        print("\n--- SYNC RESPONSE HEADERS ---")
        print(response.headers)

# --- Async Example ---
async def get(url):
    with tracer.start_as_current_span("async-example-span"):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            print("\n--- ASYNC REQUEST HEADERS ---")
            print(response.request.headers)

            print("\n--- ASYNC RESPONSE HEADERS ---")
            print(response.headers)

asyncio.run(get(url))
