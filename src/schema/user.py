from typing import Optional
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    email: str = Field(...)

class UserLogin(UserBase):
    password: str = Field(...)

class User(UserBase):
    id: int = Field(...)
    username: str = Field(...)
    activated: bool = Field(False, description="user is activated or not")
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    username: str = Field(...)
    password: str = Field(...)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None