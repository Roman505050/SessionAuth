import pytest
from httpx import AsyncClient, ASGITransport
from api.rest.main import app

@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
