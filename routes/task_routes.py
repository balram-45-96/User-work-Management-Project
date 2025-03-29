from fastapi import APIRouter, HTTPException, Depends, Security
from models.task import Task
from typing import List, Optional  # ✅ Import List for Python 3.8 and Optional for type hinting
from services.task_service import create_task, get_tasks, get_task, update_task, delete_task
from middlewares.auth_middleware import verify_token
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

router = APIRouter()

# Define a security scheme for the header token
api_key_header = APIKeyHeader(name="Authorization")

# Ensure TaskWithId is defined correctly
class TaskWithId(BaseModel):  # ✅ Ensure this is defined before usage
    id: str
    _id: str  # ✅ Include _id field
    title: str
    description: Optional[str] = None
    completed: bool = False

@router.get("/tasks", response_model=List[TaskWithId], dependencies=[Depends(api_key_header)], tags=["Tasks"])  # ✅ Add tag for grouping
async def read_tasks(payload: dict = Depends(verify_token)):
    tasks = await get_tasks()  # ✅ Ensure this function returns TaskWithId objects
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskWithId, dependencies=[Depends(api_key_header)], tags=["Tasks"])  # ✅ Add tag for grouping
async def read_task(task_id: str, payload: dict = Depends(verify_token)):
    print("task payload", payload)
    task = await get_task(task_id)  # ✅ Ensure this function returns TaskWithId object
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskWithId, dependencies=[Depends(api_key_header)], tags=["Tasks"])  # ✅ Add tag for grouping
async def update_existing_task(task_id: str, task: Task, payload: dict = Depends(verify_token)):
    updated_task = await update_task(task_id, task)  # ✅ Ensure this function returns TaskWithId object
    return updated_task

@router.delete("/tasks/{task_id}", dependencies=[Depends(api_key_header)], tags=["Tasks"])  # ✅ Add tag for grouping
async def delete_existing_task(task_id: str, payload: dict = Depends(verify_token)):
    return await delete_task(task_id)
