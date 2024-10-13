class UserIsDeactivateException(Exception):
    def __init__(self, message: str = "User is deactivate."):
        super().__init__(message)
