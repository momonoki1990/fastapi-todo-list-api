from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import task, user

app = FastAPI()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods="*"
)

app.include_router(task.router)
app.include_router(user.router)