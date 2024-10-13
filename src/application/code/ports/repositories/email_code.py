from abc import ABC, abstractmethod

from application.code.enums.email_code_type import EmailCodeType
from domain.code.entities.email_code import EmailCodeEntity


class IEmailCodeRepository(ABC):
    @abstractmethod
    async def save(
        self, code_type: EmailCodeType, code: EmailCodeEntity, **kwargs
    ) -> None:
        pass

    @abstractmethod
    async def get(self, code_type: EmailCodeType, **kwargs) -> EmailCodeEntity:
        pass

    @abstractmethod
    async def delete(self, code_type: EmailCodeType, **kwargs) -> None:
        pass

    @abstractmethod
    async def update(
        self, code_type: EmailCodeType, code: EmailCodeEntity, **kwargs
    ) -> None:
        pass
