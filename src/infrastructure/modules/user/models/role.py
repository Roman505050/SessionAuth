from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import (
    UUID as PgUUID,  # noqa
)
from uuid import uuid4, UUID

from infrastructure.database.base import Base, created_at, updated_at
from domain.user.entities.role import RoleEntity


class Role(Base):
    __tablename__ = "roles"

    uuid: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String(length=64), nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    @staticmethod
    def from_entity(role: RoleEntity) -> "Role":
        return Role(
            uuid=role.uuid,
            name=role.name,
            created_at=role.created_at,
            updated_at=role.updated_at,
        )

    def to_entity(self) -> RoleEntity:
        return RoleEntity(
            uuid=self.uuid,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
