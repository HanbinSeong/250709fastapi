# schemas/board.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BoardBase(BaseModel):
    title: str
    author: str
    content: str


class BoardUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    date: Optional[datetime] = None
    views: Optional[int] = None
    like: Optional[int] = None
    content: Optional[str] = None


class BoardCreate(BoardBase):
    pass


class BoardOut(BoardBase):
    id: int
    date: datetime
    views: int
    like: int

    class Config:
        orm_mode = True

class LikeToggle(BaseModel):
    is_liked: bool