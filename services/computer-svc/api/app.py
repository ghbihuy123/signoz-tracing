from fastapi import FastAPI
from api.routers import compute
from astrotel.provider.fastapi import FastAPIOpentelemetryTracing
import logging

app = FastAPI()
tracer = FastAPIOpentelemetryTracing()
tracer.configure_tracing(app)
logging_handler = tracer.configure_logging_handler()

# Attach handler to root logger
logging.basicConfig(
    level=logging.INFO, 
    handlers=[logging_handler, logging.StreamHandler()]  # also keep console logs
)

# Attach handler to FastAPI's logger too
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.addHandler(logging_handler)

uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.addHandler(logging_handler)

fastapi_logger = logging.getLogger("fastapi")
fastapi_logger.addHandler(logging_handler)

app.include_router(compute.router, prefix="", tags=["computer"])
