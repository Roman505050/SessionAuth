from shared.exceptions.not_found import NotFoundException


class SessionNotFoundException(NotFoundException):
    def __init__(self, message: str = "Session not found.") -> None:
        super().__init__(message)
