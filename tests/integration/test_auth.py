import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register(ac: AsyncClient):
    response = await ac.post(
        "/api/v1/auth/register",
        json={
            "username": "david12",
            "email": "david12@gmail.com",
            "password": "12345678",
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["message"] == "Check your email box to verify your email."
    sessions = data["sessions"]
    current_session = None
    for session in sessions:
        if session["is_current"]:
            current_session = session
            break
    assert current_session is not None, "Current session not found"
