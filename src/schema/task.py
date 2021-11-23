from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title: str = Field(..., example="running", max_length=1024)

class TaskResponse(TaskBase):
    id: int = Field(..., gt=1, example=1)
    done: bool = Field(False, description="done task or not")

    class Config:
        orm_mode = True

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    done: bool = Field(False, description="done task or not")