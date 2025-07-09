# schemas/user.py
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str
    age: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True