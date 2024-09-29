from shared.exceptions.already_exist import AlreadyExistException


class UserAlreadyExistException(AlreadyExistException):
    def __init__(self, message: str = "User already exist") -> None:
        super().__init__(message)
