from typing import Generic, TypeVar, List, Optional
from src.dal.base import AbstractRepository

_T = TypeVar("_T")


class AbstractService(Generic[_T]):
    repository: type(AbstractRepository[_T])

    def __init__(self, repository: AbstractRepository[_T]):
        self.repository = repository

    def get_by_id(self, obj_id) -> Optional[_T]:
        return self.repository.get_by_id(obj_id)

    def get_all(self) -> List[_T]:
        return self.repository.get_all()

    def create(self, obj: _T) -> _T:
        return self.repository.create(obj)

    def update(self, obj: _T) -> _T:
        return self.repository.update(obj)

    def delete(self, obj: _T) -> None:
        self.repository.delete(obj)

    def get_count(self) -> int:
        return self.repository.get_count()

    def create_bulk(self, objs: List[_T]) -> List[_T]:
        return self.repository.create_bulk(objs)

    def update_bulk(self, objs: List[_T]) -> List[_T]:
        return self.repository.update_bulk(objs)

    def delete_by_id(self, obj_id) -> None:
        self.repository.delete_by_id(obj_id)

    def filter_by(self, **kwargs) -> List[_T]:
        return self.repository.filter_by(**kwargs)

    def filter_first(self, **kwargs) -> Optional[_T]:
        return self.repository.filter_first(**kwargs)

    def filter_count(self, **kwargs) -> int:
        return self.repository.filter_count(**kwargs)

    def execute(self, stmt) -> None:
        return self.repository.execute(stmt)

    def raw_sql(self, stmt) -> None:
        return self.repository.raw_sql(stmt)
