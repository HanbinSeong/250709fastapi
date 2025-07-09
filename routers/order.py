# routers/order.py
from typing import List, Dict, Any, Tuple
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.order import Order
from models.user import User
from models.product import Product
from schemas.order import OrderCreate, OrderOut, OrderUpdate
from database import get_db
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    order = Order(**order.dict())
    db.add(order)
    db.commit()
    db.refresh(order)
    logger.info("Created order id=%s", order.id)
    return order


@router.get("/", response_model=List[OrderOut], status_code=status.HTTP_200_OK)
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Order).offset(skip).limit(limit).all()


# JOIN 예시: User, Product 정보를 함께 조회
@router.get(
    "/with-details", response_model=List[Dict[str, Any]], status_code=status.HTTP_200_OK
)
def read_orders_with_details(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Order JOIN User, Product
    반환 예시: [{"order_id":1, "user_name":"Alice", "product_title":"Mouse", ...}, ...]
    """
    rows: List[Tuple[Order, User, Product]] = (
        db.query(Order, User, Product)
        .join(User, Order.user_id == User.id)
        .join(Product, Order.product_id == Product.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    result = []
    for order, user, product in rows:
        result.append(
            {
                "order_id": order.id,
                "quantity": order.quantity,
                "order_date": order.order_date,
                "user_name": user.name,
                "user_email": user.email,
                "product_title": product.title,
                "product_price": product.price,
            }
        )
    return result


# UNION / UNION ALL 예시
@router.get(
    "/quantity-union",
    response_model=List[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
)
def union_example(db: Session = Depends(get_db)):
    """
    quantity > 5 인 주문과 quantity < 2 인 주문을 UNION
    """
    q1 = db.query(Order.id.label("order_id"), Order.quantity, Order.order_date).filter(
        Order.quantity > 5
    )

    q2 = db.query(Order.id.label("order_id"), Order.quantity, Order.order_date).filter(
        Order.quantity < 2
    )

    # UNION (기본으로 중복 제거)
    union_q = q1.union(q2).all()

    # 만약 중복 포함하려면 .union_all(q2)
    # union_all_q = q1.union_all(q2).all()

    return [
        {"order_id": o.order_id, "quantity": o.quantity, "order_date": o.order_date}
        for o in union_q
    ]


# ORDER BY 예시: 주문 일자 내림차순 정렬
@router.get("/sorted", response_model=List[OrderOut], status_code=status.HTTP_200_OK)
def order_by_example(db: Session = Depends(get_db)):
    """
    ORDER BY order_date DESC
    """
    orders = db.query(Order).order_by(Order.order_date.desc()).all()
    return orders


# SUBQUERY 예시: 가격이 높은 상품(예: 100 이상) 주문만 조회
@router.get(
    "/high-value", response_model=List[OrderOut], status_code=status.HTTP_200_OK
)
def subquery_example(price_threshold: float = 100.0, db: Session = Depends(get_db)):
    """
    서브쿼리로 Product.price > threshold 인 product_id 목록을 뽑아
    해당 주문만 필터링
    """
    # 1) 가격이 높은 상품 ID를 찾는 서브쿼리
    subq = db.query(Product.id).filter(Product.price > price_threshold).subquery()

    # 2) 메인 쿼리에서 그 상품 주문만 필터
    orders = db.query(Order).filter(Order.product_id.in_(subq)).all()
    return orders


# 사용자별 기본 통계
#     1. 총 구매횟수 - /stats/by-user
#     2. 총 지출 - /stats/total-spent
#     3. 평균 구매 금액 - /stats/average-spent
#     4. 마지막 구매일 - /stats/last-purchase
@router.get(
    "/stats/all", response_model=List[Dict[str, Any]], status_code=status.HTTP_200_OK
)
def get_all_stats(db: Session = Depends(get_db)):
    """
    SELECT user_id,
           COUNT(Order.id) AS order_count,
           SUM(Order.quantity * Product.price) AS total_spent,
           AVG(Order.quantity * Product.price) AS average_spent,
           MAX(Order.order_date) AS last_purchase_date
      FROM orders
      JOIN products ON orders.product_id = products.id
     GROUP BY user_id
    """
    rows = (
        db.query(
            Order.user_id,
            func.count(Order.id).label("order_count"),
            func.sum(Order.quantity * Product.price).label("total_spent"),
            func.avg(Order.quantity * Product.price).label("average_spent"),
            func.max(Order.order_date).label("last_purchase_date"),
        )
        .join(Product, Order.product_id == Product.id)
        .group_by(Order.user_id)
        .all()
    )
    return [
        {
            "user_id": user_id,
            "order_count": order_count,
            "total_spent": total_spent,
            "average_spent": average_spent,
            "last_purchase_date": last_purchase_date,
        }
        for user_id, order_count, total_spent, average_spent, last_purchase_date in rows
    ]


@router.get("/{id}", response_model=OrderOut, status_code=status.HTTP_200_OK)
def read_order(id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


@router.post("/update/{id}")
def update_order(id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    db_order = read_order(db, id)
    db_order.user_id = order.user_id if order.user_id else db_order.user_id
    db_order.product_id = order.product_id if order.product_id else db_order.product_id
    db_order.quantity = order.quantity if order.quantity else db_order.quantity
    db_order.order_date = order.order_date if order.order_date else db_order.order_date
    db.commit()
    db.refresh(db_order)
    logger.info("Updated order id=%s", db_order.id)
    return db_order


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = read_order(db, order_id)
    db.delete(order)
    db.commit()
    logger.info("Deleted order id=%s", order.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/user/{user_id}", response_model=List[OrderOut])
def get_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    if not orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return orders


@router.get("/product/{product_id}", response_model=List[OrderOut])
def get_orders_by_product(product_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.product_id == product_id).all()
    if not orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return orders
