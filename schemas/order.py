# schemas/order.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from schemas.user import UserOut
from schemas.product import ProductOut


class OrderBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    order_date: Optional[datetime]


class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    order_date: Optional[datetime] = None


class OrderCreate(OrderBase):
    pass


class OrderOut(OrderBase):
    id: int
    user: UserOut         # 중첩된 User 정보
    product: ProductOut   # 중첩된 Product 정보

    class Config:
        orm_mode = True
