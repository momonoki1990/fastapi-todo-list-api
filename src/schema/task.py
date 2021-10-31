from typing import Optional
from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str

class Task(TaskBase):
    id: int
    done: bool

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass