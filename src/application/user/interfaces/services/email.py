from abc import ABC, abstractmethod
from uuid import UUID

from domain.code.enums import Purpose


class IEmailService(ABC):
    @abstractmethod
    async def send_email(self, email: str, subject: str, body: str) -> None:
        pass

    @abstractmethod
    async def send_verification_code(
        self,
        user_uuid: UUID,
        email: str,
        purpose: Purpose,
    ) -> None:
        pass
