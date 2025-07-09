# schemas/todo.py
from pydantic import BaseModel
from typing import Optional


class TodoBase(BaseModel):
    text: str
    due_date: str


class TodoUpdate(BaseModel):
    text: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[str] = None


class TodoCreate(TodoBase):
    pass


class TodoOut(TodoBase):
    id: int
    completed: bool
    created_at: str
    updated_at: str
    due_date: str

    class Config:
        orm_mode = True