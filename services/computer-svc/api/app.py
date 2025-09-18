from fastapi import FastAPI
from api.routers import compute

app = FastAPI()

app.include_router(compute.router, prefix="", tags=["computer"])
