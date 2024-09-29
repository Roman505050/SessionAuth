from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.dialects.postgresql import (
    UUID as PgUUID,  # noqa
)
from typing import List
from uuid import uuid4, UUID

from infrastructure.database.base import Base, created_at, updated_at
from infrastructure.modules.user.models.role import Role
from infrastructure.modules.user.models.users_roles_association import (
    users_roles_association_table,
)
from domain.user.entities.user import UserEntity


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    username: Mapped[str] = mapped_column(String(length=50), nullable=False)
    email: Mapped[str] = mapped_column(String(length=320), nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    email_verified: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    roles: Mapped[List[Role]] = relationship(
        secondary=users_roles_association_table,
    )

    @staticmethod
    def from_entity(user: UserEntity) -> "User":
        return User(
            uuid=user.uuid,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            email_verified=user.email_verified,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def to_entity(self) -> UserEntity:
        return UserEntity(
            uuid=self.uuid,
            username=self.username,
            email=self.email,
            password_hash=self.password_hash,
            email_verified=self.email_verified,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
            roles=[],
        )
