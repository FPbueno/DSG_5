from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: str  # aceita qualquer texto, sem validação de formato

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class User(UserInDB):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
