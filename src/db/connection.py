from threading import local
from contextlib import suppress

import sqlalchemy as sa
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import Engine

from src.core.config import settings

thread_local = local()

Base = declarative_base()


def get_engine() -> Engine:
    if not hasattr(thread_local, "engine"):
        thread_local.engine = sa.create_engine(
            settings.db_dsn, echo=settings.db_log_echo
        )
    return thread_local.engine


def create_db(db_name: str) -> None:
    with sa.create_engine(settings.db_url, isolation_level="AUTOCOMMIT").connect() as conn:
        with suppress(ProgrammingError):
            conn.execute(sa.text(f"CREATE DATABASE {db_name};"))


def create_tables(metadata: sa.MetaData) -> None:
    with get_engine().begin() as conn:
        metadata.create_all(conn)


def drop_tables(metadata: sa.MetaData) -> None:
    with get_engine().begin() as conn:
        metadata.drop_all(conn)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.commit()
        session.close()
