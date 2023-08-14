from sqlalchemy import Column, Integer, String

from src.db.tables.base import Base


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True)
    title = Column(String)
