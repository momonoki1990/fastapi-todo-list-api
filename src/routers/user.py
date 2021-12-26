from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from src.schema import user as user_schema

router = APIRouter(prefix="/users", tags=["user"])

oauth2_schema: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/token")

@router.get("/me", response_model=user_schema.User)
async def get_user(token: str = Depends(oauth2_schema)):
    return user_schema.User(id=1, username="Naoya", email="nick@sample.com")
