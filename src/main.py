from fastapi import FastAPI
from src.routers import task

app = FastAPI()

app.include_router(task.router)
