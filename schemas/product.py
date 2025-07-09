# schemas/product.py
from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    title: str
    price: float
    description: str
    category: str
    image: str
    rating_rate: float
    rating_count: int


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None
    rating_rate: Optional[float] = None
    rating_count: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True