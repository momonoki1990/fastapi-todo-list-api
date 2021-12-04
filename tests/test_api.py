import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.db import Base, get_db
from src.main import app

ASYNC_DB_URL = "mysql+asyncmy://root@db-test:3306/todo?charset=utf8mb4"

@pytest.fixture
async def async_client() -> AsyncClient:
    engine = create_async_engine(ASYNC_DB_URL, echo=True, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        autoflush=True, bind=engine, class_=AsyncSession, future=True
    )

    async def get_test_db():
        async with async_session() as session:
            yield session
    app.dependency_overrides[get_db] = get_test_db

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

@pytest.fixture
async def sample_req_body():
    return {
        "title": "sample task title"
    }

@pytest.fixture
async def sample_res_body():
    return {
        "id": 1,
        "title": "sample task title",
        "done": False
    }

@pytest.mark.asyncio
async def test_create_and_read_task(async_client, sample_req_body, sample_res_body):
    res: Response = await async_client.post("/tasks", json=sample_req_body)
    assert res.status_code == 200
    assert res.json()== sample_res_body

    res2: Response = await async_client.get("/tasks")
    assert res2.status_code == 200
    assert res2.json()[0] == sample_res_body

@pytest.mark.asyncio
async def test_create_task_ng(async_client):
    res: Response = await async_client.post("tasks", json={})
    assert res.status_code == 422

@pytest.mark.asyncio
async def test_create_and_update_task(async_client, sample_req_body):
    res: Response = await async_client.post("tasks", json=sample_req_body)
    id = res.json()["id"]
    req_body_update = {
        "title": "updated task title",
        "done": True
    }
    res2: Response = await async_client.put(f"tasks/{id}", json=req_body_update)
    assert res2.status_code == 200
    res2.json() == req_body_update.update({"id": id})

@pytest.mark.asyncio
async def test_create_and_delete_task(async_client, sample_req_body):
    res: Response = await async_client.post("tasks", json=sample_req_body)
    id = res.json()["id"]
    res2: Response = await async_client.delete(f"tasks/{id}")
    assert res2.status_code == 200
    assert res2.json() is None

