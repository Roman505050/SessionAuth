from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.pool import NullPool
from alembic.config import Config
from alembic import command
from dotenv import load_dotenv
import asyncio
import pytest
import os

from infrastructure.database.base import Base
from tests.overrides.dependency_overrides import override_get_session_dependency

load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")

DATABASE_URL_TEST = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
Base.metadata.bind = engine_test

@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.attributes["connection"] = engine_test
    event_loop = asyncio.get_event_loop()
    await event_loop.run_in_executor(
        None, lambda: command.upgrade(alembic_cfg, "head")
    )
    yield
    await event_loop.run_in_executor(
        None, lambda: command.downgrade(alembic_cfg, "base")
    )


@pytest.fixture(scope="function")
async def db_session() -> AsyncSession:
    async for session in override_get_session_dependency():
        yield session
