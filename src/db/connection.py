import threading
from contextlib import suppress, asynccontextmanager
from typing import AsyncIterator

import sqlalchemy as sa
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
)

from src.core.config import settings

thread_local = threading.local()


def get_engine() -> AsyncEngine:
    if not hasattr(thread_local, "engine"):
        thread_local.engine = create_async_engine(
            settings.db_dsn, echo=settings.db_log_echo
        )
    return thread_local.engine


async def create_db(db_name: str) -> None:
    async with create_async_engine(
        settings.db_url, isolation_level="AUTOCOMMIT"
    ).connect() as conn:
        with suppress(ProgrammingError):
            await conn.execute(sa.text(f"CREATE DATABASE {db_name};"))


async def create_tables(metadata: sa.MetaData) -> None:
    async with get_engine().begin() as conn:
        await conn.run_sync(metadata.create_all)


async def drop_tables(metadata: sa.MetaData) -> None:
    async with get_engine().begin() as conn:
        await conn.run_sync(metadata.drop_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSession(get_engine(), expire_on_commit=False) as sess:
        try:
            yield sess
        except Exception:
            raise
        else:
            await sess.commit()


session_ctx = asynccontextmanager(get_session)
