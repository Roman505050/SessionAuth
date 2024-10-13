from abc import ABC, abstractmethod
from uuid import UUID

from application.session.dto.session import SessionDTO
from application.user.dto.user import UserDTO
from domain.session.entities.session import SessionEntity
from domain.session.value_objects.user_agent import UserAgent


class ISessionService(ABC):
    @abstractmethod
    async def create(
        self, user: UserDTO, user_agent: UserAgent, ip_address: str
    ) -> tuple[list[SessionDTO], str]:
        pass

    @abstractmethod
    def create_session_entity(
        self, user: UserDTO, user_agent: UserAgent, ip_address: str
    ) -> SessionEntity:
        pass

    @abstractmethod
    async def validate_session(self, session_id: str) -> SessionDTO:
        pass

    @abstractmethod
    async def get_all_sessions_by_user_uuid(
        self, user_uuid: UUID, session_id: str | None = None
    ) -> list[SessionDTO]:
        pass
