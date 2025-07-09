from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base


class Product(Base):
    __tablename__ = "products"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8",
        "mysql_collate": "utf8_general_ci",
    }
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=True)
    price = Column(Float, nullable=True)
    description = Column(String(1000), nullable=True)
    category = Column(String(100), nullable=True)
    image = Column(String(400), nullable=True)
    rating_rate = Column(Float, nullable=True)
    rating_count = Column(Integer, nullable=True)
    # Product 1:N Order — Order.product 와 연관짓기
    orders = relationship(
        "Order", back_populates="product", cascade="all, delete-orphan"
    )
    # ↑ 기본 패턴: 한 상품에는 여러 주문이 연결 :contentReference[oaicite:1]{index=1}
