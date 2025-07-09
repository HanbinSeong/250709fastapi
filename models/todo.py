# models/todo.py
from sqlalchemy import Column, Text, BigInteger, Boolean, DateTime, TIMESTAMP
from database import Base
from datetime import datetime


class Todo(Base):
    __tablename__ = "todo"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8",
        "mysql_collate": "utf8_general_ci",
    }

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    text = Column(Text, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False)
    due_date = Column(DateTime, default=datetime.now, nullable=False)