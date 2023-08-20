from typing import Generic, Iterable, Mapping, Sequence, TypeVar

from fastapi import Depends
from sqlalchemy import delete, insert, select, update
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.interfaces import ORMOption
from sqlalchemy.sql import Delete, Insert, Select, Update
from sqlalchemy.orm import Session

from src.db.connection import get_session
from src.db.models.base import Pagination

_T = TypeVar('_T')
_T2 = TypeVar('_T2')


def _rows_to_orm(stmt: Update | Insert, model: type) -> Select:
    return select(model).from_statement(stmt).execution_options(populate_existing=True)


class Dal(Generic[_T]):
    model: type[_T]

    def __init__(self, sess: Session = Depends(get_session)) -> None:
        self.sess = sess

    # Create
    def add_orm(self, obj: _T2) -> _T2:
        """
        Save object (and its nested objects) into database.
        NOTE: Doesn't support `asyncio.gather` because of eager `sess.flush()`.
        NOTE: Does any of INSERT/UPDATE/DELETE sql.
        """
        self.sess.add(obj)
        self.sess.flush()

        return obj

    def bulk_add_orm(self, *objects: _T2) -> tuple[_T2, ...]:
        self.sess.add_all(objects)
        self.sess.flush()
        return objects

    def insert(self, item: Mapping) -> _T:
        row_stmt = insert(self.model).returning(self.model).values(**item)
        stmt = _rows_to_orm(row_stmt, self.model)
        return self.sess.scalar(stmt)

    def bulk_insert(self, items: Iterable[Mapping]) -> list[_T]:
        stmt = insert(self.model).returning(self.model).values([*items])
        orm_stmt = _rows_to_orm(stmt, self.model)
        objects = self.sess.scalars(orm_stmt)
        return objects.all()

    # Retrieve
    def get_(self, id_: int, options: Sequence[ORMOption] = None) -> _T | None:
        return self.sess.get(self.model, id_, options = options)

    def fetch_one(self, stmt: Select) -> _T | None:
        """Returns at most 1 item, fails if there's more"""
        objects = self.sess.scalars(stmt)
        return objects.unique().one_or_none()

    def fetch_first(self, stmt: Select) -> _T | None:
        """Returns at most 1 item, doesn't fail if there's more"""
        results = self.sess.execute(stmt)
        return results.scalars().unique().first()

    def fetch_all(self,
                        stmt: Select | None = None,
                        limit: Pagination | int | None = None) -> list[_T]:
        if stmt is None:
            stmt = select(self.model)

        if isinstance(limit, Pagination):
            if limit.created_before is not None:
                tsmp = self.model.created_at  # type: ignore[attr-defined]
                stmt = stmt.where(tsmp < limit.created_before)
                stmt = stmt.order_by(tsmp.desc())  # Newest first
            stmt = stmt.limit(limit.page_size)

        elif isinstance(limit, int):
            stmt = stmt.limit(limit)

        results =  self.sess.execute(stmt)
        return results.scalars().unique().all()

    # Update
    def update_n(self, stmt: Delete | Insert | Update) -> int:
        results = self.sess.execute(stmt)
        return results.rowcount  # type: ignore[attr-defined]

    def update(self, filters: Mapping, data: Mapping) -> _T | None:
        # yapf: disable
        row_stmt = (
            update(self.model)
            .returning(self.model)
            .filter_by(**filters)
            .values(data)
        )
        # yapf: enable
        stmt = _rows_to_orm(row_stmt, self.model)
        result = self.sess.scalar(stmt)
        self.sess.flush()
        return self.sess.scalar(stmt)

    # Delete
    def delete_orm(self, obj) -> None:
        self.sess.delete(obj)

    def delete(self, filters: Mapping) -> None:
        stmt = delete(self.model).filter_by(**filters)
        self.sess.execute(stmt)

    # Etc.
    def insert_or_update(self, ids: Mapping, values: Mapping):
        # yapf: disable
        upsert_stmt = (
            postgresql.insert(self.model)
            .values(ids | values)  # type: ignore[operator]
            .on_conflict_do_update(
                index_elements=[*ids],
                set_=values,
            )
            .returning(self.model)
        )
        # yapf: enable
        stmt = _rows_to_orm(upsert_stmt, self.model)
        return self.sess.scalar(stmt)
