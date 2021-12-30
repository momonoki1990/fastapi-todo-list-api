from sqlalchemy.ext.asyncio import AsyncSession
from src.schema import user as user_schema
from src.models import model

async def create_user(db: AsyncSession, form_data: user_schema.UserCreate) -> model.User:
    user = model.User(**form_data.dict())
    user.activated = True
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
