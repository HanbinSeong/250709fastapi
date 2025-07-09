from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8",
        "mysql_collate": "utf8_general_ci",
    }
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    order_date = Column(DateTime, default=datetime.now)
    # N:1 관계 — User.orders 와 연관짓기
    user = relationship("User", back_populates="orders")

    # N:1 관계 — Product.orders 와 연관짓기
    product = relationship("Product", back_populates="orders")
    # ↑ ForeignKey 제약을 기반으로 JOIN 조건을 자동 추론 :contentReference[oaicite:2]{index=2}
