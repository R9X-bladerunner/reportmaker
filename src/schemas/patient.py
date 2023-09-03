from datetime import date

from src.schemas.base import ApiModel, IdModel, Gender, Validators
from src.schemas.relative import RelationshipType
from pydantic import validator

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

    _name_validator = validator(
        'last_name',
        'first_name',
        'middle_name',
        allow_reuse=True)(Validators.validate_names)

    _birthday_validator = validator(
        'birthday',
        allow_reuse=True)(Validators.validate_date)

    class Config:
        schema_extra = {
            "example":
                {
                    "last_name": "Иванов",
                    "first_name": "Иван",
                    "middle_name": "Петрович",
                    "birthday": "2000-01-01",
                    "gender": "male",
                    "snils": "1234567890"
                }

        }

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


    _name_validator = validator(
        'last_name',
        'first_name',
        'middle_name',
        allow_reuse=True)(Validators.validate_names)

    _birthday_validator = validator(
        'birthday',
        allow_reuse=True)(Validators.validate_date)

    class Config:
        schema_extra = {
            "example":
                {
                    "last_name": "Иванов",
                    "first_name": "Иван",
                    "middle_name": "Петрович",
                    "birthday": "2000-01-01",
                    "gender": "male",
                    "snils": "1234567890"
                }

        }
