from sqlalchemy import Column, Integer, String, ForeignKey, Text

from src.db.tables.base import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255))
    middle_name = Column(String(255))
    last_name = Column(String(255))
    passport_number = Column(String(255))
