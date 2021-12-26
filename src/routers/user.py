from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from src.schema import user as user_schema

router = APIRouter(prefix="/users", tags=["user"])

oauth2_schema: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/token")

async def fake_decode_token(token: str):
    return user_schema.User(id=1, username="Naoya", email="nick@sample.com")

async def get_current_user(token: str = Depends(oauth2_schema)):
    return fake_decode_token(token)

@router.get("/me", response_model=user_schema.User)
async def get_user(current_user: user_schema.User = Depends(get_current_user)):
    return current_user
