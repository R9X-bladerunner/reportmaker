from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, Enum, Boolean, Table
from sqlalchemy.orm import relationship

from src.db.tables.base import Base
from src.schemas.patient import Gender
from src.schemas.relative import RelationshipType


relationships  = Table(
    "relationships",
    Base.metadata,
    Column("patient_id", Integer, ForeignKey("patients.id"), primary_key=True),
    Column("relative_id", Integer, ForeignKey("patients.id"), primary_key=True),
    Column("relationship_type", Enum(RelationshipType))
)



class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(255))
    first_name = Column(String(255))
    middle_name = Column(String(255))
    birthday = Column(Date)
    gender = Column(Enum(Gender))
    snils = Column(String)

    is_patient = Column(Boolean, default=True, nullable=False)
    is_relative = Column(Boolean, default=False, nullable=False)

    relatives = relationship('Patient',
                             secondary=relationships,
                             primaryjoin=id == relationships.c.patient_id,
                             secondaryjoin=id ==relationships.c.relative_id,
                             backref='patients')

    documents = relationship('Document', backref='patient')


