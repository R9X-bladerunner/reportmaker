import re
from datetime import datetime
from typing import NamedTuple

from fastapi import Query
from pydantic import BaseModel, errors


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
#
# class PId(str):
#     """
#     Field for 'p1' format
#     """
#
#     md_regex = re.compile(r"^p[0-9]+$")  # P1 format
#
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate
#
#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(
#             pattern=r"^p[0-9]+$",
#             examples=["p1", "p131"],
#         )
#
#     @classmethod
#     def validate(cls, v):
#         if not isinstance(v, str):
#             raise TypeError("string required")
#         m = cls.md_regex.fullmatch(v)
#         if not m:
#             raise ValueError("invalid PId format")
#         return v
#
#
# class MdId(str):
#     """
#     Field for 'MD00001' format
#     """
#
#     md_regex = re.compile(r"^md\d{5}$")  # MD00005 format
#
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate
#
#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(
#             pattern=r"^md\d{5}$",
#             examples=["md00001", "md00002"],
#         )
#
#     @classmethod
#     def validate(cls, v):
#         if not isinstance(v, str):
#             raise TypeError("string required")
#         m = cls.md_regex.fullmatch(v)
#         if not m:
#             raise ValueError("invalid MdId format")
#         return v
#
#
# class LgId(str):
#     """
#     Field for 'lg1' format
#     """
#
#     md_regex = re.compile(r"^lg[0-9]+$")  # lg1 format
#
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate
#
#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(
#             pattern=r"^lg[0-9]+$",
#             examples=["lg1", "lg131"],
#         )
#
#     @classmethod
#     def validate(cls, v):
#         if not isinstance(v, str):
#             raise TypeError("string required")
#         m = cls.md_regex.fullmatch(v)
#         if not m:
#             raise ValueError("invalid LgId format")
#         return v
#
#
# class TId(str):
#     """
#     Field for 't1' format
#     """
#
#     md_regex = re.compile(r"^t[0-9]+$")  # t1 format
#
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate
#
#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(
#             pattern=r"^t[0-9]+$",
#             examples=["t1", "t131"],
#         )
#
#     @classmethod
#     def validate(cls, v):
#         if not isinstance(v, str):
#             raise TypeError("string required")
#         m = cls.md_regex.fullmatch(v)
#         if not m:
#             raise ValueError("invalid TId format")
#         return v
