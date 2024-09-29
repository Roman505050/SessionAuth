class AlreadyExistException(Exception):
    def __init__(self, message: str = "Already exist") -> None:
        super().__init__(message)
