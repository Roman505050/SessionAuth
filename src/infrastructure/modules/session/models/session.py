from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.dialects.postgresql import (
    UUID as PgUUID,
)
from typing import Optional
from uuid import uuid4, UUID
import datetime

from domain.session.entities.session import SessionEntity
from domain.session.value_objects.user_agent import UserAgent
from infrastructure.database.base import Base, created_at, updated_at


class Session(Base):
    __tablename__ = "sessions"

    uuid: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_uuid: Mapped[UUID] = mapped_column(ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False)
    session_id: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False
    )
    browser: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    browser_version: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True
    )
    os: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    device: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    ip_address: Mapped[str] = mapped_column(String(39), nullable=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    last_activity_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    @staticmethod
    def from_entity(entity: "SessionEntity") -> "Session":
        return Session(
            user_uuid=entity.user_uuid,
            session_id=entity.session_id,
            browser=entity.user_agent.browser,
            browser_version=entity.user_agent.browser_version,
            os=entity.user_agent.os,
            device=entity.user_agent.device,
            ip_address=entity.ip_address,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            last_activity_at=entity.last_activity_at,
        )

    def to_entity(self) -> "SessionEntity":
        return SessionEntity(
            uuid=self.uuid,
            user_uuid=self.user_uuid,
            session_id=self.session_id,
            user_agent=UserAgent(
                browser=self.browser,
                browser_version=self.browser_version,
                os=self.os,
                device=self.device,
            ),
            ip_address=self.ip_address,
            expires_at=self.expires_at,
            created_at=self.created_at,
            updated_at=self.updated_at,
            last_activity_at=self.last_activity_at,
        )
