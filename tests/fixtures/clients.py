from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
import pytest

from api.rest.main import app


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
