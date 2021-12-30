from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from passlib.context import CryptContext
from src.schema import user as user_schema, task as task_schema
from src.cruds import user as user_crud
from src.db import get_db

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "id": 1,
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "activated": True,
    }
}
class UserInDB(user_schema.User):
    password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_schema: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/token")

router = APIRouter(prefix="", tags=["user"])

def fake_hashed_password(password: str):
    return "fakehashed" + password

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

async def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = user_schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: user_schema.User = Depends(get_current_user)):
    if not current_user.activated:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_hashed_password(password) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(username: str):
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": username,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/user", response_model=user_schema.Token)
async def register_user(
    form_data: user_schema.UserCreate = Depends(),
    db: AsyncSession = Depends(get_db)
):
    form_data.password = get_hashed_password(form_data.password)
    user = await user_crud.create_user(db, form_data)
    access_token = create_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=user_schema.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect uername or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=user_schema.User)
async def read_users_me(current_user: user_schema.User = Depends(get_current_active_user)):
    return current_user

@router.get("/users/me/tasks", response_model=List[task_schema.Task])
async def read_own_items(current_user: user_schema.User = Depends(get_current_active_user)):
    sample_task = task_schema.Task(id=1, title="my task", done=False)
    return [sample_task]