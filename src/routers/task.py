from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema import task as task_schema
from src.db import get_db
from src.cruds import task as task_crud

router = APIRouter(prefix="/tasks", tags=["task"])

@router.get("", response_model=List[task_schema.TaskResponse])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    return await task_crud.get_tasks(db)


@router.post("", response_model=task_schema.TaskResponse)
async def create_task(
    task_body: task_schema.TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    return await task_crud.create_task(db, task_body)


@router.put("/{task_id}", response_model=task_schema.TaskResponse)
async def update_task(
    task_body: task_schema.TaskUpdate,
    task_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
):
    task = await task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = task_body.title
    task.done = task_body.done
    return await task_crud.update_task(db, task)


@router.delete("/{task_id}", response_model=None)
async def delete_task(
    task_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)
):
    task = await task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    await task_crud.delete_task(db, task)
