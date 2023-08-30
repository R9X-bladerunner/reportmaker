from datetime import datetime, date
from typing import NamedTuple

from fastapi import Query
from pydantic import BaseModel, errors
from strenum import StrEnum
from re import match


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

class DocType(StrEnum):
    passport = 'passport'
    birth_cert_new  = 'birth_cert'
    birth_cert_old = 'birth_cert_old'

class Validators:

    @staticmethod
    def validate_names(v):
        pattern = r'^([А-Яа-яёЁ]([ \'-]?[А-Яа-яёЁ])*)$'
        if not match(pattern, v):
            raise ValueError('incorrect format of the <first_name>/<last_name>/<middle_name> field value')
        return v



    @staticmethod
    def validate_date(v):
        try:
            input_date = datetime.strptime(v, '%Y-%m-%d').date()
        except TypeError:
            raise ValueError("data type of the date field must be str")
        except ValueError:
            raise ValueError("date field must be in <YYYY-MM-DD> format")

        current_date = date.today()
        if input_date > current_date:
            raise ValueError('<date must not be later than the current date>')
        return v


    @staticmethod
    def validate_document_series(v, values):
        print(values)
        if 'document_type' not in values:
            raise ValueError('<series> field requires filling in the <document_type> field')

        if values['document_type'] is None:
            raise ValueError('<series> field requires the correct value to be filled in the <document_type> field')

        if values['document_type'] == DocType.passport:
            pattern = r'^\d{4}$'
            if not match(pattern, v):
                raise ValueError('incorrect format of the <series> field value')

        if values['document_type'] in (DocType.birth_cert_new, DocType.birth_cert_old):
            pattern = r'[IVXLC1УХЛС]{1,4}-[А-Я]{2}'
            if not match(pattern, v):
                raise ValueError('incorrect format of the <series> field value')

        return v

    @staticmethod
    def validate_document_number(v):
        pattern = r'^\d{6}$'
        if not match(pattern, v):
            raise ValueError('incorrect format of the <number> field value')
        return v

