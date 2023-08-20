from datetime import datetime
from typing import NamedTuple
from fastapi import Query
from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeBase

class Pagination(NamedTuple):
    created_before: datetime | None = Query(
        None, description='If not set, newest records will be returned')
    page_size: int = Query(100, gt=0)

class Base(DeclarativeBase):
    pass

