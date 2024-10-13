from fastapi import Depends

from api.rest.dependencies.email_code_service import (
    get_email_sender,
    get_email_code_repo,
)
from application.code.ports.services.email import IEmailSender
from application.code.services.email_code_service import EmailCodeService
from infrastructure.modules.code.repositories.email_code import (
    EmailCodeRepository,
)


class OverrideEmailCodeService(EmailCodeService):
    @staticmethod
    def generate_code() -> str:
        return "123456"


def override_get_email_code_service(
    email_service: IEmailSender = Depends(get_email_sender),
    email_code_repo: EmailCodeRepository = Depends(get_email_code_repo),
):
    return OverrideEmailCodeService(
        email_service=email_service, email_code_repo=email_code_repo
    )
