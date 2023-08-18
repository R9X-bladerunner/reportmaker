from datetime import date

from pydantic import Field

from src.schemas.base import ApiModel

from strenum import StrEnum

class Gender(StrEnum):
    female = 'жен'
    male = 'муж'


class RelationshipType(StrEnum):
    father = 'отец'
    mother = 'мать'
    grandfather = 'дедушка'
    grandmother = 'бабушка'
    guardian = 'опекун'


class RelativeId(ApiModel):
    id: int
class RelativeBase(ApiModel):
    last_name: str
    first_name: str
    middle_name: str | None = None
    birthday: date
    passport_number: str
    gender: Gender
    snils: str
    relationship_type: RelationshipType


class RelativeIn(RelativeBase):
    pass

class RelativeOut(RelativeBase, RelativeId):
    pass