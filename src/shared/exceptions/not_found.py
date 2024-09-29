class NotFoundException(Exception):
    def __init__(self, message: str = "Not found") -> None:
        super().__init__(message)
