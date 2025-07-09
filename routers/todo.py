# routers/todo.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from models.todo import Todo
from schemas.todo import TodoCreate, TodoOut, TodoUpdate
from database import get_db
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    todo = Todo(**todo.dict())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    logger.info("Created todo id=%s", todo.id)
    return todo


@router.get("", response_model=List[TodoOut], status_code=status.HTTP_200_OK)
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Todo).offset(skip).limit(limit).all()


@router.get("/{id}", response_model=TodoOut, status_code=status.HTTP_200_OK)
def read_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    db.delete(todo)
    db.commit()
    logger.info("Deleted todo id=%s", todo.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{id}/update", status_code=status.HTTP_200_OK)
def update_todo(id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    db_todo.text = todo.text if todo.text else db_todo.text
    db_todo.completed = todo.completed if todo.completed else db_todo.completed
    db_todo.due_date = todo.due_date if todo.due_date else db_todo.due_date
    db_todo.updated_at = datetime.now()
    db.commit()
    db.refresh(db_todo)
    logger.info("Updated todo id=%s", db_todo.id)
    return db_todo


@router.post("/{id}/complete", response_model=TodoOut, status_code=status.HTTP_200_OK)
def like_todo(id: int, payload: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    todo.completed = payload.completed
    db.commit()
    db.refresh(todo)
    logger.info("Updated Post Complete id=%s", todo.id)
    return todo
