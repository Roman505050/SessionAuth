from shared.exceptions.not_found import NotFoundException


class UserNotFoundException(NotFoundException):
    def __init__(self, message: str = "User not found") -> None:
        self.message = message
        super().__init__(self.message)
