# routers/user.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserOut, UserUpdate
from database import get_db
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        logger.warning("Attempt to register duplicate email: %s", user.email)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    user = User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info("Created user id=%s email=%s", user.id, user.email)
    return user


@router.get("/", response_model=List[UserOut], status_code=status.HTTP_200_OK)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()


@router.get("/{id}", response_model=UserOut, status_code=status.HTTP_200_OK)
def read_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/update/{id}")
def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = read_user(db, id)
    db_user.name = user.name if user.name else db_user.name
    db_user.email = user.email if user.email else db_user.email
    db_user.age = user.age if user.age else db_user.age
    db.commit()
    db.refresh(db_user)
    logger.info("Updated user id=%s", db_user.id)
    return db_user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = read_user(db, user_id)
    db.delete(user)
    db.commit()
    logger.info("Deleted user id=%s", user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
