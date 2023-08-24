import re
from datetime import datetime
from typing import NamedTuple

from fastapi import Query
from pydantic import BaseModel, errors
from strenum import StrEnum


class naive_datetime(datetime):
    """Формат даты с Z на конце на выходе и без информации о временной зоне
    внутри
    """

    format = "%Y-%m-%dT%H:%M:%S.%fZ"

    @classmethod
    def __get_validators__(cls):
        yield cls.parse_datetime
        yield cls.remove_tzinfo

    @classmethod
    def remove_tzinfo(cls, dt: datetime):
        return dt.replace(tzinfo=None)

    @classmethod
    def parse_datetime(cls, value: str | datetime) -> datetime:
        if isinstance(value, datetime):
            return value
        try:
            return datetime.strptime(value, cls.format)
        except ValueError:
            raise errors.DateTimeError()

    @classmethod
    def to_str(cls, dt: datetime) -> str:
        return dt.strftime(cls.format)


class ApiModel(BaseModel):
    class Config:
        orm_mode = True  # Construct from arbitrary objects using their attrs
        smart_union = True  # Correctly handle Union types
        # Декодер пришлось указать для datetime, тк этот формат выдает алхимия
        json_encoders = {datetime: naive_datetime.to_str}


class Pagination(NamedTuple):
    limit: int = Query(10000, gt=0)
    page_number: int = Query(1, gt=0)


class IdModel(ApiModel):
    id: int

class Gender(StrEnum):
    male = 'male'
    female = 'female'

class RelationshipType(StrEnum):
    father = 'father'
    mother = 'mother'
    grandfather = 'grandfather'
    grandmother = 'grandmother'
    guardian = 'guardian'