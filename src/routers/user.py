from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.schema import user as user_schema

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@sample.com",
        "password": "fakehashedsecret",
        "activated": False
    }, 
    "alice": {
        "username": "alice",
        "email": "alice@sample.com",
        "password": "fakehashedpassword2",
        "activated": True
    }
}

def fake_hashed_password(password: str):
    return "fakehashed" + password

router = APIRouter(prefix="/users", tags=["user"])

oauth2_schema: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/token")

async def fake_decode_token(token: str):
    return user_schema.User(id=1, username="Naoya", email="nick@sample.com")

class UserInDB(user_schema.User):
    hashed_password: str

async def get_current_user(token: str = Depends(oauth2_schema)):
    return fake_decode_token(token)

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hashed_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "Bearer"}

@router.get("/me", response_model=user_schema.User)
async def get_user(current_user: user_schema.User = Depends(get_current_user)):
    return current_user