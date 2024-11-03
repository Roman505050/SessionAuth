import pytest
from httpx import AsyncClient

from api.rest.dependencies.email_code_service import get_email_code_service
from api.rest.main import app
from tests.overrides.email_code_service import override_get_email_code_service


@pytest.mark.asyncio
async def test_register(ac: AsyncClient):
    app.dependency_overrides[get_email_code_service] = (
        override_get_email_code_service
    )

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

    app.dependency_overrides[get_email_code_service] = get_email_code_service


@pytest.mark.asyncio
async def test_verify_email(ac: AsyncClient):
    response = await ac.post(
        "/api/v1/auth/confirm-email",
        json={
            "code": "998899",
        },
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["success"] == False
    assert data["message"] == "Invalid code. Attempts: 1/3"

    response = await ac.post(
        "/api/v1/auth/confirm-email",
        json={
            "code": "123456",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Email confirmed successfully."
    assert data["user"]["email_verified"] == True, "Email not confirmed"


@pytest.mark.asyncio
async def test_register_already_exist(ac: AsyncClient):
    response = await ac.post(
        "/api/v1/auth/register",
        json={
            "username": "david12",
            "email": "tothemoon@gmail.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 400, response.text

    data = response.json()
    assert data["success"] == False
    assert data["message"] == "User with username david12 already exists"

    response = await ac.post(
        "/api/v1/auth/register",
        json={
            "username": "david",
            "email": "david12@gmail.com",
            "password": "12345678",
        },
    )

    assert response.status_code == 400, response.text

    data = response.json()
    assert data["success"] == False
    assert (
        data["message"] == "User with email david12@gmail.com already exists"
    )

@pytest.mark.asyncio
async def test_login(ac: AsyncClient):
    response = await ac.post(
        "/api/v1/auth/login",
        json={
            "email": "david12@gmail.com",
            "password": "12345678",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Login successfully."
    assert data["user"]["email"] == "david12@gmail.com"