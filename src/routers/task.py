from fastapi import APIRouter

router = APIRouter(
    prefix="/tasks",
    tags=["task"]
)

@router.get("")
async def get_all_tasks():
    return "all tasks"

@router.post("")
async def create_task():
    return "created task"

@router.put("/{task_id}")
async def update_task():
    return "updated task"

@router.delete("/{task_id}")
async def delte_task():
    return "delete task"