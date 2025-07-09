# routers/board.py
from typing import List, Dict, Any, Tuple
from fastapi import APIRouter, Depends, HTTPException, Response, status
# from sqlalchemy import func
from sqlalchemy.orm import Session
from models.board import Board
from schemas.board import BoardCreate, BoardOut, BoardUpdate, LikeToggle
from database import get_db
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=BoardOut, status_code=status.HTTP_201_CREATED)
def create_board(board: BoardCreate, db: Session = Depends(get_db)):
    board = Board(**board.dict())
    db.add(board)
    db.commit()
    db.refresh(board)
    logger.info("Created board id=%s", board.id)
    return board


@router.get("/", response_model=List[BoardOut], status_code=status.HTTP_200_OK)
def read_boards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Board).offset(skip).limit(limit).all()

@router.post("/update/{id}", status_code=status.HTTP_200_OK)
def update_board(id: int, board: BoardUpdate, db: Session = Depends(get_db)):
    db_board = db.query(Board).filter(Board.id == id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )
    db_board.title = board.title if board.title else db_board.title
    db_board.author = board.author if board.author else db_board.author
    db_board.date = board.date if board.date else db_board.date
    db_board.views = board.views if board.views else db_board.views
    db_board.like = board.like if board.like else db_board.like
    db_board.content = board.content if board.content else db_board.content
    db.commit()
    db.refresh(db_board)
    logger.info("Updated board id=%s", db_board.id)
    return db_board

@router.post("/editpost/{id}", status_code=status.HTTP_200_OK)
def editpost_board(id: int, board: BoardUpdate, db: Session = Depends(get_db)):
    db_board = db.query(Board).filter(Board.id == id).first()
    if not db_board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )
    db_board.title = board.title if board.title else db_board.title
    db_board.date = board.date if board.date else datetime.now()
    db_board.content = board.content if board.content else db_board.content
    db.commit()
    db.refresh(db_board)
    logger.info("Updated board id=%s", db_board.id)
    return db_board

@router.post("/{id}/views", status_code=status.HTTP_200_OK)
def views_board(id: int, db: Session = Depends(get_db)):
    db_board = db.query(Board).filter(Board.id == id).first()
    if not db_board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )
    db_board.views += 1
    db.commit()
    db.refresh(db_board)
    logger.info("Updated Post Views id=%s", db_board.id)
    return db_board

@router.post("/{id}/like", response_model=BoardOut, status_code=status.HTTP_200_OK)
def like_board(id: int, payload: LikeToggle, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )
    # 좋아요 증감
    if payload.is_liked:
        board.like += 1
    else:
        board.like = max(0, board.like - 1)
    db.commit()
    db.refresh(board)
    logger.info("Updated Post Like id=%s", board.id)
    return board


@router.get("/{id}", response_model=BoardOut, status_code=status.HTTP_200_OK)
def read_board(id: int, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )
    return board





@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board(id: int, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == id).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )
    db.delete(board)
    db.commit()
    logger.info("Deleted board id=%s", board.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
