from fastapi import FastAPI
from api.routers import compute
from astrotel.provider.fastapi import FastAPIOpentelemetryTracing

app = FastAPI()
tracer = FastAPIOpentelemetryTracing().configure_tracing(app)

app.include_router(compute.router, prefix="", tags=["computer"])
