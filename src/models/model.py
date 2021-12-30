from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from src.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(60))
    email = Column(String(254), unique=True)
    password = Column(String(60))
    activated = Column(Boolean)

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(1024))
    done = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tasks")