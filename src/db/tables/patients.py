from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, Boolean, Table
from sqlalchemy.orm import relationship

from src.db.tables.base import Base
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

    id = Column(Integer, primary_key=True, autoincrement=True)
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


