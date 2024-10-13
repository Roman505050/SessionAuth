from abc import ABC, abstractmethod
from uuid import UUID

from domain.session.entities.session import SessionEntity


class ISessionRepository(ABC):
    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def save(self, session: SessionEntity) -> None:
        pass

    @abstractmethod
    async def get_all_by_user_uuid(
        self, user_uuid: UUID
    ) -> list[SessionEntity]:
        pass

    @abstractmethod
    async def get_by_session_id(self, session_id: str) -> SessionEntity:
        pass

    @abstractmethod
    async def delete(self, session: SessionEntity) -> None:
        pass

    @abstractmethod
    async def delete_all_by_user_uuid(self, user_uuid: UUID) -> None:
        pass
