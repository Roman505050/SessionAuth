from abc import ABC, abstractmethod

from application.code.enums.email_code_type import EmailCodeType


class IEmailCodeService(ABC):
    @abstractmethod
    async def resend_code(
        self, code_type: EmailCodeType, email: str, **kwargs
    ) -> None:
        pass

    @abstractmethod
    async def send_code(
        self, code_type: EmailCodeType, email: str, **kwargs
    ) -> None:
        pass

    @abstractmethod
    async def validate_code(
        self, code_type: EmailCodeType, code: str, **kwargs
    ) -> bool:
        pass
