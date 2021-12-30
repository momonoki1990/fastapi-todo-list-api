from sqlalchemy import create_engine
from src.models.model import Base

DB_URL = "mysql+pymysql://root@db:3306/todo?charset=utf8mb4"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    reset_database()
