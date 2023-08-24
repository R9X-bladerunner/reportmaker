from datetime import date
from src.schemas.base import IdModel, ApiModel, RelationshipType, Gender

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

