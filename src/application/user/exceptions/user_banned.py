class UserBannedException(Exception):
    def __init__(self, message: str = "User is banned."):
        super().__init__(message)
