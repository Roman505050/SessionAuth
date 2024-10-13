from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.pool import NullPool
from alembic.config import Config
from alembic import command
from typing import AsyncGenerator
import asyncio
import pytest

from infrastructure.database.base import Base
from tests.overrides.dependency_overrides import (
    override_get_session_dependency,
)
from tests.env_config import DATABASE_URL_TEST


engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
Base.metadata.bind = engine_test # type: ignore[attr-defined]


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.attributes["connection"] = engine_test
    event_loop = asyncio.get_event_loop()
    print("\n")
    await event_loop.run_in_executor(
        None, lambda: command.upgrade(alembic_cfg, "head")
    )
    print("\n")
    yield
    print("\n")
    await event_loop.run_in_executor(
        None, lambda: command.downgrade(alembic_cfg, "base")
    )


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in override_get_session_dependency():
        yield session
