from typing import Optional
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str = Field(...)
    email: str = Field(...)

class User(UserBase):
    id: int = Field(...)
    activated: bool = Field(False, description="user is activated or not")
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str = Field(...)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None