from redis.asyncio import Redis
from typing import AsyncGenerator
import pytest

from config import redis_settings
from tests.overrides.dependency_overrides import override_get_redis_dependency

async_redis_client = Redis(
    host=redis_settings.HOST,
    port=redis_settings.PORT,
    db=redis_settings.DB,
    # username=redis_settings.USERNAME,
    password=redis_settings.PASSWORD,
)


@pytest.fixture(scope="function")
async def redis_client() -> AsyncGenerator[Redis, None]:
    async for client in override_get_redis_dependency():
        yield client
