from dataclasses import dataclass, field
from uuid import UUID, uuid4
import datetime

from shared.domain.entity import Entity
from domain.code.enums import Status, Purpose


@dataclass
class EmailCodeEntity(Entity):
    user_uuid: UUID
    purpose: Purpose
    code: str
    status: Status
    expires_at: datetime.datetime
    attempts: int
    max_attempts: int = field(default=3)
    _attempts: int = field(init=False, repr=False)

    @staticmethod
    def factory(
        user_uuid: UUID,
        purpose: Purpose,
        code: str,
        expires_at: datetime.datetime,
    ) -> "EmailCodeEntity":
        return EmailCodeEntity(
            uuid=uuid4(),
            user_uuid=user_uuid,
            purpose=purpose,
            code=code,
            attempts=0,
            status=Status.PENDING,
            expires_at=expires_at,
            created_at=datetime.datetime.now(datetime.timezone.utc),
            updated_at=datetime.datetime.now(datetime.timezone.utc),
        )

    def can_attempt(self):
        return self.attempts < self.max_attempts

    @property  # type: ignore[no-redef]
    def attempts(self):
        return self._attempts

    @attempts.setter
    def attempts(self, value: int):
        if hasattr(self, "_attempts") and self._attempts >= self.max_attempts:
            raise ValueError("Max attempts reached")
        if value > self.max_attempts:
            raise ValueError("Max attempts reached")
        self._attempts = value

    def check(self, code: str) -> Status:
        now = datetime.datetime.now(datetime.timezone.utc)
        if now > self.expires_at:
            self.status = Status.EXPIRED
            return self.status

        if self.code == code:
            self.status = Status.ACCEPTED
        else:
            self.attempts += 1
            if not self.can_attempt():
                self.status = Status.REJECTED
        return self.status

    @staticmethod
    def status_code_to_bool(status: str) -> bool:
        return status == "accepted"
