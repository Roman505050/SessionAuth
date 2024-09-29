from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4
import datetime

from shared.domain.entity import Entity
from domain.session.value_objects.user_agent import UserAgent


@dataclass
class SessionEntity(Entity):
    uuid: UUID
    user_uuid: UUID
    session_id: str
    user_agent: UserAgent
    ip_address: Optional[str]
    expires_at: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime
    last_activity_at: datetime.datetime

    @staticmethod
    def factory(
        user_uuid: UUID,
        session_id: str,
        user_agent: UserAgent,
        ip_address: str,
        expires_at: datetime.datetime,
        created_at: datetime.datetime,
        updated_at: datetime.datetime,
        last_activity_at: datetime.datetime,
    ) -> "SessionEntity":
        return SessionEntity(
            uuid=uuid4(),
            user_uuid=user_uuid,
            session_id=session_id,
            user_agent=user_agent,
            ip_address=ip_address,
            expires_at=expires_at,
            created_at=created_at,
            updated_at=updated_at,
            last_activity_at=last_activity_at,
        )
