from shared.exceptions.not_found import NotFoundException


class EmailCodeNotFoundException(NotFoundException):
    def __init__(self, message: str = "Code not found") -> None:
        super().__init__(message)
