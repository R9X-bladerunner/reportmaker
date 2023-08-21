from src.schemas.base import IdModel
from src.schemas.patient import PatientId, PatientBase, PatientUpdate
from strenum import StrEnum

class RelationshipType(StrEnum):
    father = 'отец'
    mother = 'мать'
    grandfather = 'дедушка'
    grandmother = 'бабушка'
    guardian = 'опекун'


class RelativeId(IdModel):
    pass

class RelativeBase(PatientBase):
    middle_name: str | None = None  # overload middle_name from patient model for make this attribute as not required
    relationship_type: RelationshipType


class RelativeIn(RelativeBase):
    pass

class RelativeOut(RelativeBase, RelativeId):
    relationship_type: RelationshipType | None = None

class RelativeUpdate(PatientUpdate):
    relationship_type: RelationshipType | None = None

