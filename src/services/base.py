from typing import TypeVar, Generic, Mapping, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.connection import get_session
from src.repositories.base import Repository
from src.schemas.base import Pagination, PId, MdId
from src.utils.custom_types import TModel

TRepository = TypeVar("TRepository", bound=Repository)


class BaseService(Generic[TRepository, TModel]):
    repo_type: type[TRepository]
    repo: TRepository

    def __init__(self, sess: AsyncSession = Depends(get_session)) -> None:
        self.sess = sess
        self.repo = self.repo_type(self.sess)
        self.check = 'check'

    async def base_fetch_all(
        self, pagination: Pagination | None = None
    ) -> list[TModel]:
        return await self.repo.fetch_all(pagination=pagination)

    async def base_create(self, data: Mapping[str, Any]) -> TModel:
        return await self.repo.insert(data)

    async def base_update(
        self, filters: Mapping[str, Any], data: Mapping[str, Any]
    ) -> TModel | None:
        return await self.repo.update(filters, data)

    async def base_delete(self, filters: Mapping[str, Any]) -> None:
        return await self.repo.delete(filters)

    async def base_fetch_one(self, id_: int | PId | MdId) -> TModel | None:
        return await self.repo.get_(id_)


