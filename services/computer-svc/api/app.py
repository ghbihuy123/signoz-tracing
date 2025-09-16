import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from worker.tasks.compute import add_task

app = FastAPI()

class ComputeRequest(BaseModel):
    a: float
    b: float

@app.post("/compute")
async def compute(data: ComputeRequest):
    task = add_task.delay(data.a, data.b)

