from redis.asyncio import Redis
from fastapi import Depends

from application.code.services.email_code_service import EmailCodeService
from application.code.ports.services.email import IEmailSender
from infrastructure.modules.code.repositories.email_code import (
    EmailCodeRepository,
)
from infrastructure.redis.connext import get_redis_dependency
from infrastructure.services.email_service import RabbitMQEmailSender
from config import rabbitmq_settings as settings


def get_email_sender():
    return RabbitMQEmailSender(settings.rabbitmq_url)


def get_email_code_repo(
    redis_client: Redis = Depends(get_redis_dependency),
):
    return EmailCodeRepository(redis_client)


def get_email_code_service(
    email_service: IEmailSender = Depends(get_email_sender),
    email_code_repo: EmailCodeRepository = Depends(get_email_code_repo),
) -> EmailCodeService:
    return EmailCodeService(
        email_service=email_service,
        email_code_repo=email_code_repo,
    )
