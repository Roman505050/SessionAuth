from dataclasses import dataclass, field
import datetime


@dataclass
class EmailCodeEntity:
    code: str
    expires_at: datetime.datetime
    created_at: datetime.datetime
    attempts: int
    max_attempts: int = field(default=3)
    _attempts: int = field(init=False, repr=False)

    @staticmethod
    def factory(
        code: str,
        expires_at: datetime.datetime,
    ) -> "EmailCodeEntity":
        return EmailCodeEntity(
            code=code,
            attempts=0,
            expires_at=expires_at,
            created_at=datetime.datetime.now(datetime.timezone.utc),
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
