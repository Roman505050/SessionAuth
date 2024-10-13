from typing import AsyncGenerator
from redis.asyncio import Redis

from config import redis_settings as settings

async_redis_client = Redis(
    host=settings.HOST,
    port=settings.PORT,
    db=settings.DB,
    # username=redis_settings.USERNAME,
    password=settings.PASSWORD,
)


async def get_redis_dependency() -> AsyncGenerator[Redis, None]:
    yield async_redis_client
    await async_redis_client.close()
