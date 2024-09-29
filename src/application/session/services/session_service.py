import datetime
import secrets

from application.session.dto.session import SessionDTO
from application.session.interfaces.repositories.session import (
    ISessionRepository,
)
from application.user.dto.user import UserDTO
from domain.session.entities.session import SessionEntity
from domain.session.value_objects.user_agent import UserAgent

from config import session_settings


class SessionService:
    def __init__(self, session_repository: ISessionRepository):
        self.session_repository = session_repository

    async def create(
        self, user: UserDTO, user_agent: UserAgent, ip_address: str
    ) -> tuple[list[SessionDTO], SessionEntity]:
        sessions = await self.session_repository.get_all_by_user_uuid(
            user.uuid
        )

        session_id = secrets.token_hex(32)

        session = SessionEntity.factory(
            user_uuid=user.uuid,
            session_id=session_id,
            user_agent=user_agent,
            ip_address=ip_address,
            expires_at=datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(seconds=session_settings.expire_seconds),
            created_at=datetime.datetime.now(datetime.timezone.utc),
            updated_at=datetime.datetime.now(datetime.timezone.utc),
            last_activity_at=datetime.datetime.now(datetime.timezone.utc),
        )

        await self.session_repository.save(session)
        await self.session_repository.commit()

        return [SessionDTO.from_entity(item) for item in sessions], session
