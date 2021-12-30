from pydantic import BaseModel, Field

class User(BaseModel):
    __tablename__ = "users"

    id: int = Field(...)
    username: str = Field(...)
    email: str = Field(...)
    password: str = Field(None)
    activated: bool = Field(False, description="user is activated or not")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None