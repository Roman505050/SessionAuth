from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from user_agents import parse  # type: ignore

from api.rest.dependencies.email_code_service import get_email_code_service
from api.rest.dependencies.unitofwork import UOWDep
from application.code.services.email_code_service import EmailCodeService
from application.session.services.session_service import SessionService
from application.user.services.user_service import UserService
from domain.session.value_objects.user_agent import UserAgent
from infrastructure.database.connext import get_session_dependency
from infrastructure.modules.session.repositories.session import (
    SessionRepository,
)
from infrastructure.modules.user.repositories.user import UserRepository
from infrastructure.services.cryptography import CryptographyService


def get_ip_remote(request: Request) -> str:
    return request.headers.get("X-Real-IP", request.client.host)


def get_user_agent(request: Request) -> UserAgent:
    user_agent = parse(request.headers.get("User-Agent", "Unknown"))
    return UserAgent(
        browser=user_agent.browser.family,
        os=user_agent.os.family,
        device=user_agent.device.family,
        browser_version=user_agent.browser.version_string,
    )


def get_session_service(
    session: AsyncSession = Depends(get_session_dependency),
):
    return SessionService(SessionRepository(session))


def get_user_service(
    uow: UOWDep,
    session: AsyncSession = Depends(get_session_dependency),
    email_code_service: EmailCodeService = Depends(get_email_code_service),
    session_service: SessionService = Depends(get_session_service),
):
    return UserService(
        UserRepository(session),
        CryptographyService(),
        email_code_service,
        session_service,
        uow,
    )
