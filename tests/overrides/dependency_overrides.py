from api.rest.dependencies.email_code_service import get_email_sender
from infrastructure.database.connext import get_session_dependency
from infrastructure.redis.connext import get_redis_dependency
from tests.mocks.email_sender import MockEmailSender
from api.rest.main import app


async def override_get_session_dependency():
    # Because of the circular import, we need to import the async_session_maker here
    from tests.fixtures.database_fixture import async_session_maker

    async with async_session_maker() as session:
        yield session


async def override_get_redis_dependency():
    # Because of the circular import, we need to import the async_redis_client here
    from tests.fixtures.redis_fixture import async_redis_client

    yield async_redis_client
    await async_redis_client.aclose()


app.dependency_overrides[get_session_dependency] = (
    override_get_session_dependency
)
app.dependency_overrides[get_redis_dependency] = override_get_redis_dependency
app.dependency_overrides[get_email_sender] = MockEmailSender
