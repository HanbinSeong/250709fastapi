# routers/bord.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.bord import Bords
from schemas.bord import BordsCreate, BordsOut
from database import get_db

router = APIRouter()

@router.post("/", response_model=BordsOut)
def create_bord(bord: BordsCreate, db: Session = Depends(get_db)):
    print(bord)
    db_bord = Bords(**bord.dict())
    db.add(db_bord)
    db.commit()
    db.refresh(db_bord)
    return db_bord

@router.get("/{bord_id}", response_model=BordsOut)
def read_bord(bord_id: int, db: Session = Depends(get_db)):
    print("bord_id")
    print(bord_id)
    bord = db.query(Bords).filter(Bords.id == bord_id).first()
    if not bord:
        raise HTTPException(status_code=404, detail="Bords not found")
    return bord