from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, Enum

from src.db.tables.base import Base
from src.schemas.patient import Gender

#
# class Relative(Base):
#     __tablename__ = "relatives"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     last_name = Column(String(255), nullable=False)
#     first_name = Column(String(255), nullable=False)
#     middle_name = Column(String(255), nullable=True)
#     birthday = Column(Date, nullable=False)
#     gender = Column(Enum(Gender), nullable=False)
#     snils = Column(String, nullable=False)