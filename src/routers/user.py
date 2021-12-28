from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.schema import user as user_schema

fake_users_db = {
    "johndoe": {
        "id": 1,
        "username": "johndoe",
        "email": "johndoe@sample.com",
        "password": "fakehashedsecret",
        "activated": False
    }, 
    "alice": {
        "id": 2,
        "username": "alice",
        "email": "alice@sample.com",
        "password": "fakehashedpassword2",
        "activated": True
    }
}

def fake_hashed_password(password: str):
    return "fakehashed" + password

router = APIRouter(prefix="", tags=["user"])

oauth2_schema: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/token")

class UserInDB(user_schema.User):
    password: str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

async def fake_decode_token(token: str):
    return get_user(fake_users_db, token)

async def get_current_user(token: str = Depends(oauth2_schema)):
    user = await fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

async def get_current_active_user(current_user: user_schema.User = Depends(get_current_user)):
    if not current_user.activated:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hashed_password(form_data.password)
    if not hashed_password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me", response_model=user_schema.User)
async def read_users_me(current_user: user_schema.User = Depends(get_current_active_user)):
    return current_user