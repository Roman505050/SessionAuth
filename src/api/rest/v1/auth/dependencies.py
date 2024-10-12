from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from user_agents import parse  # type: ignore

from application.session.services.session_service import SessionService
from application.user.interfaces.services.email import IEmailService
from application.user.services.user_service import UserService
from config import rabbitmq_settings as settings
from domain.session.value_objects.user_agent import UserAgent
from infrastructure.database.connext import get_session_dependency
from infrastructure.modules.session.repositories.session import (
    SessionRepository,
)
from infrastructure.modules.user.repositories.user import UserRepository
from infrastructure.services.cryptography import CryptographyService
from infrastructure.services.email_service import RabbitMQEmailService


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


def get_email_service():
    return RabbitMQEmailService(settings.rabbitmq_url)


def get_user_service(
    session: AsyncSession = Depends(get_session_dependency),
    email_service: IEmailService = Depends(get_email_service),
):
    return UserService(
        UserRepository(session),
        CryptographyService(),
        email_service,
    )


def get_session_service(
    session: AsyncSession = Depends(get_session_dependency),
):
    return SessionService(SessionRepository(session))
