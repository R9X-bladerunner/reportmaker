import asyncio
import sys
from contextlib import suppress, contextmanager

# https://stackoverflow.com/questions/54895002/modulenotfounderror-with-pytest
from sqlalchemy.orm import Session, sessionmaker

sys.path.append("src/tests")
from typing import Iterator

import pytest
from src.db.models.base import Base
from sqlalchemy import text, create_engine
from sqlalchemy.exc import ProgrammingError
from fastapi.testclient import TestClient
from src.core.config import settings
from src.core.main import app
from src.db.connection import get_session

pytest_plugins = [
    "data.patients",
    "data.relatives",
    "data.documents"
]

engine = create_engine(
    settings.test_db_dsn, echo=True
)


# https://github.com/pytest-dev/pytest-asyncio/issues/68
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def create_test_db() -> None:
    root_engine = create_engine(settings.test_db_url)
    with root_engine.begin() as conn:
        conn.execute(text("commit;"))
        with suppress(ProgrammingError):
            conn.execute(
                text(f"create database {settings.test_db_name};")
            )


@pytest.fixture(scope="session", autouse=True)
def migrations(create_test_db) -> None:
    """
    Создание тестовой БД
    """
    with engine.begin() as conn:
        Base.metadata.create_all(conn)
    yield
    # with engine.begin():
    #     Base.metadata.drop_all(engine)


TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_test_session() -> Iterator[Session]:
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.commit()
        session.close()


test_session_ctx = contextmanager(get_test_session)


@pytest.fixture()
def client() -> TestClient:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_session` dependency that is injected into routers.
    """
    app.dependency_overrides[get_session] = get_test_session

    return TestClient(app)
