from pydantic import BaseModel
from typing import Optional
from uuid import UUID
import datetime

from domain.session.entities.session import SessionEntity


class SessionDTO(BaseModel):
    uuid: UUID
    browser: Optional[str]
    browser_version: Optional[str]
    os: Optional[str]
    device: Optional[str]
    ip_address: Optional[str]
    is_current: (
        bool  # This is a flag to indicate if the session is the current one
    )
    created_at: datetime.datetime
    last_activity_at: datetime.datetime

    @staticmethod
    def from_entity(
        entity: SessionEntity, is_current: bool = False
    ) -> "SessionDTO":
        return SessionDTO(
            uuid=entity.uuid,
            browser=entity.user_agent.browser,
            browser_version=entity.user_agent.browser_version,
            os=entity.user_agent.os,
            device=entity.user_agent.device,
            ip_address=entity.ip_address,
            is_current=is_current,
            created_at=entity.created_at,
            last_activity_at=entity.last_activity_at,
        )
