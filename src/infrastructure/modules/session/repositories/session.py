from uuid import UUID

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from application.session.interfaces.repositories.session import (
    ISessionRepository,
)
from domain.session.entities.session import SessionEntity
from infrastructure.modules.session.models.session import Session
from shared.exceptions.not_found import NotFoundException


class SessionRepository(ISessionRepository):
    model = Session

    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def save(self, session: SessionEntity) -> None:
        stmt = insert(self.model).values(
            uuid=session.uuid,
            user_uuid=session.user_uuid,
            session_id=session.session_id,
            browser=session.user_agent.browser,
            browser_version=session.user_agent.browser_version,
            os=session.user_agent.os,
            device=session.user_agent.device,
            ip_address=session.ip_address,
            expires_at=session.expires_at,
            created_at=session.created_at,
            updated_at=session.updated_at,
            last_activity_at=session.last_activity_at,
        )
        await self.session.execute(stmt)
        await self.commit()

    async def get_all_by_user_uuid(
        self, user_uuid: UUID
    ) -> list[SessionEntity]:
        stmt = select(self.model).filter_by(user_uuid=user_uuid)
        result = await self.session.execute(stmt)
        sessions = result.scalars().all()
        return [session.to_entity() for session in sessions]

    async def get_by_session_id(self, session_id: str) -> SessionEntity:
        stmt = select(self.model).filter_by(session_id=session_id)
        result = await self.session.execute(stmt)
        session = result.scalars().first()
        if not session:
            raise NotFoundException(
                "Session not found."
            )  # TODO: Create a custom exception
        return session.to_entity()

    async def delete(self, session: SessionEntity) -> None:
        stmt = delete(self.model).filter_by(uuid=session.uuid)
        await self.session.execute(stmt)
        await self.commit()
