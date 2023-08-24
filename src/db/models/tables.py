

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, Text, CheckConstraint
from sqlalchemy.orm import relationship

from src.db.models.base import Base
from src.schemas.document import DocType
from src.schemas.patient import Gender
from src.schemas.relative import RelationshipType


# relationships = Table(
#     "relationships",
#     Base.metadata,
#     Column("patient_id", Integer, ForeignKey("patients.id", ondelete="CASCADE"), primary_key=True),
#     Column("relative_id", Integer, ForeignKey("relatives.id", ondelete="CASCADE"), primary_key=True),
#     Column("relationship_type", Enum(RelationshipType))
# )

class Relationship(Base):
    __tablename__ = 'relationships'

    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), primary_key=True)
    relative_id = Column(Integer, ForeignKey("relatives.id", ondelete="CASCADE"), primary_key=True)
    relationship_type = Column(Enum(RelationshipType))

    relative = relationship("Relative", uselist=False)
    patient = relationship("Patient", uselist=False)





class Patient(Base):
    __tablename__ = "patients"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=False)
    gender = Column(Enum(Gender))
    snils = Column(String(11))

    relatives = relationship(
        "Relative",
        secondary='relationships',
        backref="patients"
    )
    relative_association = relationship("Relationship")

    documents = relationship("Document", backref="patient")


class Relative(Base):
    __tablename__ = "relatives"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255), nullable=True)
    birthday = Column(Date, nullable=False)
    gender = Column(Enum(Gender))
    snils = Column(String(11))

    relative_association = relationship("Relationship")

    documents = relationship("Document", backref="relative")

class Document(Base):
    __tablename__ = "documents"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    series = Column(String, nullable=False)
    number = Column(String, nullable=False)
    document_type = Column(Enum(DocType), nullable=False)
    issue_date = Column(Date, nullable=False)
    issuing_authority = Column(String, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=True)
    relative_id = Column(Integer, ForeignKey("relatives.id", ondelete="CASCADE"), nullable=True)
    __table_args__ = (
            CheckConstraint(
                "(patient_id IS NOT NULL AND relative_id IS NULL) OR (patient_id IS NULL AND relative_id IS NOT NULL) OR (patient_id IS NOT NULL AND relative_id IS NOT NULL)",
                name="check_valid_document",
            ),
        )


class Operator(Base):
    __tablename__ = "operators"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String)
    password_hash = Column(String)

class Template(Base):
    __tablename__ = "templates"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    operator_id = Column(Integer, ForeignKey('operators.id'), nullable=True)
    html = Column(Text)