from application.session.exceptions.session_not_valid import (
    SessionNotValidException,
)


class SessionExpiredException(SessionNotValidException):
    def __init__(self, message: str = "Session expired."):
        super().__init__(message)
