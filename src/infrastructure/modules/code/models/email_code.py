from sqlalchemy import String, ForeignKey, SMALLINT, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import (
    UUID as PgUUID,
    ENUM as PgENUM,
)
from uuid import uuid4, UUID
import datetime

from infrastructure.database.base import Base, created_at, updated_at
from domain.code.entities.email_code import EmailCodeEntity
from domain.code.enums import Status, Purpose


class EmailCode(Base):
    __tablename__ = "email_codes"

    uuid: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    user_uuid: Mapped[UUID] = mapped_column(
        ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False
    )
    purpose: Mapped[Purpose] = mapped_column(
        PgENUM(
            Purpose,
            name="email_code_purpose",
        ),
        nullable=False,
    )
    code: Mapped[str] = mapped_column(String(length=6), nullable=False)
    attempts: Mapped[int] = mapped_column(SMALLINT, nullable=False, default=0)
    max_attempts: Mapped[int] = mapped_column(
        SMALLINT, nullable=False, default=3
    )
    status: Mapped[Status] = mapped_column(
        PgENUM(
            Status,
            name="email_code_status",
        ),
        nullable=False,
        default="pending",
    )
    expires_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    __table_args__ = (
        CheckConstraint(
            "attempts >= 0 AND attempts <= 16", name="check_limit_attempts"
        ),
        CheckConstraint(
            "max_attempts >= 0 AND max_attempts <= 16",
            name="check_limit_max_attempts",
        ),
        CheckConstraint(
            "attempts <= max_attempts", name="check_attempts_max_attempts"
        ),
    )

    @staticmethod
    def from_entity(email_code: EmailCodeEntity) -> "EmailCode":
        return EmailCode(
            uuid=email_code.uuid,
            user_uuid=email_code.user_uuid,
            purpose=email_code.purpose,
            code=email_code.code,
            attempts=email_code.attempts,
            max_attempts=email_code.max_attempts,
            status=email_code.status,
            expires_at=email_code.expires_at,
            created_at=email_code.created_at,
            updated_at=email_code.updated_at,
        )

    def to_entity(self) -> EmailCodeEntity:
        return EmailCodeEntity(
            uuid=self.uuid,
            user_uuid=self.user_uuid,
            code=self.code,
            purpose=self.purpose,
            attempts=self.attempts,
            max_attempts=self.max_attempts,
            status=self.status,
            expires_at=self.expires_at,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
