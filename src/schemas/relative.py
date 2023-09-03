from datetime import date
from src.schemas.base import IdModel, ApiModel, RelationshipType, Gender, Validators
from pydantic import validator, Field


class RelativeId(IdModel):
    pass

class RelativeBase(ApiModel):
    last_name: str
    first_name: str
    middle_name: str | None = None
    birthday: date
    gender: Gender
    snils: str


class RelativeIn(RelativeBase):
    relationship_type: RelationshipType

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
                    "first_name": "Петр",
                    "middle_name": "Алексеевич",
                    "birthday": "1975-01-01",
                    "gender": "male",
                    "snils": "1234567890",
                    "relationship_type": "father"
                }

        }


class RelativeOut(RelativeBase, RelativeId):
    relationship_type: RelationshipType | None = None

class RelativeUpdate(ApiModel):
    last_name: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    birthday: date | None = None
    gender: Gender | None = None
    snils: str | None = None
    relationship_type: RelationshipType | None = None

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
                    "first_name": "Петр",
                    "middle_name": "Алексеевич",
                    "birthday": "1975-01-01",
                    "gender": "male",
                    "snils": "1234567890",
                    "relationship_type": "father"
                }

        }
