from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
from datetime import datetime


class Board(Base):
    __tablename__ = "board"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8",
        "mysql_collate": "utf8_general_ci",
    }

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(100), nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)
    views = Column(Integer, default=0, nullable=False)
    like = Column(Integer, default=0, nullable=False)
    content = Column(Text, nullable=False)
