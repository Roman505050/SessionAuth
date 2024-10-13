from uuid import UUID
from loguru import logger
import datetime
import secrets

from application.session.dto.session import SessionDTO
from application.session.exceptions.session_expired import (
    SessionExpiredException,
)
from application.session.exceptions.session_not_found import (
    SessionNotFoundException,
)
from application.session.exceptions.session_not_valid import (
    SessionNotValidException,
)
from application.session.interfaces.session_service import ISessionService
from application.session.ports.repositories.session import (
    ISessionRepository,
)
from application.user.dto.user import UserDTO
from domain.session.entities.session import SessionEntity
from domain.session.value_objects.user_agent import UserAgent

from config import session_settings


class SessionService(ISessionService):
    def __init__(self, session_repository: ISessionRepository):
        self.session_repository = session_repository

    @staticmethod
    def generate_session_id() -> str:
        return secrets.token_hex(32)

    def create_session_entity(
        self, user: UserDTO, user_agent: UserAgent, ip_address: str
    ) -> SessionEntity:
        session_id = self.generate_session_id()

        session = SessionEntity.factory(
            user_uuid=user.uuid,
            session_id=session_id,
            user_agent=user_agent,
            ip_address=ip_address,
            expires_at=datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(seconds=session_settings.EXPIRE_SECONDS),
            created_at=datetime.datetime.now(datetime.timezone.utc),
            updated_at=datetime.datetime.now(datetime.timezone.utc),
            last_activity_at=datetime.datetime.now(datetime.timezone.utc),
        )

        return session

    async def create(
        self, user: UserDTO, user_agent: UserAgent, ip_address: str
    ) -> tuple[list[SessionDTO], str]:
        sessions = await self.session_repository.get_all_by_user_uuid(
            user.uuid
        )

        if len(sessions) >= session_settings.MAX_SESSIONS:
            await self.session_repository.delete_all_by_user_uuid(user.uuid)
            sessions: list[SessionEntity] = []

        session_id = secrets.token_hex(32)

        session = self.create_session_entity(
            user=user, user_agent=user_agent, ip_address=ip_address
        )

        await self.session_repository.save(session)
        await self.session_repository.commit()

        dto_sessions = [
            SessionDTO.from_entity(session) for session in sessions
        ]
        dto_sessions.append(SessionDTO.from_entity(session, is_current=True))

        return dto_sessions, session_id

    async def validate_session(self, session_id: str) -> SessionEntity:
        try:
            session = await self.session_repository.get_by_session_id(
                session_id=session_id
            )
        except SessionNotFoundException as e:
            raise SessionNotValidException() from e

        if session.expires_at < datetime.datetime.now(datetime.timezone.utc):
            raise SessionExpiredException()

        return session

    async def get_all_sessions_by_user_uuid(
        self, user_uuid: UUID, session_id: str | None = None
    ) -> list[SessionDTO]:
        sessions = await self.session_repository.get_all_by_user_uuid(
            user_uuid
        )
        dto_sessions = [
            SessionDTO.from_entity(session) for session in sessions
        ]

        if session_id:
            for session in dto_sessions:
                if session.session_id == session_id:
                    session.is_current = True
                    break
            else:
                logger.warning(
                    f"Session with id {session_id} not found in user sessions"
                )

        return dto_sessions
