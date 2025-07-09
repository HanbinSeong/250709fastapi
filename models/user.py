from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8",
        "mysql_collate": "utf8_general_ci",
    }
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(100))
    age = Column(Integer, nullable=True)
    # User 1:N Order — Order.user 와 연관짓기
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    # ↑ back_populates 로 매핑된 반대쪽 속성 이름을 지정 :contentReference[oaicite:0]{index=0}
