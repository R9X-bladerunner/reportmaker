from sqlalchemy import Column, Integer, String, ForeignKey, Text

from src.db.tables.base import Base


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    operator_id = Column(Integer, ForeignKey('operators.id'), nullable=True)
    html = Column(Text)