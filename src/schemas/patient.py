from datetime import date

from pydantic import Field

from src.schemas.base import ApiModel, IdModel, Gender
from src.schemas.relative import RelationshipType





class PatientId(IdModel):
    pass

class PatientBase(ApiModel):
    last_name: str
    first_name: str
    middle_name: str
    birthday: date
    gender: Gender
    snils: str



class PatientIn(PatientBase):
    pass

class PatientOut(PatientBase, PatientId):
    pass

class PatientOutWithRelType(PatientOut):
    relative_to_patient_as: RelationshipType

class PatientUpdate(ApiModel):
    last_name: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    birthday: date | None = None
    gender: Gender | None = None
    snils: str | None = None
