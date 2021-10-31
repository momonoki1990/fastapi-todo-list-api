from fastapi import APIRouter

router = APIRouter(
    prefix="/tasks/{task_id}/done",
    tags=["done"]
)

@router.post("")
async def mark_task_as_done():
    return "mark task as done"

@router.delete("")
async def unmark_task_as_done():
    return "unmark_task_as_done"