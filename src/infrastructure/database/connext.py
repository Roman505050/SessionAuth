from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import postgres_settings as settings


async_engine = create_async_engine(
    url=settings.db_uri_asyncpg,
    echo=False,
    pool_size=150,
    max_overflow=150,
    pool_timeout=60,
)
async_session_maker = async_sessionmaker(async_engine)


async def get_session_dependency():
    async with async_session_maker() as session:
        yield session
        await session.close()
