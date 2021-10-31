from fastapi import APIRouter

router = APIRouter(
    prefix="/tasks/{task_id}/done",
    tags=["done"]
)

@router.post("", response_model=None)
async def mark_task_as_done(task_id: int):
    print(task_id)
    return None

@router.delete("", response_model=None)
async def unmark_task_as_done(task_id: int):
    print(task_id)
    return None