from abc import ABC, abstractmethod
from uuid import UUID

from domain.code.enums import Purpose
from domain.code.entities.email_code import EmailCodeEntity


class IEmailCodeRepository(ABC):
    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def save(self, code: EmailCodeEntity) -> EmailCodeEntity:
        pass

    @abstractmethod
    async def update(self, code: EmailCodeEntity) -> EmailCodeEntity:
        pass

    @abstractmethod
    async def get_by_purpose(
        self, user_uuid: UUID, purpose: Purpose
    ) -> EmailCodeEntity:
        pass

    @abstractmethod
    async def get_by_code(self, user_uuid: UUID, code: str) -> EmailCodeEntity:
        pass
