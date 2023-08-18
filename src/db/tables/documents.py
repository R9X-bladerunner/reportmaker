from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship

from src.db.tables.base import Base
from src.schemas.document import DocType


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    series = Column(String)
    number = Column(String)
    document_type = Column(Enum(DocType))
    issue_date = Column(Date)
    issuing_authority = Column(String)
    owner_id = Column(Integer, ForeignKey('patients.id'))




