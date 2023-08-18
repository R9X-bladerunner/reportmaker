from datetime import date

from pydantic import Field

from src.schemas.base import ApiModel

from strenum import StrEnum

class Gender(StrEnum):
    female = 'жен'
    male = 'муж'

class PatientId(ApiModel):
    id: int
class PatientBase(ApiModel):
    last_name: str
    first_name: str
    middle_name: str
    birthday: date
    passport_number: str
    gender: Gender
    snils: str


class PatientIn(PatientBase):
    pass

class PatientOut(PatientBase, PatientId):
    pass