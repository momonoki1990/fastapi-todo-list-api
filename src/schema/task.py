from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str

class TaskResponse(TaskBase):
    id: int
    done: bool

    class Config:
        orm_mode = True

class TaskCreate(TaskBase):
    pass

class TaskCreateResponse(TaskBase):
    id: int
    done: bool

    class Config:
        orm_mode = True

class TaskUpdate(TaskBase):
    done: bool

class TaskUpdateResponse(TaskBase):
    id: int
    done: bool

    class Config:
        orm_mode = True