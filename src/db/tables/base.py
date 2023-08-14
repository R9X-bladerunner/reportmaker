from sqlalchemy.orm import DeclarativeBase
from typing import TypeVar



class Base(DeclarativeBase):
    ...


BaseType = TypeVar("BaseType", bound=Base)
