from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60))
    email = Column(String(254))
    password = Column(String(60))
    activated = Column(Boolean)

    tasks = relationship("Task", back_populates="owner")