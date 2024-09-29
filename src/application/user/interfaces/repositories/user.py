from abc import ABC, abstractmethod
from uuid import UUID

from domain.user.entities.user import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def save(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    async def get_by_uuid(self, uuid: UUID) -> UserEntity:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> UserEntity:
        pass

    @abstractmethod
    async def update(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    async def delete(self, uuid: UUID) -> None:
        pass
