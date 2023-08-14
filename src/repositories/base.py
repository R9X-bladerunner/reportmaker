from typing import (
    TypeVar,
    Protocol,
    ClassVar,
    Generic,
    Mapping,
    Iterable,
    Sequence,
    Collection,
    overload,
    Any,
)

from fastapi import Depends
from sqlalchemy import (
    insert,
    select,
    Row,
    Executable,
    Select,
    Delete,
    Insert,
    Update,
    update,
    delete,
    TextClause,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import Mapped
from sqlalchemy.orm.interfaces import ORMOption
from sqlalchemy.sql import CompoundSelect
from sqlalchemy.sql.selectable import TypedReturnsRows
from uuid import UUID

from src.db.connection import get_session
from src.schemas.base import Pagination, PId, MdId, LgId, TId
from src.utils.custom_types import TModel

_T2 = TypeVar("_T2")
_Tup = TypeVar("_Tup", bound=tuple)


class _WithId(Protocol):
    id: ClassVar[Mapped[int]]


_T_with_id = TypeVar("_T_with_id", bound=_WithId, covariant=True)


class Repository(Generic[TModel]):
    model: type[TModel]

    def __init__(self, sess: AsyncSession = Depends(get_session)) -> None:
        self.sess = sess

    # Create
    async def add_orm(self, obj: _T2) -> _T2:
        """
        Save object (and its nested objects) into database.
        NOTE: Doesn't support `asyncio.gather` because of eager `sess.flush()`.
        NOTE: Does any of INSERT/UPDATE/DELETE sql.
        """
        self.sess.add(obj)
        await self.sess.flush()
        return obj

    async def bulk_add_orm(self, *objects: _T2) -> tuple[_T2, ...]:
        self.sess.add_all(objects)
        await self.sess.flush()
        return objects

    async def insert(self, item: Mapping) -> TModel:
        stmt = insert(self.model).returning(self.model).values(**item)
        objects = await self.sess.scalars(stmt)
        return next(objects)

    async def bulk_insert(self, items: Iterable[Mapping]) -> list[TModel]:
        stmt = insert(self.model).returning(self.model).values([*items])
        objects = await self.sess.scalars(stmt)
        return [*objects]

    # Retrieve
    async def get_(
        self,
        id_: int | MdId | PId | UUID | TId | LgId,
        options: Sequence[ORMOption] = (),
    ) -> TModel | None:
        return await self.sess.get(self.model, id_, options=options)

    async def bulk_get(
        self: "Repository[_T_with_id]", ids: Collection[int]
    ) -> list[_T_with_id]:
        if not ids:
            return []
        stmt = select(self.model).where(self.model.id.in_(ids))
        return await self.fetch_all(stmt)

    async def fetch_one_row(
        self, stmt: TypedReturnsRows[_Tup]
    ) -> Row[_Tup] | None:
        result = await self.sess.execute(stmt)
        return result.unique().fetchone()

    @overload
    async def fetch_one(
        self, stmt: TypedReturnsRows[tuple[_T2]]
    ) -> _T2 | None:
        ...

    @overload
    async def fetch_one(self, stmt: Executable) -> Any | None:
        ...

    async def fetch_one(self, stmt: Executable) -> Any | None:
        """Returns at most 1 item, fails if there's more"""
        objects = await self.sess.scalars(stmt)
        return objects.unique().one_or_none()

    @overload
    async def fetch_first(
        self, stmt: TypedReturnsRows[tuple[_T2]]
    ) -> _T2 | None:
        ...

    @overload
    async def fetch_first(self, stmt: Executable) -> Any | None:
        ...

    async def fetch_first(self, stmt: Executable) -> Any | None:
        """Returns at most 1 item, doesn't fail if there's more"""
        objects = await self.sess.scalars(stmt)
        return next(objects.unique(), None)

    @overload
    async def fetch_all(
        self, *, pagination: Pagination | None = ...
    ) -> list[TModel]:
        ...

    @overload
    async def fetch_all(
        self,
        stmt: Select[tuple[_T2]],
        pagination: Pagination | None = ...,
    ) -> list[_T2]:
        ...

    async def fetch_all(
        self,
        stmt: Select[tuple[_T2]] | None = None,
        pagination: Pagination | None = None,
    ) -> list[TModel] | list[_T2]:
        if stmt is None:
            stmt = select(self.model)
        assert stmt is not None

        if pagination:
            stmt = stmt.limit(pagination.limit).offset(
                pagination.limit * (pagination.page_number - 1)
            )

        objects = await self.sess.scalars(stmt)
        return [*objects.unique()]

    async def filter_all(self, filters: Mapping[str, Any]) -> list[TModel]:
        """Returns filtered item's list"""
        stmt = select(self.model).filter_by(**filters)
        return await self.fetch_all(stmt)

    async def filter_one(
        self, filters: Mapping[str, Any], options: Sequence[ORMOption] = ()
    ) -> TModel | None:
        """Returns at most 1 item by filters, fails if there's more"""
        stmt = select(self.model).filter_by(**filters).options(*options)
        return await self.fetch_one(stmt)

    # Update
    async def update_n(self, stmt: Delete | Insert | Update) -> int:
        results = await self.sess.execute(stmt)
        return results.rowcount  # type: ignore[attr-defined]

    async def update(
        self, filters: Mapping[str, Any], data: Mapping[str, Any]
    ) -> TModel | None:
        stmt = (
            update(self.model)
            .returning(self.model)
            .filter_by(**filters)
            .values(data)
        )
        return await self.sess.scalar(stmt)

    # Delete
    async def delete_orm(self, obj) -> None:
        await self.sess.delete(obj)

    async def delete(
        self, filters: Mapping, synchronize_session: bool | str = False
    ) -> None:
        stmt = (
            delete(self.model)
            .filter_by(**filters)
            .execution_options(synchronize_session=synchronize_session)
        )
        await self.sess.execute(stmt)

    # Etc.
    async def insert_or_update(self, ids: Mapping, values: Mapping):
        stmt = (
            postgresql.insert(self.model)
            .values(ids | values)  # type: ignore[operator]
            .on_conflict_do_update(index_elements=[*ids], set_=values)
            .returning(self.model)
        )
        return await self.sess.scalar(stmt)

    def _rows_to_orm(
        self, stmt: Update | Insert | CompoundSelect | TextClause
    ) -> Select:
        return (
            select(self.model)
            .from_statement(stmt)
            .execution_options(populate_existing=True)
        )
