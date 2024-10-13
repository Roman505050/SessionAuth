class UserNotConfirmEmailException(Exception):
    def __init__(self, message: str = "User not confirm email."):
        super().__init__(message)
