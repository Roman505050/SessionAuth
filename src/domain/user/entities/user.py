from dataclasses import dataclass, field
from uuid import uuid4
import datetime

from domain.user.entities.role import RoleEntity
from shared.domain.entity import Entity
from shared.validators.email import validate_email


@dataclass
class UserEntity(Entity):
    username: str
    password_hash: str
    roles: list[RoleEntity]
    email_verified: bool = field(default=False)
    is_active: bool = field(default=True)
    email: str  # type: ignore[misc]
    _email: str = field(init=False, repr=False)

    def __post_init__(self):
        self._validate_username(self.username)

    @staticmethod
    def factory(
        username: str, email: str, password_hash: str, roles: list[RoleEntity]
    ) -> "UserEntity":
        return UserEntity(
            uuid=uuid4(),
            username=username,
            email=email,
            password_hash=password_hash,
            roles=roles,
            created_at=datetime.datetime.now(datetime.timezone.utc),
            updated_at=datetime.datetime.now(datetime.timezone.utc),
        )

    @property  # type: ignore[no-redef]
    def email(self):
        return self._email

    @email.setter
    def email(self, value: str):
        value = validate_email(value)
        self._email = value

    @staticmethod
    def _validate_username(username: str) -> None:
        if not 3 <= len(username) <= 64:
            raise ValueError("Username must be between 3 and 64 characters")
