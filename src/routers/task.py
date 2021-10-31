from typing import List
from fastapi import APIRouter
from src.schema import task as task_schema

router = APIRouter(
    prefix="/tasks",
    tags=["task"]
)

@router.get("", response_model=List[task_schema.Task])
async def get_all_tasks():
    return [task_schema.Task(id=1, title="sample task1", done=False)]

@router.post("", response_model=task_schema.Task)
async def create_task(task_body: task_schema.TaskCreate):
    title = task_body.title
    return task_schema.Task(id=1, title=title, done=False)

@router.put("/{task_id}", response_model=task_schema.Task)
async def update_task(task_id: int, task_body: task_schema.TaskUpdate):
    title = task_body.title
    return task_schema.Task(id=task_id, title=title, done=False)

@router.delete("/{task_id}", response_model=None)
async def delete_task(task_id: int):
    print(task_id)
    return None