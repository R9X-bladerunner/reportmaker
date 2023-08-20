from datetime import date

from pydantic import Field

from src.schemas.base import ApiModel, IdModel

from strenum import StrEnum

class Gender(StrEnum):
    male = 'male'
    female = 'female'


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
    is_patient: bool


class PatientUpdate(PatientBase):
    last_name: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    birthday: date | None = None
    gender: Gender | None = None
    snils: str | None = None
