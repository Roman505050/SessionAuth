from pydantic import BaseModel, Field
from uuid import UUID
import datetime

from domain.user.entities.user import UserEntity


class UserDTO(BaseModel):
    uuid: UUID
    username: str = Field(..., min_length=3, max_length=64)
    email: str = Field(..., min_length=5, max_length=320)
    email_verified: bool
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @staticmethod
    def from_entity(entity: UserEntity) -> "UserDTO":
        return UserDTO(
            uuid=entity.uuid,
            username=entity.username,
            email=entity.email,
            email_verified=entity.email_verified,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
