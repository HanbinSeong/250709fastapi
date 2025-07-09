# routers/product.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from models.product import Product
from schemas.product import ProductCreate, ProductOut, ProductUpdate
from database import get_db
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    if db.query(Product).filter(Product.title == product.title).first():
        logger.warning("Attempt to register duplicate product: %s", product.title)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Product Title already registered"
        )
    product = Product(**product.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    logger.info("Created product id=%s", product.id)
    return product


@router.get("/", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Product).offset(skip).limit(limit).all()


@router.get("/{id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
def read_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.post("/update/{id}")
def update_product(id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = read_product(db, id)
    db_product.title = product.title if product.title else db_product.title
    db_product.price = product.price if product.price else db_product.price
    db_product.description = product.description if product.description else db_product.description
    db_product.category = product.category if product.category else db_product.category
    db_product.image = product.image if product.image else db_product.image
    db_product.rating_rate = product.rating_rate if product.rating_rate else db_product.rating_rate
    db_product.rating_count = product.rating_count if product.rating_count else db_product.rating_count
    db.commit()
    db.refresh(db_product)
    logger.info("Updated product id=%s", db_product.id)
    return db_product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = read_product(db, product_id)
    db.delete(product)
    db.commit()
    logger.info("Deleted product id=%s", product.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
