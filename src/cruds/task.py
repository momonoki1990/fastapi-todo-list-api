from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.engine import Result
from src.models import task as task_model
from src.schema import task as task_schema

async def create_task(db: AsyncSession, task_create: task_schema.TaskCreate) -> task_model.Task:
    task = task_model.Task(**task_create.dict())
    task.done = False
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_task(db: AsyncSession, id: int) -> Optional[task_model.Task]:
    stmt = select(task_model.Task).where(task_model.Task.id == id)
    result: Result = await db.execute(stmt)
    return result.scalar()

async def get_tasks(db: AsyncSession) -> List[task_schema.TaskResponse]:
    stmt = select(task_model.Task)
    result: Result = await db.execute(stmt)
    return result.scalars().all()

async def update_task(db: AsyncSession, task: task_model.Task) -> task_model.Task:
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task
    

async def delete_task(db: AsyncSession, task: task_model.Task) -> None:
    await db.delete(task)
    await db.commit()