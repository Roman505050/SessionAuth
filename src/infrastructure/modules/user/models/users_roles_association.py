from sqlalchemy import Column, Table, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import (
    UUID as PgUUID,  # noqa
)
from uuid import uuid4

from infrastructure.database.base import Base

users_roles_association_table = Table(
    "users_roles_association",
    Base.metadata,
    Column("uuid", PgUUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("user_uuid", ForeignKey("users.uuid"), nullable=False),
    Column("role_uuid", ForeignKey("roles.uuid"), nullable=False),
    UniqueConstraint("user_uuid", "role_uuid", name="unique_user_role"),
)
