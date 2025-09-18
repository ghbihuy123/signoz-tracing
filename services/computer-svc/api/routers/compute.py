from fastapi import APIRouter
from pydantic import BaseModel
from worker.tasks.compute import add_task

router = APIRouter()

class ComputeRequest(BaseModel):
    a: float
    b: float

@router.post("/compute")
async def compute(data: ComputeRequest):
    task = add_task.delay(data.a, data.b)