from loguru import logger
import random
import string
import datetime

from application.code.enums.email_code_type import (
    EmailCodeType,
    EMAIL_CODE_REQUIRED_FIELDS,
)
from application.code.exceptions.code_expired import EmailCodeExpiredException
from application.code.exceptions.code_invalid import EmailCodeInvalidException
from application.code.exceptions.code_not_found import (
    EmailCodeNotFoundException,
)
from application.code.interfaces.email_code_service import IEmailCodeService
from application.code.ports.repositories.email_code import (
    IEmailCodeRepository,
)
from application.code.ports.services.email import IEmailSender
from domain.code.entities.email_code import EmailCodeEntity
from shared.validators.email import validate_email


class EmailCodeService(IEmailCodeService):
    def __init__(
        self,
        email_code_repo: IEmailCodeRepository,
        email_service: IEmailSender,
    ):
        self.email_code_repo = email_code_repo
        self.email_service = email_service

    @staticmethod
    def _validate_params(code_type: EmailCodeType, **kwargs):
        required = EMAIL_CODE_REQUIRED_FIELDS[code_type]
        missing = set(required) - set(kwargs.keys())
        if missing:
            raise ValueError(
                f"Missing required parameters for {code_type}: "
                f"{', '.join(missing)}"
            )

    @staticmethod
    def generate_code() -> str:
        return "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )

    async def resend_code(
        self, code_type: EmailCodeType, email: str, **kwargs
    ) -> None:
        self._validate_params(code_type, **kwargs)
        validate_email(email)

        try:
            code_entity = await self.email_code_repo.get(
                code_type=code_type,
                **kwargs,
            )

            await self.email_service.send_email(
                email=email,
                subject="Your verification code",
                body=f"Your code is: {code_entity.code}",
            )
        except EmailCodeNotFoundException as e:
            logger.info(f"Code not found. Sending new code. Error: {e}")
            await self.send_code(code_type, email, **kwargs)

    async def send_code(
        self, code_type: EmailCodeType, email: str, **kwargs
    ) -> None:
        # Validate parameters and email
        self._validate_params(code_type, **kwargs)
        validate_email(email)

        code = self.generate_code()

        code_entity = EmailCodeEntity.factory(
            code=code,
            expires_at=datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(minutes=5),
        )

        await self.email_code_repo.save(
            code_type=code_type,
            code=code_entity,
            **kwargs,
        )

        await self.email_service.send_email(
            email=email,
            subject="Your verification code",
            body=f"Your code is: {code}",
        )

    async def validate_code(
        self, code_type: EmailCodeType, code: str, **kwargs
    ) -> bool:
        self._validate_params(code_type, **kwargs)

        try:
            code_entity = await self.email_code_repo.get(
                code_type=code_type,
                **kwargs,
            )
        except EmailCodeNotFoundException as e:
            raise EmailCodeExpiredException("Email code expired.") from e

        if not code_entity.can_attempt():
            await self.email_code_repo.delete(
                code_type=code_type,
                **kwargs,
            )
            raise EmailCodeInvalidException(
                "Max attempts reached. Please try again later."
            )

        if code_entity.code != code:
            code_entity.attempts += 1
            if not code_entity.can_attempt():
                await self.email_code_repo.delete(
                    code_type=code_type,
                    **kwargs,
                )
                raise EmailCodeInvalidException(
                    "Max attempts reached. Please try again later."
                )
            try:
                await self.email_code_repo.update(
                    code_type=code_type,
                    code=code_entity,
                    **kwargs,
                )
            except EmailCodeNotFoundException as e:
                raise EmailCodeExpiredException("Email code expired.") from e
            raise EmailCodeInvalidException(
                f"Invalid code. Attempts: "
                f"{code_entity.attempts}/{code_entity.max_attempts}"
            )

        if code_entity.expires_at < datetime.datetime.now(
            datetime.timezone.utc
        ):
            await self.email_code_repo.delete(
                code_type=code_type,
                **kwargs,
            )
            raise EmailCodeExpiredException("Email code expired.")

        await self.email_code_repo.delete(
            code_type=code_type,
            **kwargs,
        )
        return True
