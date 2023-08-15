from sqlalchemy import Column, Integer, String

from src.db.tables.base import Base

class Operator(Base):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String)
    password_hash = Column(String)
