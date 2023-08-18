from src.schemas.patient import PatientId, PatientBase
from strenum import StrEnum

class RelationshipType(StrEnum):
    father = 'отец'
    mother = 'мать'
    grandfather = 'дедушка'
    grandmother = 'бабушка'
    guardian = 'опекун'


class RelativeId(PatientId):
    pass

class RelativeBase(PatientBase):
    middle_name: str | None = None
    relationship_type: RelationshipType


class RelativeIn(RelativeBase):
    pass

class RelativeOut(RelativeBase, RelativeId):
    pass