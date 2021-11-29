from typing import Counter
from sqlalchemy import Boolean, Column, Integer, String
from src.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(1024))
    done = Column(Boolean)
