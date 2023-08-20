from datetime import datetime
from typing import TypeVar, Union

from src.db.models.base import Base

TModel = TypeVar("TModel", bound=Base)
flat = Union[str, float, int, bool, None, datetime]
flat_dict = [str, flat]
