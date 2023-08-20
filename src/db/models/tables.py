

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, Boolean, Table, Text
from sqlalchemy.orm import relationship



from src.db.models.base import Base
from src.schemas.document import DocType
from src.schemas.patient import Gender
from src.schemas.relative import RelationshipType


relationships  = Table(
    "relationships",
    Base.metadata,
    Column("patient_id", Integer, ForeignKey("patients.id", ondelete='CASCADE'), primary_key=True),
    Column("relative_id", Integer, ForeignKey("patients.id", ondelete='CASCADE'), primary_key=True),
    Column("relationship_type", Enum(RelationshipType))
)



class Patient(Base):
    __tablename__ = "patients"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255), nullable=True)
    birthday = Column(Date, nullable=False)
    gender = Column(Enum(Gender))
    snils = Column(String(11))

    # if is_patient == False - creating only-Relative's status record (not Patient)
    # if is_patient == True - creating Patient status record and Relative or Not-Relative (depends on relationship table)
    is_patient = Column(Boolean, default=True, nullable=False)

    relatives = relationship('Patient',
                             secondary=relationships,
                             primaryjoin=id == relationships.c.patient_id,
                             secondaryjoin=id ==relationships.c.relative_id,
                             backref='patients')

    documents = relationship('Document', backref='patient')


class Document(Base):
    __tablename__ = "documents"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    series = Column(String)
    number = Column(String)
    document_type = Column(Enum(DocType))
    issue_date = Column(Date)
    issuing_authority = Column(String)
    owner_id = Column(Integer, ForeignKey('patients.id', ondelete='CASCADE'))

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