from api.rest.v1.auth.dependencies import get_email_service
from infrastructure.database.connext import get_session_dependency
from tests.mocks.email_service import MockEmailService
from api.rest.main import app

async def override_get_session_dependency():
    # Because of the circular import, we need to import the async_session_maker here
    from tests.fixtures.database import async_session_maker
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_session_dependency] = override_get_session_dependency
app.dependency_overrides[get_email_service] = MockEmailService
